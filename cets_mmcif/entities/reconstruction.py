from typing import Dict, List, Any


def extract_em_3d_reconstruction(region: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract em_3d_reconstruction data from a CETS region.
    
    Args:
        region: CETS region dictionary
        
    Returns:
        Dictionary with extracted reconstruction data, or None if no tilt series
    """
    region_id = region.get('id', '1')
    
    tilt_series_list = region.get('tilt_series', [])
    if not tilt_series_list:
        return None
    
    tilt_series = tilt_series_list[0]
    images = tilt_series.get('images', [])
    
    num_images = len(images)
    processing_id = f"{region_id}_processing"
    
    return {
        'id': region_id,
        'image_processing_id': processing_id,
        'method': "'TOMOGRAPHY'",
        'num_particles': num_images
    }


def generate_em_3d_reconstruction(regions: List[Dict[str, Any]]) -> List[str]:
    """
    Generate em_3d_reconstruction category from multiple CETS regions.
    
    Args:
        regions: List of CETS region dictionaries
        
    Returns:
        List of mmCIF formatted lines
    """
    # Extract data from all regions
    recon_data = [extract_em_3d_reconstruction(region) for region in regions]
    recon_data = [data for data in recon_data if data is not None]
    
    if not recon_data:
        return []
    
    lines = []
    lines.append("#")
    lines.append("loop_")
    lines.append("_em_3d_reconstruction.id")
    lines.append("_em_3d_reconstruction.image_processing_id")
    lines.append("_em_3d_reconstruction.method")
    lines.append("_em_3d_reconstruction.num_particles")
    
    for recon in recon_data:
        lines.append(f"{recon['id']} {recon['image_processing_id']} {recon['method']} {recon['num_particles']}")
    
    lines.append("#")
    
    return lines
