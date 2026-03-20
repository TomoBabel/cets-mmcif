from typing import Dict, Any, Optional
from cets_mmcif.models.categories import EmTomography


def extract_em_tomography(
    region: Dict[str, Any],
    region_index: int
) -> Optional[EmTomography]:
    tilt_series_list = region.get("tilt_series", [])
    if not tilt_series_list:
        return None

    tilt_series = tilt_series_list[0]
    images = tilt_series.get("images", [])
    if not images:
        return None

    tilt_angles = [
        img.get("nominal_tilt_angle", 0)
        for img in images
        if img.get("nominal_tilt_angle") is not None
    ]
    if not tilt_angles:
        return None

    axis1_min = min(tilt_angles)
    axis1_max = max(tilt_angles)

    if len(tilt_angles) > 1:
        sorted_angles = sorted(set(tilt_angles))
        increments = [sorted_angles[i+1] - sorted_angles[i]
                      for i in range(len(sorted_angles)-1)]
        axis1_increment = sum(increments) / len(increments) if increments else None
    else:
        axis1_increment = None

    return EmTomography(
        id=region_index,
        imaging_id=region_index,
        axis1_min_angle=axis1_min,
        axis1_max_angle=axis1_max,
        axis1_angle_increment=axis1_increment,
        axis2_min_angle=None,
        axis2_max_angle=None,
        axis2_angle_increment=None,
        dual_tilt_axis_rotation=None
    )
