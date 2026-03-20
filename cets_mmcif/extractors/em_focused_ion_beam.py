from typing import Dict, Any
from cets_mmcif.models.categories import EmFocusedIonBeam


def extract_em_focused_ion_beam(
    region: Dict[str, Any],
    region_index: int
) -> EmFocusedIonBeam:
    return EmFocusedIonBeam(
        id=region_index,
        em_tomography_specimen_id=region_index,
        instrument=None,
        ion=None,
        voltage=None,
        current=None,
        duration=None,
        initial_thickness=None,
        final_thickness=None,
        dose_rate=None,
        temperature=None,
        details=None
    )
