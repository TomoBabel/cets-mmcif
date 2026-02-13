from typing import Dict, Any, List, Optional


def extract_pixel_spacing(tomogram: Dict[str, Any]) -> Optional[List[float]]:
    """
    Extract pixel spacing from tomogram coordinate transformations.
    
    Args:
        tomogram: Tomogram dictionary from CETS
        
    Returns:
        List of [x, y, z] pixel spacing in Angstroms, or None
    """
    transformations = tomogram.get("coordinate_transformations", [])
    
    for transform in transformations:
        if transform.get("transformation_type") == "scale":
            scale = transform.get("scale", [])
            if len(scale) == 3:
                return scale
    
    return None


def add_category_separators(mmcif_string: str) -> str:
    """Add # separators between categories in mmCIF string."""
    lines = mmcif_string.split("\n")
    result = []
    prev_category = None
    
    for line in lines:
        stripped = line.strip()
        
        if not stripped:
            continue
            
        if stripped.startswith("_"):
            category = stripped.split(".")[0]
            
            if prev_category and category != prev_category:
                result.append("#")
            
            prev_category = category
            
        elif stripped.startswith("loop_"):
            if result and result[-1] != "#":
                result.append("#")
            prev_category = None
        
        result.append(line)
    
    return "\n".join(result)
