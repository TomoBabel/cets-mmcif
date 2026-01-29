from typing import Dict, List, Any


def extract_em_software(region: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract em_software data from a CETS region.
    
    Args:
        region: CETS region dictionary
        
    Returns:
        Dictionary with extracted software data
    """
    region_id = region.get('id', '1')
    
    # Software information is not in CETS
    software_id = f"{region_id}_software_1"
    software_name = "?"
    category = "'RECONSTRUCTION'"
    processing_id = f"{region_id}_processing"
    
    return {
        'id': software_id,
        'name': software_name,
        'category': category,
        'image_processing_id': processing_id
    }


def generate_em_software(regions: List[Dict[str, Any]]) -> List[str]:
    """
    Generate em_software category from multiple CETS regions.
    
    Args:
        regions: List of CETS region dictionaries
        
    Returns:
        List of mmCIF formatted lines
    """
    if not regions:
        return []
    
    # Extract data from all regions
    software_data = [extract_em_software(region) for region in regions]
    
    lines = []
    lines.append("#")
    lines.append("loop_")
    lines.append("_em_software.id")
    lines.append("_em_software.name")
    lines.append("_em_software.category")
    lines.append("_em_software.image_processing_id")
    
    for soft in software_data:
        lines.append(f"{soft['id']} {soft['name']} {soft['category']} {soft['image_processing_id']}")
    
    lines.append("#")
    
    return lines
