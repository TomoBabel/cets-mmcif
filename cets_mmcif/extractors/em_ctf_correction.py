from typing import Dict, Any
from cets_mmcif.models.categories import EmCtfCorrection


def extract_em_ctf_correction(
    region: Dict[str, Any],
    region_index: int
) -> EmCtfCorrection:
    return EmCtfCorrection(
        id=region_index,
        em_image_processing_id=region_index,
        type=None,
        correction_operation=None,
        phase_reversal=None,
        phase_reversal_correction_space=None,
        phase_reversal_anisotropic=None,
        amplitude_correction=None,
        amplitude_correction_factor=None,
        amplitude_correction_space=None,
        details=None
    )
