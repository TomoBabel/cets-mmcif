from pydantic import BaseModel
from typing import Optional


class EmExperiment(BaseModel):
    """Data model for _em_experiment category."""
    
    entry_id: str
    id: str
    reconstruction_method: str
    aggregation_state: Optional[str] = None
    specimen_type: Optional[str] = None
    entity_assembly_id: Optional[str] = None


class EmImaging(BaseModel):
    """Data model for _em_imaging category."""
    
    entry_id: str
    id: str
    astigmatism: Optional[str] = None
    electron_beam_tilt_params: Optional[str] = None
    residual_tilt: Optional[float] = None
    sample_support_id: Optional[str] = None
    detector_id: Optional[str] = None
    scans_id: Optional[str] = None
    microscope_id: Optional[str] = None
    microscope_model: Optional[str] = None
    specimen_holder_type: Optional[str] = None
    specimen_holder_model: Optional[str] = None
    details: Optional[str] = None
    date: Optional[str] = None
    accelerating_voltage: Optional[float] = None
    illumination_mode: Optional[str] = None
    mode: Optional[str] = None
    nominal_cs: Optional[float] = None
    nominal_defocus_min: Optional[float] = None
    nominal_defocus_max: Optional[float] = None
    calibrated_defocus_min: Optional[float] = None
    calibrated_defocus_max: Optional[float] = None
    tilt_angle_min: Optional[float] = None
    tilt_angle_max: Optional[float] = None
    nominal_magnification: Optional[int] = None
    calibrated_magnification: Optional[int] = None
    electron_source: Optional[str] = None
    electron_dose: Optional[float] = None
    energy_filter: Optional[str] = None
    energy_window: Optional[float] = None
    citation_id: Optional[str] = None
    temperature: Optional[float] = None
    detector_distance: Optional[float] = None
    recording_temperature_minimum: Optional[float] = None
    recording_temperature_maximum: Optional[float] = None
    alignment_procedure: Optional[str] = None
    c2_aperture_diameter: Optional[float] = None
    specimen_id: Optional[str] = None
    cryogen: Optional[str] = None
    objective_aperture: Optional[float] = None
    microscope_serial_number: Optional[str] = None
    microscope_version: Optional[str] = None


class EmTomography(BaseModel):
    """Data model for _em_tomography category."""
    
    axis1_angle_increment: Optional[float] = None
    axis1_max_angle: Optional[float] = None
    axis1_min_angle: Optional[float] = None
    axis2_angle_increment: Optional[float] = None
    axis2_max_angle: Optional[float] = None
    axis2_min_angle: Optional[float] = None
    dual_tilt_axis_rotation: Optional[float] = None
    id: str
    imaging_id: str


class EmImagingOptics(BaseModel):
    """Data model for _em_imaging_optics category."""
    
    chr_aberration_corrector: Optional[str] = None
    energyfilter_lower: Optional[float] = None
    energyfilter_slit_width: Optional[float] = None
    energyfilter_name: Optional[str] = None
    energyfilter_upper: Optional[float] = None
    id: str
    imaging_id: str
    phase_plate: Optional[str] = None
    sph_aberration_corrector: Optional[str] = None
    details: Optional[str] = None


class EmTomographySpecimen(BaseModel):
    """Data model for _em_tomography_specimen category."""
    
    cryo_protectant: Optional[str] = None
    details: Optional[str] = None
    fiducial_markers: Optional[str] = None
    high_pressure_freezing: Optional[str] = None
    id: str
    sectioning: Optional[str] = None
    specimen_id: Optional[str] = None


class EmFocusedIonBeam(BaseModel):
    """Data model for _em_focused_ion_beam category."""
    
    current: Optional[float] = None
    details: Optional[str] = None
    dose_rate: Optional[float] = None
    duration: Optional[float] = None
    em_tomography_specimen_id: Optional[str] = None
    final_thickness: Optional[float] = None
    id: str
    initial_thickness: Optional[float] = None
    instrument: Optional[str] = None
    ion: Optional[str] = None
    temperature: Optional[float] = None
    voltage: Optional[float] = None


class EmImageRecording(BaseModel):
    """Data model for _em_image_recording category."""
    
    id: str
    imaging_id: str
    average_exposure_time: Optional[float] = None
    avg_electron_dose_per_subtomogram: Optional[float] = None
    avg_electron_dose_per_image: Optional[float] = None
    details: Optional[str] = None
    detector_mode: Optional[str] = None
    film_or_detector_model: Optional[str] = None
    num_diffraction_images: Optional[int] = None
    num_grids_imaged: Optional[int] = None
    num_real_images: Optional[int] = None


class EmImageProcessing(BaseModel):
    """Data model for _em_image_processing category."""
    
    id: str
    image_recording_id: str
    details: Optional[str] = None


class EmVolumeSelection(BaseModel):
    """Data model for _em_volume_selection category."""
    
    details: Optional[str] = None
    id: str
    image_processing_id: str
    method: Optional[str] = None
    num_tomograms: Optional[int] = None
    num_volumes_extracted: Optional[int] = None
    reference_model: Optional[str] = None


class EmCtfCorrection(BaseModel):
    """Data model for _em_ctf_correction category."""
    
    id: str
    amplitude_correction: Optional[str] = None
    amplitude_correction_factor: Optional[float] = None
    amplitude_correction_space: Optional[str] = None
    correction_operation: Optional[str] = None
    details: Optional[str] = None
    em_image_processing_id: Optional[str] = None
    phase_reversal: Optional[str] = None
    phase_reversal_anisotropic: Optional[str] = None
    phase_reversal_correction_space: Optional[str] = None
    type: Optional[str] = None


class EmEulerAngleAssignment(BaseModel):
    """Data model for _em_euler_angle_assignment category."""
    
    details: Optional[str] = None
    id: str
    image_processing_id: str
    order: Optional[str] = None
    proj_matching_angular_sampling: Optional[float] = None
    proj_matching_merit_function: Optional[str] = None
    proj_matching_num_projections: Optional[int] = None
    type: Optional[str] = None


class EmFinalClassification(BaseModel):
    """Data model for _em_final_classification category."""
    
    avg_num_images_per_class: Optional[int] = None
    details: Optional[str] = None
    id: str
    image_processing_id: str
    num_classes: Optional[int] = None
    type: Optional[str] = None


class Em3dReconstruction(BaseModel):
    """Data model for _em_3d_reconstruction category."""
    
    entry_id: str
    id: str
    method: Optional[str] = None
    algorithm: Optional[str] = None
    citation_id: Optional[str] = None
    details: Optional[str] = None
    resolution: Optional[float] = None
    resolution_method: Optional[str] = None
    magnification_calibration: Optional[str] = None
    ctf_correction_method: Optional[str] = None
    nominal_pixel_size: Optional[float] = None
    actual_pixel_size: Optional[float] = None
    num_particles: Optional[int] = None
    euler_angles_details: Optional[str] = None
    num_class_averages: Optional[int] = None
    software: Optional[str] = None
    fsc_type: Optional[str] = None
    refinement_type: Optional[str] = None
    image_processing_id: Optional[str] = None
    symmetry_type: Optional[str] = None


class EmSingleParticleEntity(BaseModel):
    """Data model for _em_single_particle_entity category."""
    
    entry_id: str
    id: str
    symmetry_type: Optional[str] = None
    image_processing_id: Optional[str] = None
    point_symmetry: Optional[str] = None


class Em3dFitting(BaseModel):
    """Data model for _em_3d_fitting category."""
    
    id: str
    entry_id: str
    method: Optional[str] = None
    target_criteria: Optional[str] = None
    software_name: Optional[str] = None
    details: Optional[str] = None
    overall_b_value: Optional[float] = None
    ref_space: Optional[str] = None
    ref_protocol: Optional[str] = None
    initial_refinement_model_id: Optional[str] = None


class Em3dFittingList(BaseModel):
    """Data model for _em_3d_fitting_list category."""
    
    id: str
    fitting_id: str  # Note: field name is "3d_fitting_id" but can't start with digit — see config mapping below
    pdb_entry_id: Optional[str] = None
    pdb_chain_id: Optional[str] = None
    pdb_chain_residue_range: Optional[str] = None
    details: Optional[str] = None
    chain_id: Optional[str] = None
    chain_residue_range: Optional[str] = None
    source_name: Optional[str] = None
    type: Optional[str] = None
    accession_code: Optional[str] = None
    initial_refinement_model_id: Optional[str] = None
    
    class Config:
        # Map the Python field name to mmCIF field name
        fields = {
            "fitting_id": "3d_fitting_id"
        }


class EmSoftware(BaseModel):
    """Data model for _em_software category."""
    
    category: Optional[str] = None
    details: Optional[str] = None
    id: str
    image_processing_id: Optional[str] = None
    fitting_id: Optional[str] = None
    imaging_id: Optional[str] = None
    name: Optional[str] = None
    version: Optional[str] = None
    reference_DOI: Optional[str] = None


class EmMap(BaseModel):
    """Data model for _em_map category."""
    
    annotation_details: Optional[str] = None
    axis_order_fast: Optional[str] = None
    axis_order_medium: Optional[str] = None
    axis_order_slow: Optional[str] = None
    cell_a: Optional[float] = None
    cell_b: Optional[float] = None
    cell_c: Optional[float] = None
    cell_alpha: Optional[float] = None
    cell_beta: Optional[float] = None
    cell_gamma: Optional[float] = None
    contour_level: Optional[float] = None
    contour_level_source: Optional[str] = None
    data_type: Optional[str] = None
    dimensions_col: Optional[int] = None
    dimensions_row: Optional[int] = None
    dimensions_sec: Optional[int] = None
    endian_type: Optional[str] = None
    file: Optional[str] = None
    original_file: Optional[str] = None
    format: Optional[str] = None
    id: str
    partition: Optional[int] = None
    entry_id: Optional[str] = None
    label: Optional[str] = None
    limit_col: Optional[int] = None
    limit_row: Optional[int] = None
    limit_sec: Optional[int] = None
    origin_col: Optional[int] = None
    origin_row: Optional[int] = None
    origin_sec: Optional[int] = None
    pixel_spacing_x: Optional[float] = None
    pixel_spacing_y: Optional[float] = None
    pixel_spacing_z: Optional[float] = None
    size_kb: Optional[int] = None
    spacing_x: Optional[float] = None
    spacing_y: Optional[float] = None
    spacing_z: Optional[float] = None
    statistics_average: Optional[float] = None
    statistics_maximum: Optional[float] = None
    statistics_minimum: Optional[float] = None
    statistics_std: Optional[float] = None
    symmetry_space_group: Optional[int] = None
    type: Optional[str] = None


class EmImageScans(BaseModel):
    """Data model for _em_image_scans category."""
    
    entry_id: str
    id: str
    number_digital_images: Optional[int] = None
    details: Optional[str] = None
    scanner_model: Optional[str] = None
    sampling_size: Optional[float] = None
    od_range: Optional[float] = None
    quant_bit_size: Optional[int] = None
    citation_id: Optional[str] = None
    dimension_height: Optional[int] = None
    dimension_width: Optional[int] = None
    frames_per_image: Optional[int] = None
    image_recording_id: Optional[str] = None
    used_frames_per_image: Optional[int] = None
