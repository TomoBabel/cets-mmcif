from typing import Dict, Any, Optional
from cets_mmcif.models.categories import Em3dReconstruction


def extract_em_3d_reconstruction(
    region: Dict[str, Any],
    dataset_name: str,
    region_index: int
) -> Optional[Em3dReconstruction]:
    tilt_series_list = region.get("tilt_series", [])
    if not tilt_series_list:
        return None

    images = tilt_series_list[0].get("images", [])
    num_images = len(images)

    return Em3dReconstruction(
        entry_id=dataset_name,
        id=region_index,
        image_processing_id=region_index,
        method="TOMOGRAPHY",
        num_particles=num_images,
        algorithm=None,
        resolution=None,
        resolution_method=None,
        nominal_pixel_size=None,
    )