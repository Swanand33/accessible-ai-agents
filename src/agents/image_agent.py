"""
Image Description Agent - Generates accessible alt-text for images.

This agent uses Gemini Vision API to analyze images and create detailed,
accessible descriptions suitable for visually impaired users.
"""
import google.generativeai as genai
from PIL import Image
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ImageDescriptionAgent:
    """
    Agent specialized in generating accessible alt-text for images.

    This agent analyzes images and creates descriptive text that helps
    visually impaired users understand the content, context, and important
    details of images.
    """

    def __init__(self, model_name="gemini-2.0-flash-exp"):
        """
        Initialize the Image Description Agent.

        Args:
            model_name: Name of the Gemini model to use
        """
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
        logger.info(f"[OK] ImageDescriptionAgent initialized with model: {model_name}")

    def generate_alt_text(self, image_path: str, detailed: bool = False) -> dict:
        """
        Generate accessible alt-text for an image.

        Args:
            image_path: Path to the image file (jpg, png, etc.)
            detailed: If True, generates more detailed description

        Returns:
            dict containing:
                - success (bool): Whether the operation succeeded
                - alt_text (str): Generated alt-text description
                - image_path (str): Path to the processed image
                - error (str): Error message if operation failed
        """
        try:
            logger.info(f"Processing image: {image_path}")

            # Validate file exists
            if not Path(image_path).exists():
                raise FileNotFoundError(f"Image file not found: {image_path}")

            # Load image
            img = Image.open(image_path)
            logger.debug(f"Image loaded: {img.size} pixels, {img.mode} mode")

            # Create prompt based on detail level
            if detailed:
                prompt = """Analyze this image and provide a comprehensive, accessible description
                suitable for visually impaired users. Include:

                1. MAIN SUBJECT: What is the primary focus of the image?
                2. DETAILS: Important visual elements (colors, objects, people, text)
                3. SETTING: Where is this taking place? What's the environment?
                4. TEXT: Any visible text, signs, or labels (transcribe exactly)
                5. CONTEXT: What appears to be happening or the purpose of the image?
                6. ACCESSIBILITY NOTES: Any important details for understanding

                Format the description in 3-5 clear sentences that paint a complete picture."""
            else:
                prompt = """Analyze this image and provide a clear, concise alt-text description
                suitable for visually impaired users. Include:

                1. What the main subject is
                2. Important details (colors, key objects, any text visible)
                3. Basic context or setting

                Keep it informative but concise (2-3 sentences)."""

            # Generate description using Gemini Vision
            logger.debug("Calling Gemini Vision API...")
            response = self.model.generate_content([prompt, img])
            alt_text = response.text.strip()

            logger.info(f"[OK] Generated alt-text ({len(alt_text)} chars)")
            logger.debug(f"Alt-text preview: {alt_text[:100]}...")

            return {
                "success": True,
                "alt_text": alt_text,
                "image_path": image_path,
                "error": None
            }

        except FileNotFoundError as e:
            error_msg = str(e)
            logger.error(f"[X] File not found: {error_msg}")
            return {
                "success": False,
                "alt_text": None,
                "image_path": image_path,
                "error": error_msg
            }

        except Exception as e:
            error_msg = f"Error processing image: {str(e)}"
            logger.error(f"[X] {error_msg}")
            return {
                "success": False,
                "alt_text": None,
                "image_path": image_path,
                "error": error_msg
            }

    def process_batch(self, image_paths: list) -> list:
        """
        Process multiple images in batch.

        Args:
            image_paths: List of paths to image files

        Returns:
            List of result dictionaries for each image
        """
        logger.info(f"Processing batch of {len(image_paths)} images")
        results = []

        for i, image_path in enumerate(image_paths, 1):
            logger.info(f"Processing image {i}/{len(image_paths)}")
            result = self.generate_alt_text(image_path)
            results.append(result)

        success_count = sum(1 for r in results if r["success"])
        logger.info(f"[OK] Batch complete: {success_count}/{len(image_paths)} successful")

        return results


# Test function for standalone testing
if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))

    from config import Config
    from utils.logging_config import setup_logging

    # Set up logging
    setup_logging("DEBUG")

    # Validate config
    try:
        Config.validate()
        genai.configure(api_key=Config.GEMINI_API_KEY)
    except ValueError as e:
        print(f"\n[X] Configuration error: {e}")
        print("Please create a .env file with your GEMINI_API_KEY")
        sys.exit(1)

    # Create agent
    agent = ImageDescriptionAgent()

    # Test with sample image (if exists)
    test_image = "../../examples/sample_images/test_image_1.jpg"

    if Path(test_image).exists():
        print(f"\n{'='*60}")
        print("Testing Image Description Agent")
        print(f"{'='*60}\n")

        result = agent.generate_alt_text(test_image, detailed=True)

        if result["success"]:
            print(f"[OK] SUCCESS")
            print(f"\nImage: {result['image_path']}")
            print(f"\nAlt-text:\n{result['alt_text']}")
        else:
            print(f"[X] FAILED: {result['error']}")
    else:
        print(f"\nℹ No test image found at {test_image}")
        print("Place a test image there to test the agent.")
