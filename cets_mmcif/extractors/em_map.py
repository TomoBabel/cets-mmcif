from typing import Dict, Any, Optional, List
from cets_mmcif.models.categories import EmMap


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


def extract_em_map(
    region: Dict[str, Any],
    dataset_name: str
) -> Optional[EmMap]:
    """
    Extract em_map data from a CETS region.
    
    Args:
        region: CETS region dictionary
        dataset_name: Entry ID for the dataset
        
    Returns:
        EmMap model instance, or None if no tomograms
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
    map_format = "CCP4" if file_path.endswith(".mrc") else None
    map_id = tomogram.get("id", "1")
    
    
    return EmMap(
        entry_id=dataset_name,
        id=map_id,
        file=file_path,
        format=map_format,
        type="primary map",  # TODO: use proper enum value
        
        # Mandatory fields
        axis_order_fast="X",
        axis_order_medium="Y",
        axis_order_slow="Z",
        cell_a=cell_a,
        cell_b=cell_b,
        cell_c=cell_c,
        cell_alpha=90.0,
        cell_beta=90.0,
        cell_gamma=90.0,
        data_type=None, # TODO: ?
        dimensions_col=width,
        dimensions_row=height,
        dimensions_sec=depth,
        endian_type=None, # TODO: check
        origin_col=0,
        origin_row=0,
        origin_sec=0,
        partition=1,
        size_kb=None,
        spacing_x=spacing_x,
        spacing_y=spacing_y,
        spacing_z=spacing_z,
        symmetry_space_group=1,
        
        # Deprecated fields 
        # TODO: remove these?
        pixel_spacing_x=spacing_x,
        pixel_spacing_y=spacing_y,
        pixel_spacing_z=spacing_z,
        num_columns=width,
        num_rows=height,
        num_sections=depth
    )
