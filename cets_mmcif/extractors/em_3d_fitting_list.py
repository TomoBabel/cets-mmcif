from typing import Dict, Any, List
from cets_mmcif.models.categories import Em3dFittingList


def extract_em_3d_fitting_list(
    region: Dict[str, Any]
) -> List[Em3dFittingList]:
    """
    Extract em_3d_fitting_list data.
    
    Args:
        region: CETS region dictionary
        
    Returns:
        List of Em3dFittingList model instances (empty if no fitting data)
    
    Note:
        Fitting list (fitted atomic models) not in CETS.
        Can be populated from definition file.
    """
    # TODO: This category typically has multiple entries (one per fitted model)
    # Since CETS doesn't contain this data, return empty list
    # Can be populated from a definition file with multiple entries
    return []
