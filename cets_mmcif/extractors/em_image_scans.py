from typing import Dict, Any
from cets_mmcif.models.categories import EmImageScans


def extract_em_image_scans(
    region: Dict[str, Any],
    dataset_name: str,
    region_index: int
) -> EmImageScans:
    tilt_series_list = region.get("tilt_series", [])
    number_digital_images = None
    if tilt_series_list:
        images = tilt_series_list[0].get("images", [])
        number_digital_images = len(images) if images else None

    return EmImageScans(
        entry_id=dataset_name,
        id=region_index,
        image_recording_id=region_index,
        number_digital_images=number_digital_images,
        scanner_model=None,
        sampling_size=None,
        od_range=None,
        quant_bit_size=None,
        citation_id=None,
        dimension_height=None,
        dimension_width=None,
        frames_per_image=None,
        used_frames_per_image=None,
        details=None
    )
