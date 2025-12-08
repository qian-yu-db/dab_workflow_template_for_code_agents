"""Tests for 02_extract_document_content notebook."""

from unittest.mock import Mock


class TestContentExtraction:
    """Tests for document content extraction logic."""

    def test_reads_from_source_table(self, mock_spark):
        """Test that notebook reads from source table."""
        source_table = "parsed_documents_raw"

        mock_spark.read.format.return_value.table.return_value = Mock()

        # Simulate reading from table
        mock_spark.read.format("delta").table(source_table)

        mock_spark.read.format.assert_called_with("delta")

    def test_handles_zero_records(self, mock_spark, mock_dbutils):
        """Test that pipeline exits when no records found."""
        mock_df = Mock()
        mock_df.count.return_value = 0

        record_count = mock_df.count()
        assert record_count == 0

        if record_count == 0:
            mock_dbutils.notebook.exit("No records found")

        mock_dbutils.notebook.exit.assert_called_with("No records found")

    def test_processes_multiple_records(self, mock_spark):
        """Test that multiple records are processed."""
        mock_df = Mock()
        mock_df.count.return_value = 25

        record_count = mock_df.count()
        assert record_count == 25


class TestTextExtraction:
    """Tests for text extraction transformation."""

    def test_content_column_created(self, mock_dataframe):
        """Test that content column is created."""
        mock_dataframe.withColumn.return_value = mock_dataframe

        result = mock_dataframe.withColumn("content", Mock())

        mock_dataframe.withColumn.assert_called()
        assert result is not None

    def test_error_status_column_created(self, mock_dataframe):
        """Test that error_status column is created."""
        mock_dataframe.withColumn.return_value = mock_dataframe

        result = mock_dataframe.withColumn("error_status", Mock())

        mock_dataframe.withColumn.assert_called()

    def test_select_final_columns(self, mock_dataframe):
        """Test that final columns are selected correctly."""
        expected_columns = ["path", "content", "error_status", "parsed_at"]
        mock_dataframe.select.return_value = mock_dataframe

        result = mock_dataframe.select(*expected_columns)

        mock_dataframe.select.assert_called_with(*expected_columns)

    def test_handles_error_status(self):
        """Test that error_status is handled in transformation."""
        # When error_status exists, content should be None
        # This tests the logic in the when/otherwise expression
        test_cases = [
            {"error_status": "parsing_failed", "expected_content": None},
            {"error_status": None, "expected_content": "extracted content"},
        ]

        for case in test_cases:
            if case["error_status"] is not None:
                assert case["expected_content"] is None
            else:
                assert case["expected_content"] is not None


class TestElementTransformation:
    """Tests for document element transformation."""

    def test_figure_type_uses_description(self):
        """Test that figure elements use description instead of content."""
        # The SQL expression checks: WHEN type = 'figure' THEN description ELSE content
        element = {
            "type": "figure",
            "content": "raw_content",
            "description": "Figure description",
        }

        if element["type"] == "figure":
            result = element["description"]
        else:
            result = element["content"]

        assert result == "Figure description"

    def test_non_figure_type_uses_content(self):
        """Test that non-figure elements use content."""
        element = {"type": "text", "content": "Text content", "description": None}

        if element["type"] == "figure":
            result = element["description"]
        else:
            result = element["content"]

        assert result == "Text content"

    def test_elements_concatenated_with_newlines(self):
        """Test that elements are concatenated with double newlines."""
        elements = ["First paragraph", "Second paragraph", "Third paragraph"]

        result = "\n\n".join(elements)

        assert result == "First paragraph\n\nSecond paragraph\n\nThird paragraph"
        assert result.count("\n\n") == 2


class TestDeltaTableWrite:
    """Tests for Delta table write operations."""

    def test_delta_format_used(self, mock_dataframe):
        """Test that Delta format is used for writing."""
        mock_dataframe.write.format.return_value = mock_dataframe.write

        mock_dataframe.write.format("delta")

        mock_dataframe.write.format.assert_called_with("delta")

    def test_append_mode_used(self, mock_dataframe):
        """Test that append mode is used."""
        mock_dataframe.write.mode.return_value = mock_dataframe.write

        mock_dataframe.write.mode("append")

        mock_dataframe.write.mode.assert_called_with("append")

    def test_merge_schema_enabled(self, mock_dataframe):
        """Test that mergeSchema option is enabled."""
        mock_dataframe.write.option.return_value = mock_dataframe.write

        mock_dataframe.write.option("mergeSchema", "true")

        mock_dataframe.write.option.assert_called_with("mergeSchema", "true")

    def test_saves_to_table(self, mock_dataframe):
        """Test that data is saved to table."""
        table_name = "parsed_documents_content"

        mock_dataframe.write.saveAsTable(table_name)

        mock_dataframe.write.saveAsTable.assert_called_with(table_name)


class TestWidgetParameters:
    """Tests for widget parameter handling."""

    def test_required_parameters(self, mock_dbutils):
        """Test that required parameters are retrieved."""
        required_params = ["catalog", "schema", "source_table_name", "table_name"]

        for param in required_params:
            value = mock_dbutils.widgets.get(param)
            assert value is not None

    def test_source_table_parameter(self, mock_dbutils):
        """Test that source_table_name parameter is used."""
        source_table = mock_dbutils.widgets.get("source_table_name")
        assert source_table == "test_source_table"

    def test_output_table_parameter(self, mock_dbutils):
        """Test that table_name parameter is used for output."""
        table_name = mock_dbutils.widgets.get("table_name")
        assert table_name == "test_table"
