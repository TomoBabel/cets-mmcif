from typing import Any, Dict, List


def extract_em_tomography(region: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract em_tomography data from a CETS region.
    
    Args:
        region: CETS region dictionary
        
    Returns:
        Dictionary with extracted tomography data, or None if no tilt series
    """
    region_id = region.get('id', '1')
    
    tilt_series_list = region.get('tilt_series', [])
    if not tilt_series_list:
        return None
    
    tilt_series = tilt_series_list[0]
    images = tilt_series.get('images', [])
    
    if not images:
        return None
    
    tilt_angles = [img.get('nominal_tilt_angle', 0) for img in images if img.get('nominal_tilt_angle') is not None]
    num_tilts = len(images)
    tilt_min = min(tilt_angles) if tilt_angles else 0
    tilt_max = max(tilt_angles) if tilt_angles else 0
    
    return {
        'id': region_id,
        'imaging_id': region_id,
        'num_tilts': num_tilts,
        'tilt_angle_min': f"{tilt_min:.2f}",
        'tilt_angle_max': f"{tilt_max:.2f}"
    }


def generate_em_tomography(regions: List[Dict[str, Any]]) -> List[str]:
    """
    Generate em_tomography category from multiple CETS regions.
    
    Args:
        regions: List of CETS region dictionaries
        
    Returns:
        List of mmCIF formatted lines
    """
    # Extract data from all regions
    tomo_data = [extract_em_tomography(region) for region in regions]
    tomo_data = [data for data in tomo_data if data is not None]
    
    if not tomo_data:
        return []
    
    lines = []
    lines.append("#")
    lines.append("loop_")
    lines.append("_em_tomography.id")
    lines.append("_em_tomography.imaging_id")
    lines.append("_em_tomography.num_tilts")
    lines.append("_em_tomography.tilt_angle_min")
    lines.append("_em_tomography.tilt_angle_max")
    
    for tomo in tomo_data:
        lines.append(f"{tomo['id']} {tomo['imaging_id']} {tomo['num_tilts']} {tomo['tilt_angle_min']} {tomo['tilt_angle_max']}")
    
    lines.append("#")
    
    return lines
