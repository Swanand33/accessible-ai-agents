"""
Interactive demo script for AccessibleAI.

This script demonstrates the multi-agent system with sample files.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import google.generativeai as genai
from config import Config
from utils.logging_config import setup_logging
from agents.coordinator import CoordinatorAgent


def print_header(text):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"{text:^60}")
    print(f"{'='*60}\n")


def print_section(text):
    """Print a formatted section header."""
    print(f"\n{'-'*60}")
    print(f"  {text}")
    print(f"{'-'*60}\n")


def demo_single_image(coordinator):
    """Demo: Process a single image."""
    print_section("Demo 1: Single Image Processing")

    image_path = "examples/sample_images/test_image_1.jpg"

    if not Path(image_path).exists():
        print(f"[!] Sample image not found: {image_path}")
        print("   Please add a test image to examples/sample_images/")
        return

    print(f"Processing: {image_path}")
    result = coordinator.process_file(image_path)

    if result['success']:
        print(f"\n[SUCCESS]\n")
        print(f"Alt-text:\n{result['result']['alt_text']}\n")
    else:
        print(f"\n[FAILED]\n")
        print(f"Error: {result['error']}\n")


def demo_single_pdf(coordinator):
    """Demo: Process a single PDF."""
    print_section("Demo 2: Single PDF Processing")

    pdf_path = "examples/sample_pdfs/test_doc_1.pdf"

    if not Path(pdf_path).exists():
        print(f"[!] Sample PDF not found: {pdf_path}")
        print("   Please add a test PDF to examples/sample_pdfs/")
        return

    print(f"Processing: {pdf_path}")
    result = coordinator.process_file(pdf_path)

    if result['success']:
        print(f"\n[SUCCESS]\n")
        print(f"Pages: {result['result']['page_count']}")
        print(f"Characters: {result['result']['char_count']:,}")
        print(f"\nText preview (first 300 chars):")
        print(f"{'-'*60}")
        print(f"{result['result']['text'][:300]}...")
        print(f"{'-'*60}\n")
    else:
        print(f"\n[FAILED]\n")
        print(f"Error: {result['error']}\n")


def demo_batch_processing(coordinator):
    """Demo: Batch processing of multiple files."""
    print_section("Demo 3: Batch Processing")

    # Collect all available test files
    files = []

    image_dir = Path("examples/sample_images")
    if image_dir.exists():
        files.extend([str(f) for f in image_dir.glob("*.jpg")])
        files.extend([str(f) for f in image_dir.glob("*.png")])

    pdf_dir = Path("examples/sample_pdfs")
    if pdf_dir.exists():
        files.extend([str(f) for f in pdf_dir.glob("*.pdf")])

    if not files:
        print("[!] No sample files found")
        print("   Please add images to examples/sample_images/")
        print("   Please add PDFs to examples/sample_pdfs/")
        return

    print(f"Processing {len(files)} files...\n")

    batch_result = coordinator.process_batch(files)

    # Print summary
    print(coordinator.generate_summary(batch_result))


def demo_detailed_description(coordinator):
    """Demo: Detailed image description."""
    print_section("Demo 4: Detailed Image Description")

    image_path = "examples/sample_images/test_image_1.jpg"

    if not Path(image_path).exists():
        print(f"[!] Sample image not found: {image_path}")
        return

    print(f"Processing: {image_path}")
    print("Mode: DETAILED\n")

    result = coordinator.process_file(image_path, detailed=True)

    if result['success']:
        print(f"[SUCCESS]\n")
        print(f"Detailed Description:\n")
        print(f"{result['result']['alt_text']}\n")
        print(f"Length: {len(result['result']['alt_text'])} characters\n")
    else:
        print(f"[FAILED]\n")
        print(f"Error: {result['error']}\n")


def main():
    """Run interactive demo."""
    print_header("AccessibleAI - Multi-Agent Demo")

    # Setup logging (quieter for demo)
    setup_logging("WARNING")

    # Validate configuration
    try:
        Config.validate()
        genai.configure(api_key=Config.GEMINI_API_KEY)
    except ValueError as e:
        print(f"\n[ERROR] Configuration Error: {e}\n")
        print("Please ensure:")
        print("1. You have created a .env file")
        print("2. Added your GEMINI_API_KEY to the .env file")
        print("3. Get API key from: https://aistudio.google.com/app/apikey\n")
        return 1

    # Create coordinator
    print("Initializing multi-agent system...")
    coordinator = CoordinatorAgent()
    print("[OK] System ready!\n")

    # Run demos
    try:
        demo_single_image(coordinator)
        demo_single_pdf(coordinator)
        demo_batch_processing(coordinator)
        demo_detailed_description(coordinator)

        print_header("Demo Complete!")
        print("\n[SUCCESS] All demos finished successfully!\n")
        print("Next steps:")
        print("1. Add your own images to examples/sample_images/")
        print("2. Add your own PDFs to examples/sample_pdfs/")
        print("3. Run: python demo.py")
        print("4. Or use the API directly (see README.md)\n")

    except Exception as e:
        print(f"\n[ERROR] Error during demo: {e}\n")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
