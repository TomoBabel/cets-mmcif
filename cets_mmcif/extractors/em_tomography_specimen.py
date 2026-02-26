from typing import Dict, Any
from cets_mmcif.models.categories import EmTomographySpecimen


def extract_em_tomography_specimen(
    region: Dict[str, Any],
    region_index: int
) -> EmTomographySpecimen:
    return EmTomographySpecimen(
        id=region_index,
        specimen_id=None,
        fiducial_markers=None,
        sectioning=None,
        high_pressure_freezing=None,
        cryo_protectant=None,
        details=None
    )
