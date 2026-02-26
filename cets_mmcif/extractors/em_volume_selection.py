from typing import Dict, Any, Optional
from cets_mmcif.models.categories import EmVolumeSelection


def extract_em_volume_selection(
    region: Dict[str, Any],
    region_index: int
) -> Optional[EmVolumeSelection]:
    tomograms = region.get("tomograms", [])
    num_tomograms = len(tomograms) if tomograms else None

    return EmVolumeSelection(
        id=region_index,
        image_processing_id=region_index,
        num_tomograms=num_tomograms,
        method=None,
        num_volumes_extracted=None,
        reference_model=None,
        details=None
    )
