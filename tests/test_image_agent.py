"""
Tests for Image Description Agent.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
import google.generativeai as genai
from config import Config
from agents.image_agent import ImageDescriptionAgent


@pytest.fixture(scope="module")
def setup_api():
    """Set up API configuration for tests."""
    try:
        Config.validate()
        genai.configure(api_key=Config.GEMINI_API_KEY)
    except ValueError:
        pytest.skip("GEMINI_API_KEY not configured")


@pytest.fixture
def image_agent(setup_api):
    """Create an ImageDescriptionAgent instance."""
    return ImageDescriptionAgent()


def test_agent_initialization(image_agent):
    """Test that the agent initializes correctly."""
    assert image_agent is not None
    assert image_agent.model_name == "gemini-2.0-flash-exp"
    assert image_agent.model is not None


def test_generate_alt_text_nonexistent_file(image_agent):
    """Test handling of non-existent image file."""
    result = image_agent.generate_alt_text("nonexistent_file.jpg")

    assert result["success"] is False
    assert result["alt_text"] is None
    assert result["error"] is not None
    assert "not found" in result["error"].lower()


def test_generate_alt_text_with_sample_image(image_agent):
    """Test alt-text generation with a sample image (if available)."""
    test_image = Path(__file__).parent.parent / "examples/sample_images/test_image_1.jpg"

    if not test_image.exists():
        pytest.skip("Sample image not available")

    result = image_agent.generate_alt_text(str(test_image))

    assert result["success"] is True
    assert result["alt_text"] is not None
    assert len(result["alt_text"]) > 0
    assert result["error"] is None
    print(f"\nGenerated alt-text: {result['alt_text']}")


def test_detailed_description(image_agent):
    """Test detailed description mode."""
    test_image = Path(__file__).parent.parent / "examples/sample_images/test_image_1.jpg"

    if not test_image.exists():
        pytest.skip("Sample image not available")

    result = image_agent.generate_alt_text(str(test_image), detailed=True)

    assert result["success"] is True
    assert result["alt_text"] is not None
    # Detailed descriptions should be longer
    assert len(result["alt_text"]) > 100
    print(f"\nDetailed description length: {len(result['alt_text'])} chars")


def test_batch_processing(image_agent):
    """Test batch processing of multiple images."""
    sample_dir = Path(__file__).parent.parent / "examples/sample_images"

    if not sample_dir.exists():
        pytest.skip("Sample images directory not available")

    image_files = list(sample_dir.glob("*.jpg")) + list(sample_dir.glob("*.png"))

    if len(image_files) == 0:
        pytest.skip("No sample images available")

    # Limit to first 3 images for testing
    image_paths = [str(f) for f in image_files[:3]]

    results = image_agent.process_batch(image_paths)

    assert len(results) == len(image_paths)
    successful = sum(1 for r in results if r["success"])
    assert successful > 0
    print(f"\nBatch processing: {successful}/{len(image_paths)} successful")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "-s"])
