from typing import Dict, Any
from cets_mmcif.models.categories import EmImagingOptics


def extract_em_imaging_optics(
    region: Dict[str, Any],
    region_index: int
) -> EmImagingOptics:
    return EmImagingOptics(
        id=region_index,
        imaging_id=region_index,
        energyfilter_name=None,
        phase_plate=None,
    )
