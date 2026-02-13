from typing import Dict, Any
from cets_mmcif.models.categories import EmImagingOptics


def extract_em_imaging_optics(region: Dict[str, Any]) -> EmImagingOptics:
    """
    Extract em_imaging_optics data from a CETS region.
    
    Args:
        region: CETS region dictionary
        
    Returns:
        EmImagingOptics model instance
    """
    region_id = region.get("id", "1")
    
    # Optics data is typically not in CETS
    return EmImagingOptics(
        id=f"{region_id}_1",  # TODO: ptics ID convention...?
        imaging_id=region_id,
        energyfilter_name=None,
        phase_plate=None,
        # All other fields default to None
    )
