from typing import Dict, Any, Optional
from cets_mmcif.models.categories import EmVolumeSelection


def extract_em_volume_selection(
    region: Dict[str, Any]
) -> Optional[EmVolumeSelection]:
    """
    Extract em_volume_selection data.
    
    Args:
        region: CETS region dictionary
        
    Returns:
        EmVolumeSelection model instance, or None if not applicable
    
    Note:
        Volume selection is typically for subtomogram averaging...
        Most data not in CETS - can be populated from definition file?
    """
    region_id = region.get("id", "1")
    
    # Get number of tomograms
    tomograms = region.get("tomograms", [])
    num_tomograms = len(tomograms) if tomograms else None
    
    return EmVolumeSelection(
        id=f"{region_id}_volume_selection_1",
        image_processing_id=f"{region_id}_processing",
        num_tomograms=num_tomograms,
        method=None,
        num_volumes_extracted=None,
        reference_model=None,
        details=None
    )
