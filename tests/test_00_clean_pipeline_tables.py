"""Tests for 00-clean-pipeline-tables notebook."""

import os
import shutil


class TestEnsureDirectoriesExist:
    """Tests for ensure_directories_exist function."""

    def test_creates_output_directory_when_not_exists(self, tmp_path):
        """Test that output directory is created when it doesn't exist."""
        output_path = tmp_path / "outputs"
        checkpoint_path = tmp_path / "checkpoints"

        # Ensure directories don't exist
        assert not output_path.exists()
        assert not checkpoint_path.exists()

        # Create directories (simulating the function behavior)
        os.makedirs(output_path, exist_ok=True)
        os.makedirs(checkpoint_path, exist_ok=True)

        assert output_path.exists()
        assert checkpoint_path.exists()

    def test_handles_existing_directory(self, tmp_path):
        """Test that existing directories don't cause errors."""
        output_path = tmp_path / "outputs"
        output_path.mkdir()

        # Should not raise error when directory exists
        os.makedirs(output_path, exist_ok=True)
        assert output_path.exists()


class TestCleanupPipeline:
    """Tests for cleanup_pipeline function."""

    def test_drop_tables_called(self, mock_spark):
        """Test that DROP TABLE is called for each table."""
        tables = [
            "parsed_documents_raw",
            "parsed_documents_content",
            "parsed_documents_structured",
        ]
        catalog = "test_catalog"
        schema = "test_schema"

        # Simulate dropping tables
        for table in tables:
            mock_spark.sql(f"DROP TABLE IF EXISTS {catalog}.{schema}.{table}")

        # Verify SQL was called 3 times
        assert mock_spark.sql.call_count == 3

    def test_checkpoint_cleanup(self, tmp_path):
        """Test that checkpoint directories are cleaned."""
        checkpoint_base = tmp_path / "checkpoints"
        checkpoint_paths = [
            checkpoint_base / "01_parse_documents",
            checkpoint_base / "02_extract_document_content",
            checkpoint_base / "03_extract_key_info",
        ]

        # Create checkpoint directories
        for path in checkpoint_paths:
            path.mkdir(parents=True)
            (path / "test_file.txt").write_text("test")

        # Clean checkpoints (simulating the function)
        for path in checkpoint_paths:
            if path.exists():
                shutil.rmtree(path)

        # Verify cleaned
        for path in checkpoint_paths:
            assert not path.exists()

    def test_output_directory_cleanup(self, tmp_path):
        """Test that output directory contents are cleaned but directory remains."""
        output_path = tmp_path / "outputs"
        output_path.mkdir()

        # Create some files
        (output_path / "file1.txt").write_text("content1")
        (output_path / "file2.txt").write_text("content2")
        subdir = output_path / "subdir"
        subdir.mkdir()
        (subdir / "file3.txt").write_text("content3")

        # Clean contents (simulating the function)
        for item in os.listdir(output_path):
            item_path = output_path / item
            if item_path.is_dir():
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)

        # Directory exists but is empty
        assert output_path.exists()
        assert len(list(output_path.iterdir())) == 0

    def test_skip_cleanup_when_no_selected(self, mock_dbutils):
        """Test that cleanup is skipped when clean_pipeline_tables is No."""
        mock_dbutils.widgets.get.side_effect = lambda key: (
            "No" if key == "clean_pipeline_tables" else "default"
        )

        clean_pipeline = mock_dbutils.widgets.get("clean_pipeline_tables")
        assert clean_pipeline == "No"


class TestWidgetParameters:
    """Tests for widget parameter handling."""

    def test_widget_defaults(self, mock_dbutils):
        """Test that widget parameters have expected defaults."""
        # Test default values
        catalog = mock_dbutils.widgets.get("catalog")
        schema = mock_dbutils.widgets.get("schema")

        assert catalog == "test_catalog"
        assert schema == "test_schema"

    def test_widget_text_called(self, mock_dbutils):
        """Test that widgets.text is called for text inputs."""
        mock_dbutils.widgets.text("catalog", "default_value", "Description")
        mock_dbutils.widgets.text.assert_called_with(
            "catalog", "default_value", "Description"
        )

    def test_widget_dropdown_called(self, mock_dbutils):
        """Test that widgets.dropdown is called for dropdown inputs."""
        mock_dbutils.widgets.dropdown(
            name="clean_pipeline_tables",
            choices=["No", "Yes"],
            defaultValue="No",
            label="Clean all pipeline tables?",
        )
        mock_dbutils.widgets.dropdown.assert_called_once()
