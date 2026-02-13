from typing import Dict, Any, Optional
from cets_mmcif.models.categories import Em3dReconstruction


def extract_em_3d_reconstruction(
    region: Dict[str, Any],
    dataset_name: str
) -> Optional[Em3dReconstruction]:
    """
    Extract em_3d_reconstruction data from a CETS region.
    
    Args:
        region: CETS region dictionary
        dataset_name: Entry ID for the dataset
        
    Returns:
        Em3dReconstruction model instance, or None if no tilt series
    """
    region_id = region.get("id", "1")
    
    # Get tilt series data for num_particles
    tilt_series_list = region.get("tilt_series", [])
    if not tilt_series_list:
        return None
    
    tilt_series = tilt_series_list[0]
    images = tilt_series.get("images", [])
    num_images = len(images)
    
    return Em3dReconstruction(
        entry_id=dataset_name,
        id=region_id,
        image_processing_id=f"{region_id}_processing",
        method="TOMOGRAPHY",
        num_particles=num_images,
        # All other fields not in CETS...
        algorithm=None,
        resolution=None,
        resolution_method=None,
        nominal_pixel_size=None,
    )
