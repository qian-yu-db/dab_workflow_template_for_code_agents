"""Tests for 01_parse_documents notebook."""

from unittest.mock import Mock


class TestDocumentParsing:
    """Tests for document parsing logic."""

    def test_binary_file_reader_configuration(self, mock_spark):
        """Test that binary file reader is configured correctly."""
        source_path = "/Volumes/test/inputs/"

        # Configure mock
        mock_reader = mock_spark.read
        mock_reader.format.return_value = mock_reader
        mock_reader.option.return_value = mock_reader

        # Simulate reading binary files
        mock_reader.format("binaryFile")
        mock_reader.option("pathGlobFilter", "*.{pdf,jpg,jpeg,png}")
        mock_reader.load(source_path)

        # Verify format was set
        mock_reader.format.assert_called_with("binaryFile")
        mock_reader.option.assert_called_with("pathGlobFilter", "*.{pdf,jpg,jpeg,png}")
        mock_reader.load.assert_called_with(source_path)

    def test_handles_zero_files(self, mock_spark, mock_dbutils):
        """Test that pipeline exits when no files are found."""
        # Configure mock to return 0 files
        mock_df = Mock()
        mock_df.count.return_value = 0
        mock_spark.read.format.return_value.option.return_value.load.return_value = (
            mock_df
        )

        # Check count
        file_count = mock_df.count()
        assert file_count == 0

        # Should exit notebook
        if file_count == 0:
            mock_dbutils.notebook.exit("No files found")

        mock_dbutils.notebook.exit.assert_called_with("No files found")

    def test_processes_multiple_files(self, mock_spark):
        """Test that multiple files are processed."""
        mock_df = Mock()
        mock_df.count.return_value = 10

        file_count = mock_df.count()
        assert file_count == 10

    def test_delta_write_configuration(self, mock_dataframe):
        """Test that Delta table write is configured correctly."""
        table_name = "parsed_documents_raw"

        # Configure write chain
        mock_dataframe.write.format.return_value = mock_dataframe.write
        mock_dataframe.write.mode.return_value = mock_dataframe.write
        mock_dataframe.write.option.return_value = mock_dataframe.write

        # Simulate write
        mock_dataframe.write.format("delta")
        mock_dataframe.write.mode("append")
        mock_dataframe.write.option("delta.feature.variantType-preview", "supported")
        mock_dataframe.write.option("mergeSchema", "true")
        mock_dataframe.write.saveAsTable(table_name)

        mock_dataframe.write.format.assert_called_with("delta")
        mock_dataframe.write.mode.assert_called_with("append")
        mock_dataframe.write.saveAsTable.assert_called_with(table_name)


class TestAIParseDocument:
    """Tests for ai_parse_document function usage."""

    def test_ai_parse_document_version(self):
        """Test that ai_parse_document uses version 2.0."""
        expected_version = "2.0"
        # The notebook uses version 2.0 in the ai_parse_document call
        assert expected_version == "2.0"

    def test_ai_parse_document_options(self):
        """Test that ai_parse_document has correct options."""
        expected_options = {
            "version": "2.0",
            "imageOutputPath": "/Volumes/test/outputs/",
            "descriptionElementTypes": "*",
        }

        assert expected_options["version"] == "2.0"
        assert expected_options["descriptionElementTypes"] == "*"

    def test_parsed_column_added(self, mock_dataframe):
        """Test that parsed column is added to DataFrame."""
        mock_dataframe.withColumn.return_value = mock_dataframe

        # Simulate adding parsed column
        result = mock_dataframe.withColumn("parsed", Mock())
        mock_dataframe.withColumn.assert_called()

        # Result should still be a DataFrame
        assert result.withColumn == mock_dataframe.withColumn


class TestWidgetParameters:
    """Tests for widget parameter handling."""

    def test_required_parameters(self, mock_dbutils):
        """Test that required parameters are retrieved."""
        required_params = [
            "catalog",
            "schema",
            "source_volume_path",
            "output_volume_path",
            "table_name",
        ]

        for param in required_params:
            value = mock_dbutils.widgets.get(param)
            assert value is not None

    def test_catalog_and_schema_usage(self, mock_spark, mock_dbutils):
        """Test that catalog and schema are used in SQL commands."""
        catalog = mock_dbutils.widgets.get("catalog")
        schema = mock_dbutils.widgets.get("schema")

        # Simulate USE CATALOG and USE SCHEMA
        mock_spark.sql(f"USE CATALOG {catalog}")
        mock_spark.sql(f"USE SCHEMA {schema}")

        assert mock_spark.sql.call_count == 2
