from typing import Dict, Any
from cets_mmcif.models.categories import EmImageRecording


def extract_em_image_recording(
    region: Dict[str, Any],
    region_index: int
) -> EmImageRecording:
    tilt_series_list = region.get("tilt_series", [])
    num_real_images = None
    if tilt_series_list:
        images = tilt_series_list[0].get("images", [])
        num_real_images = len(images) if images else None

    return EmImageRecording(
        id=region_index,
        imaging_id=region_index,
        num_real_images=num_real_images,
        detector_mode=None,
        film_or_detector_model=None,
    )
