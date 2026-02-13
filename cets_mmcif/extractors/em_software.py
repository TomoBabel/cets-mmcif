from typing import Dict, Any
from cets_mmcif.models.categories import EmSoftware


def extract_em_software(region: Dict[str, Any]) -> EmSoftware:
    """
    Extract em_software data from a CETS region.
    
    Args:
        region: CETS region dictionary
        
    Returns:
        EmSoftware model instance
    """
    region_id = region.get("id", "1")
    
    # TODO: another placeholder, 
    # since software information is not in CETS
    return EmSoftware(
        id=f"{region_id}_software_1",
        name=None,
        category="RECONSTRUCTION",  # Default category
        image_processing_id=f"{region_id}_processing",
        version=None,
        details=None
    )
