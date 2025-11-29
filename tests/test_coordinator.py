"""
Tests for Coordinator Agent.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
import google.generativeai as genai
from config import Config
from agents.coordinator import CoordinatorAgent


@pytest.fixture(scope="module")
def setup_api():
    """Set up API configuration for tests."""
    try:
        Config.validate()
        genai.configure(api_key=Config.GEMINI_API_KEY)
    except ValueError:
        pytest.skip("GEMINI_API_KEY not configured")


@pytest.fixture
def coordinator(setup_api):
    """Create a CoordinatorAgent instance."""
    return CoordinatorAgent()


def test_coordinator_initialization(coordinator):
    """Test that the coordinator initializes correctly."""
    assert coordinator is not None
    assert coordinator.image_agent is not None
    assert coordinator.pdf_agent is not None


def test_process_nonexistent_file(coordinator):
    """Test handling of non-existent file."""
    result = coordinator.process_file("nonexistent_file.jpg")

    assert result["success"] is False
    assert result["error"] is not None
    assert "not found" in result["error"].lower()


def test_process_unsupported_file_type(coordinator):
    """Test handling of unsupported file type."""
    # Create a temporary text file
    temp_file = Path(__file__).parent / "temp.txt"
    temp_file.write_text("test content")

    try:
        result = coordinator.process_file(str(temp_file))

        assert result["success"] is False
        assert result["file_type"] == "unsupported"
        assert "unsupported" in result["error"].lower()
    finally:
        temp_file.unlink()


def test_process_image_file(coordinator):
    """Test processing an image file."""
    test_image = Path(__file__).parent.parent / "examples/sample_images/test_image_1.jpg"

    if not test_image.exists():
        pytest.skip("Sample image not available")

    result = coordinator.process_file(str(test_image))

    assert result["success"] is True
    assert result["file_type"] == "image"
    assert result["result"]["alt_text"] is not None
    print(f"\nImage processed: {result['result']['alt_text'][:100]}...")


def test_process_pdf_file(coordinator):
    """Test processing a PDF file."""
    test_pdf = Path(__file__).parent.parent / "examples/sample_pdfs/test_doc_1.pdf"

    if not test_pdf.exists():
        pytest.skip("Sample PDF not available")

    result = coordinator.process_file(str(test_pdf))

    assert result["success"] is True
    assert result["file_type"] == "pdf"
    assert result["result"]["text"] is not None
    assert result["result"]["page_count"] > 0
    print(f"\nPDF processed: {result['result']['page_count']} pages")


def test_batch_processing_mixed_files(coordinator):
    """Test batch processing with mixed file types."""
    sample_files = []

    # Add sample images
    image_dir = Path(__file__).parent.parent / "examples/sample_images"
    if image_dir.exists():
        sample_files.extend([str(f) for f in image_dir.glob("*.jpg")[:2]])

    # Add sample PDFs
    pdf_dir = Path(__file__).parent.parent / "examples/sample_pdfs"
    if pdf_dir.exists():
        sample_files.extend([str(f) for f in pdf_dir.glob("*.pdf")[:2]])

    if len(sample_files) == 0:
        pytest.skip("No sample files available")

    batch_result = coordinator.process_batch(sample_files)

    assert batch_result["total_files"] == len(sample_files)
    assert batch_result["successful"] > 0
    assert len(batch_result["results"]) == len(sample_files)

    print(f"\nBatch processing complete:")
    print(f"  Total: {batch_result['total_files']}")
    print(f"  Successful: {batch_result['successful']}")
    print(f"  Failed: {batch_result['failed']}")


def test_generate_summary(coordinator):
    """Test summary generation."""
    sample_files = []

    # Add sample images
    image_dir = Path(__file__).parent.parent / "examples/sample_images"
    if image_dir.exists():
        sample_files.extend([str(f) for f in image_dir.glob("*.jpg")[:1]])

    # Add sample PDFs
    pdf_dir = Path(__file__).parent.parent / "examples/sample_pdfs"
    if pdf_dir.exists():
        sample_files.extend([str(f) for f in pdf_dir.glob("*.pdf")[:1]])

    if len(sample_files) == 0:
        pytest.skip("No sample files available")

    batch_result = coordinator.process_batch(sample_files)
    summary = coordinator.generate_summary(batch_result)

    assert summary is not None
    assert len(summary) > 0
    assert "SUMMARY" in summary
    print(f"\n{summary}")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "-s"])
