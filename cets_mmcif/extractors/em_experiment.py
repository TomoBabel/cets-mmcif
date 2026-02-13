from typing import Dict, Any
from cets_mmcif.models.categories import EmExperiment


def extract_em_experiment(
    region: Dict[str, Any],
    dataset_name: str
) -> EmExperiment:
    """
    Extract em_experiment data from a CETS region.
    
    Args:
        region: CETS region dictionary
        dataset_name: Entry ID for the dataset
        
    Returns:
        EmExperiment model instance
    """
    region_id = region.get("id", "1")
    
    # TODO: Detect reconstruction method from CETS if available
    # For tomography datasets — "TOMOGRAPHY"?
    
    return EmExperiment(
        entry_id=dataset_name,
        id=region_id,
        reconstruction_method="TOMOGRAPHY",
        aggregation_state=None,  # Not in CETS
        specimen_type=None,  # Deprecated field
        entity_assembly_id=None  # Not in CETS
    )
