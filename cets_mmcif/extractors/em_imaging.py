from typing import Dict, Any, Optional
from cets_mmcif.models.categories import EmImaging


def extract_em_imaging(
    region: Dict[str, Any],
    dataset_name: str, 
    region_index: int
) -> Optional[EmImaging]:
    """
    Extract em_imaging data from a CETS region.
    
    Args:
        region: CETS region dictionary
        dataset_name: Entry ID for the dataset
        
    Returns:
        EmImaging model instance, or None if no tilt series data

    Note:
        Several mandatory OneDep fields are not available in CETS:

        - microscope_model: Cannot be defaulted safely — dataset-specific.
          Set to None; OneDep will flag this(?) — can be supplied 
          e.g. via a definition file or manual entry.

        - illumination_mode: FLOOD BEAM is the standard for conventional
          cryo-ET. SPOT SCAN is only used for STEM tomography. Defaulting
          to FLOOD BEAM is correct for the vast majority of datasets.

        - specimen_id: Foreign key to em_specimen (id=1). Hardcoded to "1"
          as a conventional placeholder since em_specimen is generated
          separately with id=1.
    """
    tilt_series_list = region.get("tilt_series", [])
    if not tilt_series_list:
        return None
    
    tilt_series = tilt_series_list[0]
    images = tilt_series.get("images", [])
    
    if not images:
        return None
    
    tilt_angles = [
        img.get("nominal_tilt_angle", 0) 
        for img in images 
        if img.get("nominal_tilt_angle") is not None
    ]
    
    tilt_angle_min = min(tilt_angles) if tilt_angles else None
    tilt_angle_max = max(tilt_angles) if tilt_angles else None
    
    return EmImaging(
        entry_id=dataset_name,
        id=region_index,
        microscope_model=None,  # Not in CETS — must be supplied via definition file
        mode="BRIGHT FIELD",
        illumination_mode="FLOOD BEAM",  # Standard for cryo-ET; SPOT SCAN only for STEM
        specimen_id="1",  # to em_specimen.id — hardcoded key placeholder
        tilt_angle_min=tilt_angle_min,
        tilt_angle_max=tilt_angle_max,
        accelerating_voltage=None,  # Not in CETS
    )
