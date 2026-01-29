from typing import Any, Dict, List


def extract_em_imaging(region: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract em_imaging data from a CETS region.
    
    Args:
        region: CETS region dictionary
        
    Returns:
        Dictionary with extracted imaging data, or None if no tilt series
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
    
    electron_dose = images[-1].get('accumulated_dose', '?') if images else '?'
    tilt_min = min(tilt_angles) if tilt_angles else '?'
    tilt_max = max(tilt_angles) if tilt_angles else '?'
    
    # These fields are not in CETS
    microscope_model = "?"
    mode = "'BRIGHT FIELD'"  # Typical for cryo-ET
    accelerating_voltage = "?"
    illumination_mode = "?"
    
    return {
        'id': region_id,
        'microscope_model': microscope_model,
        'mode': mode,
        'tilt_angle_min': tilt_min,
        'tilt_angle_max': tilt_max,
        'electron_dose': electron_dose,
        'accelerating_voltage': accelerating_voltage,
        'illumination_mode': illumination_mode
    }


def generate_em_imaging(regions: List[Dict[str, Any]]) -> List[str]:
    """
    Generate em_imaging category from multiple CETS regions.
    
    Args:
        regions: List of CETS region dictionaries
        
    Returns:
        List of mmCIF formatted lines
    """
    # Extract data from all regions
    imaging_data = [extract_em_imaging(region) for region in regions]
    imaging_data = [data for data in imaging_data if data is not None]
    
    if not imaging_data:
        return []
    
    lines = []
    lines.append("#")
    lines.append("loop_")
    lines.append("_em_imaging.id")
    lines.append("_em_imaging.microscope_model")
    lines.append("_em_imaging.mode")
    lines.append("_em_imaging.tilt_angle_min")
    lines.append("_em_imaging.tilt_angle_max")
    lines.append("_em_imaging.electron_dose")
    lines.append("_em_imaging.accelerating_voltage")
    lines.append("_em_imaging.illumination_mode")
    
    for img in imaging_data:
        lines.append(f"{img['id']} {img['microscope_model']} {img['mode']} {img['tilt_angle_min']} {img['tilt_angle_max']} {img['electron_dose']} {img['accelerating_voltage']} {img['illumination_mode']}")
    
    lines.append("#")
    
    return lines
