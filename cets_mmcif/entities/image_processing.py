from typing import Dict, List, Any


def extract_em_image_processing(region: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract em_image_processing data from a CETS region.
    
    Args:
        region: CETS region dictionary
        
    Returns:
        Dictionary with extracted image processing data
    """
    region_id = region.get('id', '1')
    
    processing_id = f"{region_id}_processing"
    
    return {
        'id': processing_id,
        'image_recording_id': region_id
    }


def generate_em_image_processing(regions: List[Dict[str, Any]]) -> List[str]:
    """
    Generate em_image_processing category from multiple CETS regions.
    
    Args:
        regions: List of CETS region dictionaries
        
    Returns:
        List of mmCIF formatted lines
    """
    if not regions:
        return []
    
    # Extract data from all regions
    processing_data = [extract_em_image_processing(region) for region in regions]
    
    lines = []
    lines.append("#")
    lines.append("loop_")
    lines.append("_em_image_processing.id")
    lines.append("_em_image_processing.image_recording_id")
    
    for proc in processing_data:
        lines.append(f"{proc['id']} {proc['image_recording_id']}")
    
    lines.append("#")
    
    return lines
