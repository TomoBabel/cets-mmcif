import gemmi
from pathlib import Path
from typing import List, Tuple


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
    dict_file: Path
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
            use_unique_keys=True
        )
        
        ddl.read_ddl(dict_doc)

        is_valid = ddl.validate_cif(doc)
        
        if not is_valid and not messages:
            messages.append("Validation failed with no specific error messages.")
        
        return is_valid, messages
        
    except Exception as e:
        return False, [f"Full validation not attempted, due to error: {str(e)}"]
