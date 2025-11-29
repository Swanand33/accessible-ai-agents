"""
PDF Processing Agent - Extracts and processes text from PDF documents.

This agent makes PDF content accessible by extracting text and providing
structured output suitable for screen readers and text-to-speech systems.
"""
import PyPDF2
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class PDFProcessingAgent:
    """
    Agent specialized in extracting and processing text from PDF documents.

    This agent handles PDF text extraction with error handling for corrupt
    files, password-protected documents, and other common PDF issues.
    """

    def __init__(self):
        """Initialize the PDF Processing Agent."""
        logger.info("[OK] PDFProcessingAgent initialized")

    def extract_text(self, pdf_path: str, max_pages: int = 100) -> dict:
        """
        Extract text from a PDF file for accessibility.

        Args:
            pdf_path: Path to the PDF file
            max_pages: Maximum number of pages to process (safety limit)

        Returns:
            dict containing:
                - success (bool): Whether the operation succeeded
                - text (str): Extracted text from all pages
                - page_count (int): Number of pages processed
                - file_path (str): Path to the PDF file
                - error (str): Error message if operation failed
        """
        try:
            logger.info(f"Processing PDF: {pdf_path}")

            # Validate file exists
            if not Path(pdf_path).exists():
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")

            # Open and read PDF
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)

                # Check if PDF is encrypted
                if pdf_reader.is_encrypted:
                    logger.warning("PDF is encrypted, attempting to decrypt...")
                    try:
                        pdf_reader.decrypt('')  # Try empty password
                    except Exception as e:
                        raise ValueError(f"PDF is password-protected: {str(e)}")

                # Get page count
                total_pages = len(pdf_reader.pages)
                pages_to_process = min(total_pages, max_pages)

                if total_pages > max_pages:
                    logger.warning(
                        f"PDF has {total_pages} pages, processing first {max_pages} only"
                    )

                logger.debug(f"PDF has {total_pages} pages, processing {pages_to_process}")

                # Extract text from all pages
                extracted_pages = []
                for page_num in range(pages_to_process):
                    try:
                        page = pdf_reader.pages[page_num]
                        text = page.extract_text()

                        # Add page separator for multi-page documents
                        page_header = f"\n\n--- Page {page_num + 1} ---\n\n"
                        extracted_pages.append(page_header + text)

                        logger.debug(f"Extracted {len(text)} chars from page {page_num + 1}")

                    except Exception as e:
                        logger.warning(f"Error on page {page_num + 1}: {str(e)}")
                        extracted_pages.append(
                            f"\n\n--- Page {page_num + 1} (extraction failed) ---\n\n"
                        )

                # Combine all pages
                combined_text = "\n".join(extracted_pages)
                char_count = len(combined_text)

                logger.info(
                    f"[OK] Extracted {char_count} characters from {pages_to_process} pages"
                )

                return {
                    "success": True,
                    "text": combined_text,
                    "page_count": pages_to_process,
                    "total_pages": total_pages,
                    "file_path": pdf_path,
                    "char_count": char_count,
                    "error": None
                }

        except FileNotFoundError as e:
            error_msg = str(e)
            logger.error(f"[X] {error_msg}")
            return {
                "success": False,
                "text": None,
                "page_count": 0,
                "total_pages": 0,
                "file_path": pdf_path,
                "char_count": 0,
                "error": error_msg
            }

        except PyPDF2.errors.PdfReadError as e:
            error_msg = f"Invalid or corrupt PDF: {str(e)}"
            logger.error(f"[X] {error_msg}")
            return {
                "success": False,
                "text": None,
                "page_count": 0,
                "total_pages": 0,
                "file_path": pdf_path,
                "char_count": 0,
                "error": error_msg
            }

        except ValueError as e:
            # Password-protected PDFs
            error_msg = str(e)
            logger.error(f"[X] {error_msg}")
            return {
                "success": False,
                "text": None,
                "page_count": 0,
                "total_pages": 0,
                "file_path": pdf_path,
                "char_count": 0,
                "error": error_msg
            }

        except Exception as e:
            error_msg = f"Unexpected error processing PDF: {str(e)}"
            logger.error(f"[X] {error_msg}")
            return {
                "success": False,
                "text": None,
                "page_count": 0,
                "total_pages": 0,
                "file_path": pdf_path,
                "char_count": 0,
                "error": error_msg
            }

    def process_batch(self, pdf_paths: list) -> list:
        """
        Process multiple PDF files in batch.

        Args:
            pdf_paths: List of paths to PDF files

        Returns:
            List of result dictionaries for each PDF
        """
        logger.info(f"Processing batch of {len(pdf_paths)} PDFs")
        results = []

        for i, pdf_path in enumerate(pdf_paths, 1):
            logger.info(f"Processing PDF {i}/{len(pdf_paths)}")
            result = self.extract_text(pdf_path)
            results.append(result)

        success_count = sum(1 for r in results if r["success"])
        logger.info(f"[OK] Batch complete: {success_count}/{len(pdf_paths)} successful")

        return results

    def get_summary_stats(self, result: dict) -> str:
        """
        Get human-readable summary statistics for a PDF extraction.

        Args:
            result: Result dictionary from extract_text()

        Returns:
            Formatted summary string
        """
        if not result["success"]:
            return f"❌ Failed: {result['error']}"

        return (
            f"[OK] Success\n"
            f"  - Pages: {result['page_count']}/{result['total_pages']}\n"
            f"  - Characters: {result['char_count']:,}\n"
            f"  - Words: ~{result['char_count'] // 5:,}"
        )


# Test function for standalone testing
if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))

    from utils.logging_config import setup_logging

    # Set up logging
    setup_logging("DEBUG")

    # Create agent
    agent = PDFProcessingAgent()

    # Test with sample PDF (if exists)
    test_pdf = "../../examples/sample_pdfs/test_doc_1.pdf"

    if Path(test_pdf).exists():
        print(f"\n{'='*60}")
        print("Testing PDF Processing Agent")
        print(f"{'='*60}\n")

        result = agent.extract_text(test_pdf)

        print(agent.get_summary_stats(result))

        if result["success"]:
            print(f"\nText preview (first 500 chars):")
            print("-" * 60)
            print(result['text'][:500])
            print("...")
    else:
        print(f"\nℹ No test PDF found at {test_pdf}")
        print("Place a test PDF there to test the agent.")
