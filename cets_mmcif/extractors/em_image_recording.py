from typing import Dict, Any
from cets_mmcif.models.categories import EmImageRecording


def extract_em_image_recording(region: Dict[str, Any]) -> EmImageRecording:
    """
    Extract em_image_recording data from a CETS region.
    
    Args:
        region: CETS region dictionary
        
    Returns:
        EmImageRecording model instance
    """
    region_id = region.get("id", "1")
    
    # Get number of images from tilt series
    tilt_series_list = region.get("tilt_series", [])
    num_real_images = None
    if tilt_series_list:
        images = tilt_series_list[0].get("images", [])
        num_real_images = len(images) if images else None
    
    return EmImageRecording(
        id=region_id,
        imaging_id=region_id,
        num_real_images=num_real_images,
        detector_mode=None,  # Not in CETS
        film_or_detector_model=None,  # Not in CETS
        # All other fields default to None
    )
