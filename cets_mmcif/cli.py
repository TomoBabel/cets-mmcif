import logging
import typer
from pathlib import Path
from rich.logging import RichHandler
from typing import Annotated, Optional

from cets_mmcif import conversion, validation, settings


cets_mmcif = typer.Typer()

logging.basicConfig(
    level=logging.INFO,
    format="%(name)s - %(asctime)s - %(levelname)s - %(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger(__name__)

settings = settings.get_settings()


@cets_mmcif.command("convert")
def convert_cets_to_mmcif(
    cets_input_path: Annotated[
        Path, 
        typer.Option(
            "--cets-input", 
            "-i", 
            case_sensitive=False, 
            help="Path to input CETS JSON file."
        )
    ], 
    mmcif_output_path: Annotated[
        Optional[Path], 
        typer.Option(
            "--mmcif-output", 
            "-o", 
            case_sensitive=False, 
            help="Path for output mmCIF directory. Default is output-data/cets-mmcif."
        )
    ] = settings.output_mmcif_directory
):
    """
    Convert a CETS dataset to mmCIF format.

    Args:
        cets_input_path: Path to input CETS JSON file
        mmcif_output_path: Path for output mmCIF directory
    """
    
    conversion.convert_cets_to_mmcif(
        cets_input_path=cets_input_path,
        mmcif_output_path=mmcif_output_path
    )
    
    logger.info("Conversion complete")


@cets_mmcif.command("validate")
def validate_mmcif(
    mmcif_file: Annotated[
        Path, 
        typer.Option(
            "--mmcif-file", 
            "-f", 
            case_sensitive=False, 
            help="Path to the mmCIF file to validate."
        )
    ], 
    validation_dict_path: Annotated[
        Optional[Path], 
        typer.Option(
            "--dict-file", 
            "-d", 
            case_sensitive=False, 
            help="Path to the mmCIF dictionary file for validation."
        )
    ] = settings.validation_dictionary_path
):
    """
    Validate an mmCIF file using Gemmi's validation.
    """
    
    if not mmcif_file.exists():
        logger.error(f"mmCIF file not found: {mmcif_file}")
        raise typer.Exit(code=1)
    
    if not validation_dict_path or not validation_dict_path.exists():
        logger.error(f"Dictionary file not found: {validation_dict_path}")
        raise typer.Exit(code=1)
    
    logger.info(f"Validating mmCIF file: {mmcif_file}")
    logger.info(f"Using dictionary: {validation_dict_path}")
    
    is_valid, errors = validation.mmcif_validation(mmcif_file, validation_dict_path)
    
    if is_valid:
        logger.info("Validation passed.")
    else:
        logger.error("Validation failed.")
        for error in errors:
            logger.error(error)
