import subprocess
from pathlib import Path
from typing import Tuple, List


def mmcif_validation(cif_file: Path, dic_file: Path) -> Tuple[bool, List[str]]:
    """
    Validates an mmCIF file using Gemmi's validation.

    Parameters:
    cif_file: Path to the mmCIF file.
    dic_file: Path to the dictionary file for validation.

    Returns:
    tuple: (is_valid, error_messages)
    """
    if not cif_file.exists():
        return False, [f"CIF file not found: {cif_file}"]
    if not dic_file.exists():
        return False, [f"Dictionary file not found: {dic_file}"]

    try:
        result = subprocess.run(
            ["gemmi", "validate", "-v", str(cif_file), "-d", str(dic_file)],
            capture_output=True,
            text=True,
            check=False
        )
        
        errors = []
        if result.returncode != 0:
            errors.append(f"Validation failed with exit code {result.returncode}")
        
        if result.stderr:
            errors.extend(result.stderr.strip().split('\n'))
        
        if result.stdout:
            for line in result.stdout.split('\n'):
                if 'error' in line.lower() or 'warning' in line.lower():
                    errors.append(line.strip())
        
        is_valid = len(errors) == 0 and result.returncode == 0
        
        return is_valid, errors
        
    except FileNotFoundError:
        return False, ["gemmi command not found. Install with: pip install gemmi"]
    except Exception as e:
        return False, [f"Unexpected error: {str(e)}"]
