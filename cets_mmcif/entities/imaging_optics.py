from typing import Dict, List, Any


def extract_em_imaging_optics(region: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract em_imaging_optics data from a CETS region.
    
    Args:
        region: CETS region dictionary
        
    Returns:
        Dictionary with extracted imaging optics data
    """
    region_id = region.get('id', '1')
    
    # Most imaging optics data is not present in CETS
    optics_id = f"{region_id}_1"
    energyfilter = "?"
    phase_plate = "?"
    
    return {
        'id': optics_id,
        'imaging_id': region_id,
        'energyfilter_name': energyfilter,
        'phase_plate': phase_plate
    }


def generate_em_imaging_optics(regions: List[Dict[str, Any]]) -> List[str]:
    """
    Generate em_imaging_optics category from multiple CETS regions.
    
    Args:
        regions: List of CETS region dictionaries
        
    Returns:
        List of mmCIF formatted lines
    """
    if not regions:
        return []
    
    # Extract data from all regions
    optics_data = [extract_em_imaging_optics(region) for region in regions]
    
    lines = []
    lines.append("#")
    lines.append("loop_")
    lines.append("_em_imaging_optics.id")
    lines.append("_em_imaging_optics.imaging_id")
    lines.append("_em_imaging_optics.energyfilter_name")
    lines.append("_em_imaging_optics.phase_plate")
    
    for optics in optics_data:
        lines.append(f"{optics['id']} {optics['imaging_id']} {optics['energyfilter_name']} {optics['phase_plate']}")
    
    lines.append("#")
    
    return lines
