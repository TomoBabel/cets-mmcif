import json
import logging
from pathlib import Path
from typing import Dict, Any

from cets_mmcif.entities import (
    experiment, 
    image_processing, 
    image_recording, 
    imaging, 
    imaging_optics, 
    map, 
    reconstruction, 
    software, 
    tomography,  
    tomography_specimen
)

logger = logging.getLogger(__name__)


def convert_cets_to_mmcif(
    cets_input_path: Path,
    mmcif_output_path: Path
) -> None:
    """
    Convert a CETS JSON dataset to mmCIF format.
    
    Args:
        cets_input_path: Path to input CETS JSON file
        mmcif_output_path: Path for output mmCIF file
    """
    with open(cets_input_path, 'r') as f:
        cets_data = json.load(f)
    
    logger.info(f"Loaded CETS dataset: {cets_data.get('name', 'Unknown')}")
    
    mmcif_content = generate_mmcif_from_cets(cets_data)
    
    mmcif_output_path.mkdir(parents=True, exist_ok=True)
    mmcif_output_filepath = mmcif_output_path / f"{cets_data.get('name', 'output')}.cif"

    with open(mmcif_output_filepath, 'w') as f:
        f.write(mmcif_content)
    
    logger.info(f"Written mmCIF file: {mmcif_output_filepath}")


def generate_mmcif_from_cets(cets_data: Dict[str, Any]) -> str:
    """
    Generate mmCIF content from CETS dataset.
    
    This function now properly handles multiple regions by generating
    one loop per category with multiple data rows.
    
    Args:
        cets_data: Parsed CETS JSON data
        
    Returns:
        mmCIF formatted string
    """
    mmcif_lines = []
    
    dataset_name = cets_data.get('name', 'unknown')
    mmcif_lines.append(f"data_{dataset_name}")
    mmcif_lines.append("#")
    
    regions = cets_data.get('regions', [])
    logger.info(f"Processing {len(regions)} region(s)")
    
    mmcif_lines.extend(experiment.generate_em_experiment(regions))
    mmcif_lines.extend(imaging.generate_em_imaging(regions))
    mmcif_lines.extend(tomography.generate_em_tomography(regions))
    mmcif_lines.extend(imaging_optics.generate_em_imaging_optics(regions))
    mmcif_lines.extend(tomography_specimen.generate_em_tomography_specimen(regions))
    mmcif_lines.extend(image_recording.generate_em_image_recording(regions))
    mmcif_lines.extend(image_processing.generate_em_image_processing(regions))
    mmcif_lines.extend(reconstruction.generate_em_3d_reconstruction(regions))
    mmcif_lines.extend(software.generate_em_software(regions))
    mmcif_lines.extend(map.generate_em_map(regions))
    
    return '\n'.join(mmcif_lines) + '\n'
