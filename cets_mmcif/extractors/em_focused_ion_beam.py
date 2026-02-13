from typing import Dict, Any
from cets_mmcif.models.categories import EmFocusedIonBeam


def extract_em_focused_ion_beam(region: Dict[str, Any]) -> EmFocusedIonBeam:
    """
    Extract em_focused_ion_beam data.
    
    Args:
        region: CETS region dictionary
        
    Returns:
        EmFocusedIonBeam model instance
    
    Note:
        These data are not available in CETS — all fields return None.
        Could populate from an external definition file?
    """
    region_id = region.get("id", "1")
    
    return EmFocusedIonBeam(
        id=f"{region_id}_fib_1",
        em_tomography_specimen_id=region_id,
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
