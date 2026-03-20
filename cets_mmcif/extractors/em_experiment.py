from cets_mmcif.models.categories import EmExperiment


# Valid OneDep values for aggregation_state:
# CELL, FILAMENT, PARTICLE, TISSUE, ORGANELLE
# For cryo-ET tomography datasets, CELL is the most common default.
# This should be overridden, e.g., via a definition file for non-cell specimens.
_DEFAULT_AGGREGATION_STATE = "CELL"


def extract_em_experiment(
    dataset_name: str,
    region_index: int
) -> EmExperiment:
    """
    Extract em_experiment data from a CETS region.
    
    Args:
        dataset_name: Entry ID for the dataset
        region_index: Index of the region within the dataset
        
    Returns:
        EmExperiment model instance
    
    Note:
        aggregation_state is mandatory for OneDep but not available in CETS.
        Defaults to CELL (typical for cryo-ET). Override via definition file
        for PARTICLE (subtomogram averaging) or FILAMENT datasets.

        entity_assembly_id is a foreign key to em_entity_assembly (id=1).
        "1" is hardcoded as a conventional placeholder since 
        em_entity_assembly is not yet generated from CETS data.
    """

    return EmExperiment(
        entry_id=dataset_name,
        id=region_index,
        reconstruction_method="TOMOGRAPHY",
        aggregation_state=_DEFAULT_AGGREGATION_STATE,
        entity_assembly_id="1"  # Placeholder foreign key to em_entity_assembly.id
    )
