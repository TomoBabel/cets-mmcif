from typing import Dict, Any
from cets_mmcif.models.categories import EmSoftware


def extract_em_software(
    region: Dict[str, Any],
    region_index: int
) -> EmSoftware:
    return EmSoftware(
        id=region_index,
        name=None,
        category="RECONSTRUCTION",
        image_processing_id=region_index,
        version=None,
        details=None
    )
