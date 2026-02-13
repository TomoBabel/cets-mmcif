from typing import Dict, Any, Optional
from cets_mmcif.models.categories import EmImaging


def extract_em_imaging(
    region: Dict[str, Any],
    dataset_name: str
) -> Optional[EmImaging]:
    """
    Extract em_imaging data from a CETS region.
    
    Args:
        region: CETS region dictionary
        dataset_name: Entry ID for the dataset
        
    Returns:
        EmImaging model instance, or None if no tilt series data
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
    
    # Calculate min/max tilt angles
    tilt_angle_min = min(tilt_angles) if tilt_angles else None
    tilt_angle_max = max(tilt_angles) if tilt_angles else None
    
    # Extract electron dose (last image"s accumulated dose)
    electron_dose = images[-1].get("accumulated_dose") if images else None
    
    return EmImaging(
        entry_id=dataset_name,
        id=region_id,
        microscope_model=None,  # Not in CETS
        mode="BRIGHT FIELD",  # TODO: is this typical for cryo-ET — check...
        tilt_angle_min=tilt_angle_min,
        tilt_angle_max=tilt_angle_max,
        electron_dose=electron_dose,  # Note: deprecated but commonly used
        accelerating_voltage=None,  # Not in CETS
        illumination_mode=None,  # Not in CETS
        specimen_id=None,  # Not in CETS
        # All other fields default to None
    )
