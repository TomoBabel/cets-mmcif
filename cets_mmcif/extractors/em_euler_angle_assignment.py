from typing import Dict, Any
from cets_mmcif.models.categories import EmEulerAngleAssignment


def extract_em_euler_angle_assignment(
    region: Dict[str, Any],
    region_index: int
) -> EmEulerAngleAssignment:
    return EmEulerAngleAssignment(
        id=region_index,
        image_processing_id=region_index,
        type=None,
        order=None,
        proj_matching_num_projections=None,
        proj_matching_angular_sampling=None,
        proj_matching_merit_function=None,
        details=None
    )
