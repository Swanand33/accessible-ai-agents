"""
Tests for PDF Processing Agent.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from agents.pdf_agent import PDFProcessingAgent


@pytest.fixture
def pdf_agent():
    """Create a PDFProcessingAgent instance."""
    return PDFProcessingAgent()


def test_agent_initialization(pdf_agent):
    """Test that the agent initializes correctly."""
    assert pdf_agent is not None


def test_extract_text_nonexistent_file(pdf_agent):
    """Test handling of non-existent PDF file."""
    result = pdf_agent.extract_text("nonexistent_file.pdf")

    assert result["success"] is False
    assert result["text"] is None
    assert result["page_count"] == 0
    assert result["error"] is not None
    assert "not found" in result["error"].lower()


def test_extract_text_with_sample_pdf(pdf_agent):
    """Test text extraction with a sample PDF (if available)."""
    test_pdf = Path(__file__).parent.parent / "examples/sample_pdfs/test_doc_1.pdf"

    if not test_pdf.exists():
        pytest.skip("Sample PDF not available")

    result = pdf_agent.extract_text(str(test_pdf))

    assert result["success"] is True
    assert result["text"] is not None
    assert len(result["text"]) > 0
    assert result["page_count"] > 0
    assert result["error"] is None
    print(f"\nExtracted {result['char_count']} characters from {result['page_count']} pages")


def test_batch_processing(pdf_agent):
    """Test batch processing of multiple PDFs."""
    sample_dir = Path(__file__).parent.parent / "examples/sample_pdfs"

    if not sample_dir.exists():
        pytest.skip("Sample PDFs directory not available")

    pdf_files = list(sample_dir.glob("*.pdf"))

    if len(pdf_files) == 0:
        pytest.skip("No sample PDFs available")

    pdf_paths = [str(f) for f in pdf_files]

    results = pdf_agent.process_batch(pdf_paths)

    assert len(results) == len(pdf_paths)
    successful = sum(1 for r in results if r["success"])
    assert successful > 0
    print(f"\nBatch processing: {successful}/{len(pdf_paths)} successful")


def test_get_summary_stats(pdf_agent):
    """Test summary statistics generation."""
    test_pdf = Path(__file__).parent.parent / "examples/sample_pdfs/test_doc_1.pdf"

    if not test_pdf.exists():
        pytest.skip("Sample PDF not available")

    result = pdf_agent.extract_text(str(test_pdf))
    summary = pdf_agent.get_summary_stats(result)

    assert summary is not None
    assert len(summary) > 0
    print(f"\nSummary: {summary}")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "-s"])
