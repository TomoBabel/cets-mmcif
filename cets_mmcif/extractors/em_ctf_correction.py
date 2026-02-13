from typing import Dict, Any
from cets_mmcif.models.categories import EmCtfCorrection


def extract_em_ctf_correction(region: Dict[str, Any]) -> EmCtfCorrection:
    """
    Extract em_ctf_correction data from a CETS region.
    
    Args:
        region: CETS region dictionary
        
    Returns:
        EmCtfCorrection model instance
    
    TODO: should get these from CETS
    """
    region_id = region.get("id", "1")
    
    return EmCtfCorrection(
        id=f"{region_id}_ctf_1",
        em_image_processing_id=f"{region_id}_processing",
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
