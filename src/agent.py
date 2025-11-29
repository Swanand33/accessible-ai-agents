"""
Root agent for AccessibleAI multi-agent system.

This is the main entry point required by Google ADK for deployment.
It provides a simple interface to the multi-agent accessibility system.
"""
import sys
from pathlib import Path
import google.generativeai as genai

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from utils.logging_config import setup_logging
from agents.coordinator import CoordinatorAgent

# Set up logging
logger = setup_logging("INFO")


def main():
    """
    Main entry point for the AccessibleAI system.
    """
    try:
        # Validate and configure
        Config.validate()
        genai.configure(api_key=Config.GEMINI_API_KEY)

        # Create coordinator agent
        coordinator = CoordinatorAgent(model_name=Config.MODEL_NAME)

        print("\n" + "="*60)
        print("AccessibleAI - Multi-Agent Content Accessibility System")
        print("="*60)
        print("\nMaking digital content accessible for everyone.")
        print("\nSupported file types:")
        print("  - Images: JPG, PNG, GIF, BMP, WEBP")
        print("  - Documents: PDF")
        print("\n" + "="*60 + "\n")

        # Example usage
        print("Example usage:")
        print("-" * 60)
        print("from agents.coordinator import CoordinatorAgent")
        print("coordinator = CoordinatorAgent()")
        print("")
        print("# Process single file")
        print("result = coordinator.process_file('path/to/image.jpg')")
        print("print(result['result']['alt_text'])")
        print("")
        print("# Process batch")
        print("files = ['image1.jpg', 'document.pdf']")
        print("batch_result = coordinator.process_batch(files)")
        print("print(coordinator.generate_summary(batch_result))")
        print("-" * 60)

        return coordinator

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print(f"\n✗ Error: {e}")
        print("\nPlease ensure you have:")
        print("1. Created a .env file in the project root")
        print("2. Added your GEMINI_API_KEY to the .env file")
        print("3. Get API key from: https://aistudio.google.com/app/apikey")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Initialize the system
    coordinator = main()

    # Run interactive demo if test files exist
    test_files = [
        "../examples/sample_images/test_image_1.jpg",
        "../examples/sample_pdfs/test_doc_1.pdf"
    ]

    existing_files = [f for f in test_files if Path(f).exists()]

    if existing_files:
        print("\n" + "="*60)
        print("Running demo with available test files...")
        print("="*60 + "\n")

        batch_result = coordinator.process_batch(existing_files)
        print(coordinator.generate_summary(batch_result))
    else:
        print("\nℹ No test files found for demo.")
        print("\nTo test the system:")
        print("1. Place images in examples/sample_images/")
        print("2. Place PDFs in examples/sample_pdfs/")
        print("3. Run: python src/agent.py")
