import gemmi
import json
import logging
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
    extract_em_3d_fitting,
    extract_em_3d_fitting_list,
)
from cets_mmcif.serialisers.mmcif_serialiser import serialize_category
from cets_mmcif.utilities import add_category_separators

logger = logging.getLogger(__name__)


def convert_cets_to_mmcif(
    cets_input_path: Path,
    mmcif_output_path: Path
):
    """Convert CETS JSON to mmCIF using extractors and serializers."""

    with open(cets_input_path, "r") as f:
        cets_data = json.load(f)

    dataset_name = cets_data.get("name", "unknown")
    regions = cets_data.get("regions", [])

    doc = gemmi.cif.Document()
    block = doc.add_new_block(dataset_name)

    block.set_pair("_entry.id", dataset_name)
    block.set_pair("_audit_conform.dict_name", "mmcif_pdbx.dic")
    block.set_pair("_audit_conform.dict_version", "5.409")
    block.set_pair("_audit_conform.dict_location",
                   "http://mmcif.pdb.org/dictionaries/ascii/mmcif_pdbx.dic")

    experiments = []
    imaging_data = []
    tomography_data = []
    optics_data = []
    specimen_data = []
    recording_data = []
    processing_data = []
    reconstruction_data = []
    software_data = []
    map_data = []
    fitting_data = []
    fitting_list_data = []

    for region_index, region in enumerate(regions, start=1):
        experiments.append(extract_em_experiment(region, dataset_name, region_index))

        imaging = extract_em_imaging(region, dataset_name, region_index)
        if imaging:
            imaging_data.append(imaging)

        tomography = extract_em_tomography(region, region_index)
        if tomography:
            tomography_data.append(tomography)

        optics_data.append(extract_em_imaging_optics(region, region_index))
        specimen_data.append(extract_em_tomography_specimen(region, region_index))
        recording_data.append(extract_em_image_recording(region, region_index))
        processing_data.append(extract_em_image_processing(region, region_index))

        reconstruction = extract_em_3d_reconstruction(region, dataset_name, region_index)
        if reconstruction:
            reconstruction_data.append(reconstruction)

        software_data.append(extract_em_software(region, region_index))

        map_item = extract_em_map(region, dataset_name, region_index)
        if map_item:
            map_data.append(map_item)

        fitting = extract_em_3d_fitting(region, dataset_name, region_index)
        if fitting:
            fitting_data.append(fitting)

        fitting_list_data.extend(extract_em_3d_fitting_list(region, region_index))

    serialize_category(block, experiments)
    serialize_category(block, imaging_data)
    serialize_category(block, tomography_data)
    serialize_category(block, optics_data)
    serialize_category(block, specimen_data)
    serialize_category(block, recording_data)
    serialize_category(block, processing_data)
    serialize_category(block, reconstruction_data)
    serialize_category(block, software_data)
    serialize_category(block, map_data)
    serialize_category(block, fitting_data)
    serialize_category(block, fitting_list_data)

    mmcif_string = doc.as_string()
    mmcif_string = add_category_separators(mmcif_string)

    mmcif_output_path.mkdir(parents=True, exist_ok=True)
    mmcif_output_file = mmcif_output_path / f"{dataset_name}.cif"
    with open(mmcif_output_file, "w") as f:
        f.write(mmcif_string + "\n")

    logger.info(f"Written mmCIF file: {mmcif_output_file}")
