"""
Coordinator Agent - Orchestrates the multi-agent accessibility system.

This is the root agent that coordinates between specialized agents
(Image Description and PDF Processing) to make content accessible.
"""
import logging
from pathlib import Path
from typing import List, Dict
import google.generativeai as genai

from .image_agent import ImageDescriptionAgent
from .pdf_agent import PDFProcessingAgent

logger = logging.getLogger(__name__)


class CoordinatorAgent:
    """
    Root agent that orchestrates content accessibility workflow.

    This agent:
    1. Analyzes input files (images, PDFs)
    2. Routes to appropriate specialized agents
    3. Aggregates results
    4. Provides unified accessibility output
    """

    def __init__(self, model_name="gemini-2.0-flash-exp"):
        """
        Initialize the Coordinator Agent and sub-agents.

        Args:
            model_name: Name of the Gemini model to use
        """
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)

        # Initialize specialized agents
        self.image_agent = ImageDescriptionAgent(model_name)
        self.pdf_agent = PDFProcessingAgent()

        logger.info("=" * 60)
        logger.info("[OK] CoordinatorAgent initialized")
        logger.info(f"  - Image Description Agent: Ready")
        logger.info(f"  - PDF Processing Agent: Ready")
        logger.info(f"  - Model: {model_name}")
        logger.info("=" * 60)

    def process_file(self, file_path: str, detailed: bool = False) -> dict:
        """
        Process a file and make it accessible.

        Automatically detects file type and routes to appropriate agent.

        Args:
            file_path: Path to the file (image or PDF)
            detailed: Whether to generate detailed descriptions

        Returns:
            dict containing:
                - success (bool): Whether processing succeeded
                - file_type (str): Type of file processed
                - file_path (str): Path to the file
                - result (dict): Results from the specialized agent
                - error (str): Error message if failed
        """
        try:
            logger.info(f"\n{'='*60}")
            logger.info(f"Coordinator processing: {file_path}")

            # Validate file exists
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            # Detect file type
            file_ext = file_path_obj.suffix.lower()
            logger.info(f"Detected file type: {file_ext}")

            # Route to appropriate agent
            if file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
                logger.info("-> Routing to Image Description Agent")
                result = self.image_agent.generate_alt_text(file_path, detailed=detailed)
                file_type = "image"

            elif file_ext == '.pdf':
                logger.info("-> Routing to PDF Processing Agent")
                result = self.pdf_agent.extract_text(file_path)
                file_type = "pdf"

            else:
                raise ValueError(
                    f"Unsupported file type: {file_ext}. "
                    f"Supported: images (jpg, png, etc.) and PDFs"
                )

            logger.info(f"{'='*60}\n")

            return {
                "success": result["success"],
                "file_type": file_type,
                "file_path": file_path,
                "result": result,
                "error": result.get("error")
            }

        except FileNotFoundError as e:
            error_msg = str(e)
            logger.error(f"[X] {error_msg}")
            return {
                "success": False,
                "file_type": "unknown",
                "file_path": file_path,
                "result": None,
                "error": error_msg
            }

        except ValueError as e:
            error_msg = str(e)
            logger.error(f"[X] {error_msg}")
            return {
                "success": False,
                "file_type": "unsupported",
                "file_path": file_path,
                "result": None,
                "error": error_msg
            }

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(f"[X] {error_msg}")
            return {
                "success": False,
                "file_type": "unknown",
                "file_path": file_path,
                "result": None,
                "error": error_msg
            }

    def process_batch(self, file_paths: List[str], detailed: bool = False) -> dict:
        """
        Process multiple files in batch.

        Args:
            file_paths: List of file paths to process
            detailed: Whether to generate detailed descriptions

        Returns:
            dict containing:
                - total_files (int): Total number of files
                - successful (int): Number of successfully processed files
                - failed (int): Number of failed files
                - results (list): List of result dictionaries
        """
        logger.info(f"\n{'#'*60}")
        logger.info(f"BATCH PROCESSING: {len(file_paths)} files")
        logger.info(f"{'#'*60}\n")

        results = []
        for i, file_path in enumerate(file_paths, 1):
            logger.info(f"Processing file {i}/{len(file_paths)}")
            result = self.process_file(file_path, detailed=detailed)
            results.append(result)

        # Calculate statistics
        successful = sum(1 for r in results if r["success"])
        failed = len(results) - successful

        logger.info(f"\n{'#'*60}")
        logger.info(f"BATCH COMPLETE")
        logger.info(f"  - Total: {len(file_paths)}")
        logger.info(f"  - Successful: {successful}")
        logger.info(f"  - Failed: {failed}")
        logger.info(f"{'#'*60}\n")

        return {
            "total_files": len(file_paths),
            "successful": successful,
            "failed": failed,
            "results": results
        }

    def generate_summary(self, batch_result: dict) -> str:
        """
        Generate a human-readable summary of batch processing.

        Args:
            batch_result: Result from process_batch()

        Returns:
            Formatted summary string
        """
        summary = [
            f"\n{'='*60}",
            f"ACCESSIBILITY PROCESSING SUMMARY",
            f"{'='*60}",
            f"Total Files: {batch_result['total_files']}",
            f"Successful: {batch_result['successful']} [OK]",
            f"Failed: {batch_result['failed']} [X]",
            f"{'='*60}\n"
        ]

        # Add details for each file
        for i, result in enumerate(batch_result['results'], 1):
            file_name = Path(result['file_path']).name
            status = "[OK]" if result['success'] else "[X]"

            summary.append(f"{i}. {file_name} [{result['file_type']}] {status}")

            if result['success']:
                if result['file_type'] == 'image':
                    alt_text = result['result']['alt_text'][:80]
                    summary.append(f"   -> {alt_text}...")
                elif result['file_type'] == 'pdf':
                    char_count = result['result']['char_count']
                    page_count = result['result']['page_count']
                    summary.append(f"   -> {page_count} pages, {char_count:,} characters")
            else:
                summary.append(f"   -> Error: {result['error']}")

            summary.append("")

        return "\n".join(summary)


# Test function for standalone testing
if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))

    from config import Config
    from utils.logging_config import setup_logging

    # Set up logging
    setup_logging("INFO")

    # Validate config
    try:
        Config.validate()
        genai.configure(api_key=Config.GEMINI_API_KEY)
    except ValueError as e:
        print(f"\n[X] Configuration error: {e}")
        print("Please create a .env file with your GEMINI_API_KEY")
        sys.exit(1)

    # Create coordinator
    coordinator = CoordinatorAgent()

    # Test with sample files
    test_files = [
        "../../examples/sample_images/test_image_1.jpg",
        "../../examples/sample_pdfs/test_doc_1.pdf"
    ]

    # Filter to only existing files
    existing_files = [f for f in test_files if Path(f).exists()]

    if existing_files:
        print(f"\n{'='*60}")
        print("Testing Coordinator Agent")
        print(f"{'='*60}\n")

        # Process batch
        batch_result = coordinator.process_batch(existing_files, detailed=False)

        # Print summary
        print(coordinator.generate_summary(batch_result))
    else:
        print("\nℹ No test files found.")
        print("Place test images in examples/sample_images/")
        print("Place test PDFs in examples/sample_pdfs/")
