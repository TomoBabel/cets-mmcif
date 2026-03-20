from typing import Dict, Any
from cets_mmcif.models.categories import EmImageProcessing


def extract_em_image_processing(
    region: Dict[str, Any],
    region_index: int
) -> EmImageProcessing:
    return EmImageProcessing(
        id=region_index,
        image_recording_id=region_index,
        details=None
    )
