from typing import Dict, Any
from cets_mmcif.models.categories import EmImageScans


def extract_em_image_scans(
    region: Dict[str, Any],
    dataset_name: str
) -> EmImageScans:
    """
    Extract em_image_scans data from a CETS region.
    
    Args:
        region: CETS region dictionary
        dataset_name: Entry ID for the dataset
        
    Returns:
        EmImageScans model instance
    
    Note:
        Can be populated from definition file if needed.
    """
    region_id = region.get("id", "1")
    
    tilt_series_list = region.get("tilt_series", [])
    number_digital_images = None
    if tilt_series_list:
        images = tilt_series_list[0].get("images", [])
        number_digital_images = len(images) if images else None
    
    return EmImageScans(
        entry_id=dataset_name,
        id=f"{region_id}_scans_1",
        image_recording_id=region_id,
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
