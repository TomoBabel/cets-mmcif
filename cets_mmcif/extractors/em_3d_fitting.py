from typing import Dict, Any, Optional
from cets_mmcif.models.categories import Em3dFitting


def extract_em_3d_fitting(
    region: Dict[str, Any],
    dataset_name: str,
    region_index: int
) -> Optional[Em3dFitting]:
    """
    Extract em_3d_fitting data.

    Note:
        3D fitting data (atomic model fitting) not in CETS.
        Returns None — can be populated from a definition file.
    """
    return None
