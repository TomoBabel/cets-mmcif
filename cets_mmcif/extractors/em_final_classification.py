from typing import Dict, Any
from cets_mmcif.models.categories import EmFinalClassification


def extract_em_final_classification(
    region: Dict[str, Any],
    region_index: int
) -> EmFinalClassification:
    return EmFinalClassification(
        id=region_index,
        image_processing_id=region_index,
        type=None,
        num_classes=None,
        avg_num_images_per_class=None,
        details=None
    )
