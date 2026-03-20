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
...still to come...
