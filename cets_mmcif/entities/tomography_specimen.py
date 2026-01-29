from typing import Dict, Any, List


def extract_em_tomography_specimen(region: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract em_tomography_specimen data from a CETS region.
    
    Args:
        region: CETS region dictionary
        
    Returns:
        Dictionary with extracted specimen data
    """
    region_id = region.get('id', '1')
    
    specimen_id = f"{region_id}_specimen"
    fiducial_markers = "?"
    high_pressure_freezing = "?"
    
    return {
        'id': specimen_id,
        'fiducial_markers': fiducial_markers,
        'high_pressure_freezing': high_pressure_freezing
    }


def generate_em_tomography_specimen(regions: List[Dict[str, Any]]) -> List[str]:
    """
    Generate em_tomography_specimen category from multiple CETS regions.
    
    Args:
        regions: List of CETS region dictionaries
        
    Returns:
        List of mmCIF formatted lines
    """
    if not regions:
        return []
    
    # Extract data from all regions
    specimen_data = [extract_em_tomography_specimen(region) for region in regions]
    
    lines = []
    lines.append("#")
    lines.append("loop_")
    lines.append("_em_tomography_specimen.id")
    lines.append("_em_tomography_specimen.fiducial_markers")
    lines.append("_em_tomography_specimen.high_pressure_freezing")
    
    for specimen in specimen_data:
        lines.append(f"{specimen['id']} {specimen['fiducial_markers']} {specimen['high_pressure_freezing']}")
    
    lines.append("#")
    
    return lines
