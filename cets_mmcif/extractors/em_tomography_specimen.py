from cets_mmcif.models.categories import EmTomographySpecimen


def extract_em_tomography_specimen(
    region_index: int
) -> EmTomographySpecimen:
    """
    Extract em_tomography_specimen data from a CETS region.
    
    Args:
        region_index: CETS region index
        
    Returns:
        EmTomographySpecimen model instance
 
    Note:
        Specimen preparation data is not available in CETS — all preparation
        fields (sectioning, fiducial_markers, high_pressure_freezing) are None.
        These should be supplied via a definition file.
 
        specimen_id is a mandatory foreign key to em_specimen (id=1).
        Hardcoded to "1" as a conventional placeholder.
    """
    return EmTomographySpecimen(
        id=region_index,
        specimen_id="1",  # Mandatory key to em_specimen.id — hardcoded placeholder
        fiducial_markers=None,
        sectioning=None,
        high_pressure_freezing=None,
        cryo_protectant=None,
        details=None
    )
