from typing import Dict, List, Any


def extract_em_experiment(region: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract em_experiment data from a CETS region.
    
    Args:
        region: CETS region dictionary
        
    Returns:
        Dictionary with extracted experiment data
    """
    region_id = region.get('id', '1')
    
    # For tomography, the reconstruction method is always TOMOGRAPHY
    # Other fields would need to come from metadata not in CETS
    return {
        'id': region_id,
        'reconstruction_method': "'TOMOGRAPHY'",
        'aggregation_state': '?',
        'specimen_type': '?'
    }


def generate_em_experiment(regions: List[Dict[str, Any]]) -> List[str]:
    """
    Generate em_experiment category from multiple CETS regions.
    
    Args:
        regions: List of CETS region dictionaries
        
    Returns:
        List of mmCIF formatted lines
    """
    if not regions:
        return []
    
    # Extract data from all regions
    experiments = [extract_em_experiment(region) for region in regions]
    
    lines = []
    lines.append("#")
    lines.append("loop_")
    lines.append("_em_experiment.id")
    lines.append("_em_experiment.reconstruction_method")
    lines.append("_em_experiment.aggregation_state")
    lines.append("_em_experiment.specimen_type")
    
    # Add data rows for all regions
    for exp in experiments:
        lines.append(f"{exp['id']} {exp['reconstruction_method']} {exp['aggregation_state']} {exp['specimen_type']}")
    
    lines.append("#")
    
    return lines
