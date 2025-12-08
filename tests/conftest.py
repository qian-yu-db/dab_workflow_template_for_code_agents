"""Shared fixtures for testing Databricks notebooks."""

from unittest.mock import Mock

import pytest


@pytest.fixture
def mock_dbutils():
    """Mock dbutils for Databricks notebooks."""
    dbutils = Mock()

    # Mock widgets
    widget_values = {
        "catalog": "test_catalog",
        "schema": "test_schema",
        "source_volume_path": "/Volumes/test/path/inputs/",
        "output_volume_path": "/Volumes/test/path/outputs/",
        "table_name": "test_table",
        "source_table_name": "test_source_table",
        "raw_table_name": "parsed_documents_raw",
        "content_table_name": "parsed_documents_content",
        "structured_table_name": "parsed_documents_structured",
        "checkpoint_base_path": "checkpoints/test",
        "clean_pipeline_tables": "No",
    }
    dbutils.widgets.get = Mock(side_effect=lambda key: widget_values.get(key, ""))
    dbutils.widgets.text = Mock()
    dbutils.widgets.dropdown = Mock()

    # Mock notebook
    dbutils.notebook.exit = Mock()

    # Mock fs
    dbutils.fs.ls = Mock(return_value=[])
    dbutils.fs.rm = Mock()
    dbutils.fs.mkdirs = Mock()

    return dbutils


@pytest.fixture
def mock_spark():
    """Mock Spark session for Databricks notebooks."""
    spark = Mock()

    # Mock SQL execution
    spark.sql = Mock()

    # Mock read
    mock_reader = Mock()
    mock_df = Mock()
    mock_df.count = Mock(return_value=5)
    mock_df.write = Mock()
    mock_df.write.format = Mock(return_value=mock_df.write)
    mock_df.write.mode = Mock(return_value=mock_df.write)
    mock_df.write.option = Mock(return_value=mock_df.write)
    mock_df.write.saveAsTable = Mock()

    mock_reader.format = Mock(return_value=mock_reader)
    mock_reader.option = Mock(return_value=mock_reader)
    mock_reader.load = Mock(return_value=mock_df)
    mock_reader.table = Mock(return_value=mock_df)
    spark.read = mock_reader

    # Mock table method
    spark.table = Mock(return_value=mock_df)

    return spark


@pytest.fixture
def mock_dataframe():
    """Mock PySpark DataFrame."""
    df = Mock()
    df.count = Mock(return_value=5)
    df.columns = ["path", "content", "parsed", "parsed_at", "error_status"]

    # Mock write
    df.write = Mock()
    df.write.format = Mock(return_value=df.write)
    df.write.mode = Mock(return_value=df.write)
    df.write.option = Mock(return_value=df.write)
    df.write.saveAsTable = Mock()

    # Mock transformations
    df.withColumn = Mock(return_value=df)
    df.select = Mock(return_value=df)
    df.filter = Mock(return_value=df)

    return df


@pytest.fixture
def temp_directory(tmp_path):
    """Create temporary directory for testing file operations."""
    test_dir = tmp_path / "test_workspace"
    test_dir.mkdir()
    return test_dir
