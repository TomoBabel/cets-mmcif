from cets_mmcif.models.categories import EmSpecimen


def extract_em_specimen(
    region_index: int
) -> EmSpecimen:
    """
    Extract em_specimen data from a CETS region.

    Args:
        region_index: CETS region index

    Returns:
        EmSpecimen model instance

    Note:
        Specimen preparation metadata is not available in CETS.
        The boolean flags (embedding_applied, shadowing_applied,
        staining_applied, vitrification_applied) are hardcoded to
        the values universal across all cryo-ET depositions:
        vitrification is always applied; embedding, shadowing, and
        staining are never applied in cryo-ET workflows.

        experiment_id is a foreign key to em_experiment.id.
    """
    return EmSpecimen(
        id="1",
        experiment_id=region_index,
        concentration=None,
        embedding_applied=False,
        shadowing_applied=False,
        staining_applied=False,
        vitrification_applied=True,
        details=None,
    )