from typing import Dict, List, Any, Optional


def _extract_pixel_spacing(tomogram: Dict[str, Any]) -> Optional[List[float]]:
    """
    Extract pixel spacing from tomogram coordinate transformations.
    
    Args:
        tomogram: Tomogram dictionary from CETS
        
    Returns:
        List of [x, y, z] pixel spacing in Angstroms, or None
    """
    transformations = tomogram.get('coordinate_transformations', [])
    
    for transform in transformations:
        if transform.get('transformation_type') == 'scale':
            scale = transform.get('scale', [])
            if len(scale) == 3:
                return scale
    
    return None


def _format_value(value: Any) -> str:
    """
    Format a value for mmCIF output.
    Returns '?' for None/missing values, proper formatting for strings with spaces.
    """
    if value is None:
        return '?'
    
    str_value = str(value)
    
    if ' ' in str_value:
        return f"'{str_value}'"
    
    return str_value


def extract_em_map(region: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract em_map data from a CETS region.
    
    Args:
        region: CETS region dictionary
        
    Returns:
        Dictionary with extracted map data, or None if no tomograms
    """
    tomograms = region.get('tomograms', [])
    if not tomograms:
        return None
    
    tomogram = tomograms[0]
    
    width = tomogram.get('width', '?')
    height = tomogram.get('height', '?')
    depth = tomogram.get('depth', '?')
    
    pixel_spacing = _extract_pixel_spacing(tomogram)
    px = _format_value(pixel_spacing[0] if pixel_spacing else None)
    py = _format_value(pixel_spacing[1] if pixel_spacing else None)
    pz = _format_value(pixel_spacing[2] if pixel_spacing else None)
    
    file_path = tomogram.get('path', '?')
    map_format = "'CCP4'" if file_path.endswith('.mrc') else '?'
    map_type = "'TOMOGRAM'"
    
    map_id = tomogram.get('id', '1')
    
    return {
        'id': map_id,
        'file': file_path,
        'format': map_format,
        'num_columns': width,
        'num_rows': height,
        'num_sections': depth,
        'pixel_spacing_x': px,
        'pixel_spacing_y': py,
        'pixel_spacing_z': pz,
        'type': map_type
    }


def generate_em_map(regions: List[Dict[str, Any]]) -> List[str]:
    """
    Generate em_map category from multiple CETS regions.
    
    Args:
        regions: List of CETS region dictionaries
        
    Returns:
        List of mmCIF formatted lines
    """
    # Extract data from all regions
    map_data = [extract_em_map(region) for region in regions]
    map_data = [data for data in map_data if data is not None]
    
    if not map_data:
        return []
    
    lines = []
    lines.append("#")
    lines.append("loop_")
    lines.append("_em_map.id")
    lines.append("_em_map.file")
    lines.append("_em_map.format")
    lines.append("_em_map.num_columns")
    lines.append("_em_map.num_rows")
    lines.append("_em_map.num_sections")
    lines.append("_em_map.pixel_spacing_x")
    lines.append("_em_map.pixel_spacing_y")
    lines.append("_em_map.pixel_spacing_z")
    lines.append("_em_map.type")
    
    for map_info in map_data:
        lines.append(f"{map_info['id']} {map_info['file']} {map_info['format']} {map_info['num_columns']} {map_info['num_rows']} {map_info['num_sections']} {map_info['pixel_spacing_x']} {map_info['pixel_spacing_y']} {map_info['pixel_spacing_z']} {map_info['type']}")
    
    lines.append("#")
    
    return lines
