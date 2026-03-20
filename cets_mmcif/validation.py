import gemmi
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple
from validate_mmcif import validate as pdbe_validate
from validate_mmcif import DictionaryNotFoundError, CifNotFoundError

logger = logging.getLogger(__name__)


def _validation_logger_callback(messages: List[str]):
    """
    Create a logger callback that appends messages to a list.

    Args:
        messages: List to append validation messages to

    Returns:
        Callback function for gemmi's Ddl validator
    """
    def callback(msg: str):
        messages.append(msg)
    return callback


def mmcif_validation(
    mmcif_file: Path,
    dict_file: Path,
) -> Tuple[bool, List[str]]:
    """
    Validate an mmCIF file against a dictionary using gemmi.

    Args:
        mmcif_file: Path to the mmCIF file to validate
        dict_file: Path to the mmCIF dictionary file (e.g., mmcif_pdbx.dic)

    Returns:
        Tuple of (is_valid, list of error/warning messages)
    """
    messages = []
    validation_logger = _validation_logger_callback(messages)

    try:
        doc = gemmi.cif.read_file(str(mmcif_file))
        dict_doc = gemmi.cif.read_file(str(dict_file))

        ddl = gemmi.cif.Ddl(
            validation_logger,
            print_unknown_tags=True,
            use_regex=True,
            use_context=True,
            use_linked_groups=True,
            use_mandatory=True,
            use_unique_keys=True,
        )

        ddl.read_ddl(dict_doc)
        is_valid = ddl.validate_cif(doc)

        if not is_valid and not messages:
            messages.append("Validation failed with no specific error messages.")

        return is_valid, messages

    except Exception as e:
        return False, [f"Full validation not attempted, due to error: {str(e)}"]


@dataclass
class PdbeValidationIssue:
    """A single issue reported by the PDBe mmCIF validator."""
    line: int
    item: str
    message: str
    severity: str  # "error" or "warning"


def pdbe_mmcif_validation(
    mmcif_file: Path,
    dict_file: Path,
) -> Tuple[bool, List[PdbeValidationIssue]]:
    """
    Validate an mmCIF file using the PDBe standalone mmCIF validator
    (pdbe-mmcif-validator).

    This validator performs deeper deposition-readiness checks than gemmi,
    including foreign key integrity, enumeration validation, composite key
    validation, and data type checking against the mmCIF dictionary.

    Args:
        mmcif_file: Path to the mmCIF file to validate
        dict_file: Path to the mmCIF dictionary file

    Returns:
        Tuple of (is_valid, list of PdbeValidationIssue).
        is_valid is True when there are no issues with severity "error".
        Warnings are included in the issue list but do not affect is_valid.

    Raises:
        ImportError: if pdbe-mmcif-validator is not installed. Install with:
            poetry add --group dev pdbe-mmcif-validator
            (and comment out the metadata_completeness import in validate_mmcif.py
            until the upstream packaging issue is resolved)
    """
    try:
        raw_issues = pdbe_validate(dict_file, mmcif_file)
    except DictionaryNotFoundError as e:
        return False, [PdbeValidationIssue(line=0, item="", message=str(e), severity="error")]
    except CifNotFoundError as e:
        return False, [PdbeValidationIssue(line=0, item="", message=str(e), severity="error")]
    except Exception as e:
        return False, [PdbeValidationIssue(line=0, item="", message=f"Validation not attempted: {e}", severity="error")]

    issues = [
        PdbeValidationIssue(
            line=i.line,
            item=i.item,
            message=i.message,
            severity=i.severity,
        )
        for i in raw_issues
    ]

    is_valid = not any(i.severity == "error" for i in issues)
    return is_valid, issues
