from typing import Dict, Any
from cets_mmcif.models.categories import EmSingleParticleEntity


def extract_em_single_particle_entity(
    region: Dict[str, Any],
    dataset_name: str,
    region_index: int
) -> EmSingleParticleEntity:
    return EmSingleParticleEntity(
        entry_id=dataset_name,
        id=region_index,
        image_processing_id=region_index,
        symmetry_type=None,
        point_symmetry=None
    )
