import gemmi
from typing import List, Any
from pydantic import BaseModel
from pydantic.alias_generators import to_snake


def get_category_name(model_class: type[BaseModel]) -> str:
    """
    Convert model class name to mmCIF snake_case category name.
    """
    name = model_class.__name__
    return to_snake(name)


def format_value(value: Any) -> str:
    """
    Format a value for mmCIF output.
    
    Args:
        value: Value to format
        
    Returns:
        Formatted string suitable for mmCIF
    """
    if value is None:
        return "?"
    
    if isinstance(value, bool):
        return "YES" if value else "NO"
    
    if isinstance(value, (int, float)):
        return str(value)
    
    str_value = str(value)
    
    # Quote strings with spaces or special characters
    needs_quoting = any(char in str_value for char in [" ", ":", "/", "#"])
    
    if needs_quoting:
        # Avoid double-quoting
        if not (str_value.startswith(""") and str_value.endswith(""")):
            return f"'{str_value}'"
    
    return str_value


def get_mmcif_field_name(field_mappings: dict, python_field: str) -> str:
    """Get the mmCIF field name (handles special mappings)."""
    return field_mappings.get(python_field, python_field)


def serialize_category(
    block: gemmi.cif.Block,
    categories: List[BaseModel]
) -> None:
    """
    Serialize Pydantic model categories to mmCIF block.
    
    Args:
        block: gemmi Block to add data to
        categories: List of Pydantic model category instances
    """
    if not categories:
        return
    
    model_class = categories[0].__class__
    category = get_category_name(model_class)
    
    # TODO: deprecation fix
    field_names = list(categories[0].model_fields.keys())
    
    # Handle field name mappings (e.g., Python "fitting_id" -> mmCIF "3d_fitting_id")
    field_mappings = {}
    if hasattr(model_class, "Config") and hasattr(model_class.Config, "fields"):
        field_mappings = model_class.Config.fields
    
    mmcif_field_names = [get_mmcif_field_name(field_mappings, f) for f in field_names]

    if len(categories) == 1:
        instance = categories[0]
        for field_name, mmcif_field in zip(field_names, mmcif_field_names):
            value = getattr(instance, field_name)
            block.set_pair(f"_{category}.{mmcif_field}", format_value(value))
    else:
        loop = block.init_loop(f"_{category}.", mmcif_field_names)

        for instance in categories:
            row = [format_value(getattr(instance, field_name)) for field_name in field_names]
            loop.add_row(row)
