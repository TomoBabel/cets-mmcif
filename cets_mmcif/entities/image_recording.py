from typing import Dict, List, Any


def extract_em_image_recording(region: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract em_image_recording data from a CETS region.
    
    Args:
        region: CETS region dictionary
        
    Returns:
        Dictionary with extracted image recording data, or None if no movie stacks
    """
    region_id = region.get('id', '1')
    
    movie_collection = region.get('movie_stack_collection', {})
    movie_stacks = movie_collection.get('movie_stacks', [])
    
    if not movie_stacks:
        return None
    
    movie_series = movie_stacks[0]
    stacks = movie_series.get('stacks', [])
    
    if not stacks:
        return None
    
    num_stacks = len(stacks)
    
    return {
        'id': region_id,
        'imaging_id': region_id,
        'num_grids_imaged': 1,
        'num_real_images': num_stacks,
        'detector_mode': 'COUNTING'
    }


def generate_em_image_recording(regions: List[Dict[str, Any]]) -> List[str]:
    """
    Generate em_image_recording category from multiple CETS regions.
    
    Args:
        regions: List of CETS region dictionaries
        
    Returns:
        List of mmCIF formatted lines
    """
    # Extract data from all regions
    recording_data = [extract_em_image_recording(region) for region in regions]
    recording_data = [data for data in recording_data if data is not None]
    
    if not recording_data:
        return []
    
    lines = []
    lines.append("#")
    lines.append("loop_")
    lines.append("_em_image_recording.id")
    lines.append("_em_image_recording.imaging_id")
    lines.append("_em_image_recording.num_grids_imaged")
    lines.append("_em_image_recording.num_real_images")
    lines.append("_em_image_recording.detector_mode")
    
    for rec in recording_data:
        lines.append(f"{rec['id']} {rec['imaging_id']} {rec['num_grids_imaged']} {rec['num_real_images']} {rec['detector_mode']}")
    
    lines.append("#")
    
    return lines
