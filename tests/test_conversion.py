import gemmi
import logging
import pytest

from pathlib import Path
from validate_mmcif import validate, DictionaryNotFoundError, CifNotFoundError

from cets_mmcif import conversion


CETS_EXAMPLE = Path(__file__).parent / "input_data" / "CETS_example.json"
OUTPUT_DIR = Path(__file__).parent / "output_data" / "cets_mmcif_test"
EXPECTED_MMCIF_NAME = "CETS-EXAMPLE.cif"


logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def converted_mmcif(tmp_path_factory) -> Path:
    """
    Converts EMPIAR-12104 CETS to mmCIF and returns the path to
    the produced (temporary) file.
    """
    out_dir = tmp_path_factory.mktemp("mmcif_out")

    conversion.convert_cets_to_mmcif(
        cets_input_path=CETS_EXAMPLE,
        mmcif_output_path=out_dir,
    )

    produced = out_dir / EXPECTED_MMCIF_NAME
    assert produced.exists(), (
        f"Conversion did not produce expected file: {produced}"
    )
    return produced


@pytest.fixture(scope="session")
def mmcif_text(converted_mmcif: Path) -> str:
    return converted_mmcif.read_text()


class TestCetsToMmcifOutput:
    """
    Verifies that the mmCIF produced from EMPIAR-12104 contains the expected
    categories and spot-checks key field values that the pipeline populates
    (either directly from CETS data or via principled defaults).
    """
    REQUIRED_CATEGORIES = [
        "_entry",
        "_audit_conform",
        "_em_experiment",
        "_em_imaging",
        "_em_tomography",
        "_em_imaging_optics",
        "_em_specimen",
        "_em_tomography_specimen",
        "_em_image_recording",
        "_em_image_processing",
        "_em_3d_reconstruction",
        "_em_software",
        "_em_map",
    ]

    def test_file_is_non_empty(self, converted_mmcif: Path) -> None:
        assert converted_mmcif.stat().st_size > 0

    def test_file_is_parseable_by_gemmi(self, converted_mmcif: Path) -> None:
        """gemmi must be able to read the file."""
        doc = gemmi.cif.read_file(str(converted_mmcif))
        assert len(doc) >= 1, "Document contains no data blocks"

    @pytest.mark.parametrize("category", REQUIRED_CATEGORIES)
    def test_required_category_present(
        self, category: str, mmcif_text: str
    ) -> None:
        assert category in mmcif_text, (
            f"Expected category '{category}' not found in output mmCIF"
        )

    def test_entry_id(self, mmcif_text: str) -> None:
        assert "_entry.id CETS-EXAMPLE" in mmcif_text

    def test_audit_conform_dict_name(self, mmcif_text: str) -> None:
        assert "_audit_conform.dict_name mmcif_pdbx.dic" in mmcif_text

    # -- em_experiment defaults ----------------------------------------------
    def test_em_experiment_reconstruction_method(self, mmcif_text: str) -> None:
        assert "_em_experiment.reconstruction_method TOMOGRAPHY" in mmcif_text

    def test_em_experiment_aggregation_state_default(self, mmcif_text: str) -> None:
        """Default aggregation state for cryo-ET is CELL."""
        assert "_em_experiment.aggregation_state CELL" in mmcif_text

    def test_em_experiment_entity_assembly_id_placeholder(
        self, mmcif_text: str
    ) -> None:
        assert "_em_experiment.entity_assembly_id 1" in mmcif_text

    # -- em_imaging defaults / CETS-derived values ---------------------------
    def test_em_imaging_illumination_mode(self, mmcif_text: str) -> None:
        """FLOOD BEAM is the cryo-ET default."""
        assert "FLOOD BEAM" in mmcif_text

    def test_em_imaging_mode(self, mmcif_text: str) -> None:
        assert "BRIGHT FIELD" in mmcif_text

    def test_em_imaging_tilt_angles_populated(self, mmcif_text: str) -> None:
        """
        Tilt angle min/max must be numeric values derived from the tilt series,
        not '?' (unknown).  Example has angles spanning ~ -64 to +40.
        """
        assert "_em_imaging.tilt_angle_min" in mmcif_text
        assert "_em_imaging.tilt_angle_max" in mmcif_text

        # Extract values and confirm they are not '?'
        for line in mmcif_text.splitlines():
            if "_em_imaging.tilt_angle_min" in line:
                value = line.split()[-1]
                assert value != "?", "tilt_angle_min should not be unknown"
                assert float(value) < 0, "test min tilt should be negative"
            if "_em_imaging.tilt_angle_max" in line:
                value = line.split()[-1]
                assert value != "?", "tilt_angle_max should not be unknown"
                assert float(value) > 0, "test max tilt should be positive"

    def test_em_imaging_specimen_id_fk(self, mmcif_text: str) -> None:
        """specimen_id must be set to the em_specimen FK placeholder."""
        assert "_em_imaging.specimen_id 1" in mmcif_text

    # -- em_specimen boolean flags -------------------------------------------
    def test_em_specimen_vitrification_applied(self, mmcif_text: str) -> None:
        assert "_em_specimen.vitrification_applied YES" in mmcif_text

    def test_em_specimen_embedding_applied(self, mmcif_text: str) -> None:
        assert "_em_specimen.embedding_applied NO" in mmcif_text

    def test_em_specimen_staining_applied(self, mmcif_text: str) -> None:
        assert "_em_specimen.staining_applied NO" in mmcif_text

    # -- em_tomography: axis angles derived from CETS ------------------------
    def test_em_tomography_axis_angles_populated(self, mmcif_text: str) -> None:
        for line in mmcif_text.splitlines():
            if "_em_tomography.axis1_min_angle" in line:
                assert line.split()[-1] != "?", "axis1_min_angle should not be unknown"
            if "_em_tomography.axis1_max_angle" in line:
                assert line.split()[-1] != "?", "axis1_max_angle should not be unknown"

    # -- em_map: pixel spacing from CETS coordinate transformations ----------
    def test_em_map_pixel_spacing_populated(self, mmcif_text: str) -> None:
        for line in mmcif_text.splitlines():
            if "_em_map.pixel_spacing_x" in line:
                value = line.split()[-1]
                assert value != "?", "pixel_spacing_x should not be unknown"
                # example scale is 13.7 Å
                assert abs(float(value) - 13.7) < 0.5

    def test_em_map_format(self, mmcif_text: str) -> None:
        assert "_em_map.format CCP4" in mmcif_text

    def test_em_map_endian_type(self, mmcif_text: str) -> None:
        assert "_em_map.endian_type little" in mmcif_text

    def test_em_map_data_type(self, mmcif_text: str) -> None:
        """float32 maps to the OneDep-accepted descriptor string."""
        assert "floating point number (4 bytes)" in mmcif_text

    # -- em_tomography_specimen FK -------------------------------------------
    def test_em_tomography_specimen_fk(self, mmcif_text: str) -> None:
        assert "_em_tomography_specimen.specimen_id 1" in mmcif_text


class TestPdbeValidator:
    """
    Runs the converted file through the PDBe standalone mmCIF validator
    and asserts that no validation errors are present.

    Warnings are collected and printed to stdout so they can be reviewed,
    but they do not cause the test to fail.

    If pdbe-mmcif-validator is not installed the test is skipped with a clear
    message rather than failing.
    """
    DICT_PATH = Path(__file__).parents[1] / "resources" / "mmcif_pdbx_v50.dic"

    @pytest.fixture(autouse=True)
    def require_dictionary(self) -> None:
        if not self.DICT_PATH.exists():
            pytest.skip(
                f"mmCIF dictionary not found at {self.DICT_PATH}.  "
                "Place mmcif_pdbx_v50.dic in the resources/ directory."
            )

    def test_no_validation_errors(
        self, converted_mmcif: Path,
    ) -> None:
        """
        The converted mmCIF must be free of pdbe-mmcif-validator errors.
        Warnings are printed for review but do not fail the test.
        """

        try:
            issues = validate(self.DICT_PATH, converted_mmcif)
        except DictionaryNotFoundError as exc:
            pytest.fail(f"Dictionary not found by pdbe-mmcif-validator: {exc}")
        except CifNotFoundError as exc:
            pytest.fail(f"mmCIF file not found by pdbe-mmcif-validator: {exc}")

        errors = [i for i in issues if i.severity == "error"]
        warnings = [i for i in issues if i.severity == "warning"]

        if warnings:
            logger.warning(
                f"\n[pdbe-mmcif-validator] {len(warnings)} warning(s) "
                f"(not failing the test):"
            )
            for w in warnings:
                logger.warning(f"  WARNING  line {w.line}  {w.item}: {w.message}")

        if errors:
            error_lines = "\n".join(
                f"  ERROR  line {e.line}  {e.item}: {e.message}"
                for e in errors
            )
            pytest.fail(
                f"pdbe-mmcif-validator reported {len(errors)} error(s):\n"
                f"{error_lines}"
            )

    def test_no_critical_missing_mandatory_items(
        self, converted_mmcif: Path
    ) -> None:
        """
        A targeted check: mandatory items for the EM categories that the
        pipeline is responsible for must all be present and non-'?'.

        This test reads the issues list and fails only if mandatory-item errors
        appear in the em_* categories we make, rather than failing on any
        dictionary-level mandatory item (which may include categories not yet
        generated by the pipeline).
        """
        issues = validate(self.DICT_PATH, converted_mmcif)

        PIPELINE_CATEGORIES = {
            "_em_experiment",
            "_em_imaging",
            "_em_tomography",
            "_em_specimen",
            "_em_tomography_specimen",
            "_em_image_recording",
            "_em_image_processing",
            "_em_3d_reconstruction",
            "_em_map",
        }

        mandatory_errors = [
            i
            for i in issues
            if i.severity == "error"
            and "mandatory" in i.message.lower()
            and any(i.item.startswith(cat) for cat in PIPELINE_CATEGORIES)
        ]

        if mandatory_errors:
            detail = "\n".join(
                f"  line {e.line}  {e.item}: {e.message}"
                for e in mandatory_errors
            )
            pytest.fail(
                f"{len(mandatory_errors)} mandatory-item error(s) in "
                f"pipeline-owned EM categories:\n{detail}"
            )
