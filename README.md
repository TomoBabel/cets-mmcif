# CETS – mmCIF
For conversion between cryoET standards (CETS) and mmCIF.

## Installation + configuration
With poetry — from the top level of the cloned repository:

    poetry install

A default location for saving output mmCIF files can be specified in a .env file, as can an alternative dictionary for validation — as `output_mmcif_directory` and `validation_dictionary_path`, respectively — refer to the .env_template. 

## Use
### Conversion
To convert a CETS object to an mmCIF file:

    poetry run cets-mmcif convert -i <path_to_input_CETS_json_file>

and optionally, an output location can be specified, for example:

    poetry run cets-mmcif convert -i <path_to_input_CETS_json_file> -o <path_to_output_directory>

#### Options summary
| Option | Short | Values | Description | Default |
|--------|-------|-------------|-------------|---------|
| `--cets-input` | `-i` | — [PATH \| str] | Path to the CETS dataset to be converted. [required] | — |
| `--mmcif-output` | `-o` | — [PATH \| str] | Output directory for the mmCIF data. | ./output_data/cets-mmcif |
| `--help` | — | — | Show help. | — |

### Validation
To validate an mmCIF file:

    poetry run cets-mmcif validate -f <path_to_input_mmCIF_file>


#### Options summary
| Option | Short | Values | Description | Default |
|--------|-------|-------------|-------------|---------|
| `--file` | `-f` | — [PATH \| str] | Path to the mmCIF file to be validated. [required] | — |
| `--help` | — | — | Show help. | — |


#### Description

    Validate an mmCIF file using gemmi and the PDBe mmCIF validator.

    Both validators run against the same dictionary. 
        gemmi checks structural conformance against the DDL2 schema
        PDBe validator does submission-readiness checks. This validator performs deeper deposition-readiness checks than gemmi, including foreign key integrity, enumeration validation, composite key, validation, and data type checking against the mmCIF dictionary.


#### Example printout
[15:50:02] INFO     cets_mmcif.cli - [15:50:02] - INFO - --- gemmi validation ---                                cli.py:96
           INFO     cets_mmcif.cli - [15:50:02] - INFO - gemmi validation passed.                                cli.py:99
           INFO     cets_mmcif.cli - [15:50:02] - INFO - --- PDBe mmCIF validator ---                           cli.py:106
           INFO     cets_mmcif.cli - [15:50:02] - INFO - PDBe validation passed.                                cli.py:113
           WARNING  cets_mmcif.cli - [15:50:02] - WARNING - Line 161  _em_map.pixel_spacing_x: Out of advisory  cli.py:121
                    range: Value '13.699999809265137' is above maximum advised value '5.0'                                
           WARNING  cets_mmcif.cli - [15:50:02] - WARNING - Line 162  _em_map.pixel_spacing_y: Out of advisory  cli.py:121
                    range: Value '13.699999809265137' is above maximum advised value '5.0'                                
           WARNING  cets_mmcif.cli - [15:50:02] - WARNING - Line 163  _em_map.pixel_spacing_z: Out of advisory  cli.py:121
                    range: Value '13.699999809265137' is above maximum advised value '5.0'                                
           INFO     cets_mmcif.cli - [15:50:02] - INFO - --- Summary ---                                        cli.py:123
           INFO     cets_mmcif.cli - [15:50:02] - INFO - All validation passed.                                 cli.py:125
