from typing import Dict, Any
from cets_mmcif.models.categories import EmTomographySpecimen


def extract_em_tomography_specimen(region: Dict[str, Any]) -> EmTomographySpecimen:
    """
    Extract em_tomography_specimen data from a CETS region.
    
    Args:
        region: CETS region dictionary
        
    Returns:
        EmTomographySpecimen model instance
    """
    region_id = region.get("id", "1")
    
    # TODO: this file is a placeholder, for more information
    # since specimen preparation data is not in CETS
    # could use some sort of definition/proposal file?
    return EmTomographySpecimen(
        id=region_id,
        specimen_id=None,
        fiducial_markers=None,
        sectioning=None,
        high_pressure_freezing=None,
        cryo_protectant=None,
        details=None
    )
