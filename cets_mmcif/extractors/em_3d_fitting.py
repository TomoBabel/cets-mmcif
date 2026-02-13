from typing import Dict, Any
from cets_mmcif.models.categories import Em3dFitting


def extract_em_3d_fitting(
    region: Dict[str, Any],
    dataset_name: str
) -> Em3dFitting:
    """
    Extract em_3d_fitting data.
    
    Args:
        region: CETS region dictionary
        dataset_name: Entry ID for the dataset
        
    Returns:
        Em3dFitting model instance
    
    Note:
        3D fitting data (atomic model fitting) not in CETS.
        Can be populated from definition file.
    """
    region_id = region.get("id", "1")
    
    return Em3dFitting(
        id=f"{region_id}_fitting_1",
        entry_id=dataset_name,
        method=None,
        target_criteria=None,
        software_name=None,
        details=None,
        overall_b_value=None,
        ref_space=None,
        ref_protocol=None,
        initial_refinement_model_id=None
    )
