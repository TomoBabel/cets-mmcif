from typing import Dict, Any, Optional
from cets_mmcif.models.categories import EmImaging


def extract_em_imaging(
    region: Dict[str, Any],
    dataset_name: str,
    region_index: int
) -> Optional[EmImaging]:
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

    tilt_angle_min = min(tilt_angles) if tilt_angles else None
    tilt_angle_max = max(tilt_angles) if tilt_angles else None

    return EmImaging(
        entry_id=dataset_name,
        id=region_index,
        mode="BRIGHT FIELD",
        tilt_angle_min=tilt_angle_min,
        tilt_angle_max=tilt_angle_max,
        accelerating_voltage=None,
        illumination_mode=None,
        specimen_id=None,
    )
