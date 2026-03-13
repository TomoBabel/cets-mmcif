from typing import Dict, Any, Optional, List
from pathlib import Path
from cets_mmcif.models.categories import EmMap


# Default values for mandatory em_map fields that are not in CETS.
# These reflect the most common MRC/CCP4 format conventions for cryo-ET data.
# Override via definition file if the actual file uses different settings.
_DEFAULT_DATA_TYPE = "Image stored as floating point number (4 bytes)"  # float32
_DEFAULT_ENDIAN_TYPE = "little"  # Modern MRC files are little-endian (x86)


def _extract_pixel_spacing(tomogram: Dict[str, Any]) -> Optional[List[float]]:
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


def _estimate_size_kb(
    width: Optional[int],
    height: Optional[int],
    depth: Optional[int],
    bytes_per_voxel: int = 4
) -> Optional[int]:
    """
    Estimate map file size in KB from dimensions.
    
    The actual file size (including header and any compression) will differ,
    but this gives OneDep a plausible value when the file is not accessible.
    MRC header is 1024 bytes; we ignore it here as it's negligible.

    Args:
        width: Number of columns
        height: Number of rows  
        depth: Number of sections
        bytes_per_voxel: Bytes per voxel (4 for float32, 2 for int16)
        
    Returns:
        Estimated size in KB, or None if dimensions unavailable
    """
    if width is None or height is None or depth is None:
        return None
    return (width * height * depth * bytes_per_voxel) // 1024


def extract_em_map(
    region: Dict[str, Any],
    dataset_name: str, 
    region_index: int
) -> Optional[EmMap]:
    """
    Extract em_map data from a CETS region.
    
    Args:
        region: CETS region dictionary
        dataset_name: Entry ID for the dataset
        
    Returns:
        EmMap model instance, or None if no tomograms

    Note:
        data_type and endian_type are mandatory for OneDep but not stored in CETS.
        We default to float32 / little-endian, which covers the majority of modern
        cryo-ET datasets. These should be verified and overridden via definition file
        if the actual MRC data_type header field differs.

        size_kb is estimated from voxel dimensions when the file is not accessible.
        The estimate assumes float32 (4 bytes/voxel) and no compression. OneDep
        accepts estimated values here.
    """
    tomograms = region.get("tomograms", [])
    if not tomograms:
        return None
    
    tomogram = tomograms[0]
    
    # Extract dimensions
    width = tomogram.get("width")
    height = tomogram.get("height")
    depth = tomogram.get("depth")
    
    # Extract pixel spacing from coordinate transformations
    pixel_spacing = _extract_pixel_spacing(tomogram)
    spacing_x = pixel_spacing[0] if pixel_spacing else None
    spacing_y = pixel_spacing[1] if pixel_spacing else None
    spacing_z = pixel_spacing[2] if pixel_spacing else None
    
    # Calculate cell dimensions (dimensions * spacing)
    cell_a = (width * spacing_x) if (width and spacing_x) else None
    cell_b = (height * spacing_y) if (height and spacing_y) else None
    cell_c = (depth * spacing_z) if (depth and spacing_z) else None
    
    # File info
    file_path = tomogram.get("path", "")
    
    # Try to get actual file size; fall back to estimate from dimensions
    size_kb = None
    if file_path:
        try:
            size_kb = Path(file_path).stat().st_size // 1024
        except (OSError, FileNotFoundError):
            size_kb = _estimate_size_kb(width, height, depth)
    else:
        size_kb = _estimate_size_kb(width, height, depth)
    
    map_format = "CCP4" if file_path.endswith(".mrc") else None
    
    return EmMap(
        entry_id=dataset_name,
        id=region_index,
        file=file_path,
        format=map_format,
        type="primary map",

        # Axis order
        axis_order_fast="X",
        axis_order_medium="Y",
        axis_order_slow="Z",

        # Cell dimensions
        cell_a=cell_a,
        cell_b=cell_b,
        cell_c=cell_c,
        cell_alpha=90.0,
        cell_beta=90.0,
        cell_gamma=90.0,

        # Mandatory fields with defaults for OneDep
        data_type=_DEFAULT_DATA_TYPE,
        endian_type=_DEFAULT_ENDIAN_TYPE,
        size_kb=size_kb,

        # Voxel dimensions
        dimensions_col=width,
        dimensions_row=height,
        dimensions_sec=depth,
        origin_col=0,
        origin_row=0,
        origin_sec=0,
        partition=1,
        spacing_x=width,
        spacing_y=height,
        spacing_z=depth,
        symmetry_space_group=1,

        pixel_spacing_x=spacing_x,
        pixel_spacing_y=spacing_y,
        pixel_spacing_z=spacing_z,
    )
