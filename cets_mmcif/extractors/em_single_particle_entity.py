from typing import Dict, Any
from cets_mmcif.models.categories import EmSingleParticleEntity


def extract_em_single_particle_entity(
    region: Dict[str, Any],
    dataset_name: str
) -> EmSingleParticleEntity:
    """
    Extract em_single_particle_entity data.
    
    Args:
        region: CETS region dictionary
        dataset_name: Entry ID for the dataset
        
    Returns:
        EmSingleParticleEntity model instance
    
    Note:
        - can be populated from definition file or if CETS allows.
    """
    region_id = region.get("id", "1")
    
    return EmSingleParticleEntity(
        entry_id=dataset_name,
        id=f"{region_id}_entity_1",
        image_processing_id=f"{region_id}_processing",
        symmetry_type=None,
        point_symmetry=None
    )
