from typing import Dict, Any
from cets_mmcif.models.categories import EmExperiment


def extract_em_experiment(
    region: Dict[str, Any],
    dataset_name: str,
    region_index: int
) -> EmExperiment:
    return EmExperiment(
        entry_id=dataset_name,
        id=region_index,
        reconstruction_method="TOMOGRAPHY",
        aggregation_state=None,
        entity_assembly_id=None
    )
