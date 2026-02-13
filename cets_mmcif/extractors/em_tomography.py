from typing import Dict, Any, Optional
from cets_mmcif.models.categories import EmTomography


def extract_em_tomography(
    region: Dict[str, Any]
) -> Optional[EmTomography]:
    """
    Extract em_tomography data from a CETS region.
    
    Args:
        region: CETS region dictionary
        
    Returns:
        EmTomography model instance, or None if no tilt series data
    """
    region_id = region.get("id", "1")
    
    # Get tilt series data
    tilt_series_list = region.get("tilt_series", [])
    if not tilt_series_list:
        return None
    
    tilt_series = tilt_series_list[0]
    images = tilt_series.get("images", [])
    
    if not images:
        return None
    
    # Extract tilt angles
    tilt_angles = [
        img.get("nominal_tilt_angle", 0) 
        for img in images 
        if img.get("nominal_tilt_angle") is not None
    ]
    
    if not tilt_angles:
        return None
    
    # Calculate tilt range and increment
    # For single-axis: use min/max from images
    axis1_min = min(tilt_angles)
    axis1_max = max(tilt_angles)
    
    # Calculate increment (approximate - might vary in practice)
    if len(tilt_angles) > 1:
        sorted_angles = sorted(set(tilt_angles))
        increments = [sorted_angles[i+1] - sorted_angles[i] 
                     for i in range(len(sorted_angles)-1)]
        axis1_increment = sum(increments) / len(increments) if increments else None
    else:
        axis1_increment = None
    
    return EmTomography(
        id=region_id,
        imaging_id=region_id,
        axis1_min_angle=axis1_min,
        axis1_max_angle=axis1_max,
        axis1_angle_increment=axis1_increment,
        # TODO: dual-axis fields - typically None for single-axis tomo?
        axis2_min_angle=None,
        axis2_max_angle=None,
        axis2_angle_increment=None,
        dual_tilt_axis_rotation=None
    )
