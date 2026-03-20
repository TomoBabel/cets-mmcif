from typing import Dict, Any, List
from cets_mmcif.models.categories import Em3dFittingList


def extract_em_3d_fitting_list(
    region: Dict[str, Any],
    region_index: int
) -> List[Em3dFittingList]:
    """
    Extract em_3d_fitting_list data.

    Note:
        Fitting list (fitted atomic models) not in CETS.
        Returns empty list — can be populated from a definition file.
    """
    return []
