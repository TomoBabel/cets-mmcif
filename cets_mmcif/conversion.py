import gemmi
import json
from pathlib import Path

from cets_mmcif.extractors import (
    extract_em_experiment,
    extract_em_imaging,
    extract_em_tomography,
    extract_em_imaging_optics,
    extract_em_tomography_specimen,
    extract_em_image_recording,
    extract_em_image_processing,
    extract_em_3d_reconstruction,
    extract_em_software,
    extract_em_map,
)
from cets_mmcif.serialisers.mmcif_serialiser import serialize_category
from cets_mmcif.utilities import add_category_separators


def convert_cets_to_mmcif(
    cets_input_path: Path,
    mmcif_output_path: Path
):
    """Convert CETS JSON to mmCIF using extractors and serializers."""
    
    # Load CETS data
    with open(cets_input_path, "r") as f:
        cets_data = json.load(f)
    
    dataset_name = cets_data.get("name", "unknown")
    regions = cets_data.get("regions", [])
    
    # Create mmCIF document
    doc = gemmi.cif.Document()
    block = doc.add_new_block(dataset_name)
    
    # Add metadata
    block.set_pair("_entry.id", dataset_name)
    block.set_pair("_audit_conform.dict_name", "mmcif_pdbx.dic")
    block.set_pair("_audit_conform.dict_version", "5.409")
    block.set_pair("_audit_conform.dict_location",
                   "http://mmcif.pdb.org/dictionaries/ascii/mmcif_pdbx.dic")
    
    # em_experiment
    experiments = [extract_em_experiment(r, dataset_name) for r in regions]
    serialize_category(block, experiments)
    
    # em_imaging
    imaging_data = [extract_em_imaging(r, dataset_name) for r in regions]
    imaging_data = [i for i in imaging_data if i is not None]
    serialize_category(block, imaging_data)
    
    # em_tomography
    tomography_data = [extract_em_tomography(r) for r in regions]
    tomography_data = [t for t in tomography_data if t is not None]
    serialize_category(block, tomography_data)
    
    # em_imaging_optics
    optics_data = [extract_em_imaging_optics(r) for r in regions]
    serialize_category(block, optics_data)
    
    # em_tomography_specimen
    specimen_data = [extract_em_tomography_specimen(r) for r in regions]
    serialize_category(block, specimen_data)
    
    # em_image_recording
    recording_data = [extract_em_image_recording(r) for r in regions]
    serialize_category(block, recording_data)
    
    # em_image_processing
    processing_data = [extract_em_image_processing(r) for r in regions]
    serialize_category(block, processing_data)
    
    # em_3d_reconstruction
    reconstruction_data = [extract_em_3d_reconstruction(r, dataset_name) for r in regions]
    reconstruction_data = [rc for rc in reconstruction_data if rc is not None]
    serialize_category(block, reconstruction_data)
    
    # em_software
    software_data = [extract_em_software(r) for r in regions]
    serialize_category(block, software_data)
    
    # em_map
    map_data = [extract_em_map(r, dataset_name) for r in regions]
    map_data = [m for m in map_data if m is not None]
    serialize_category(block, map_data)
    
    # Get mmCIF string and add separators
    mmcif_string = doc.as_string()
    mmcif_string = add_category_separators(mmcif_string)
    
    # Write to file
    mmcif_output_path.mkdir(parents=True, exist_ok=True)
    mmcif_output_file = mmcif_output_path / f"{dataset_name}.cif"
    with open(mmcif_output_file, "w") as f:
        f.write(mmcif_string)
    
    print(f"Written mmCIF file: {mmcif_output_file}")
