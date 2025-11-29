"""
Configuration management for AccessibleAI project.
Loads environment variables and validates settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration from environment variables."""

    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_NAME = "gemini-2.0-flash-exp"  # Using Gemini 2.0 Flash for bonus points

    # Google Cloud Project (optional, for deployment)
    GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")

    # Application Settings
    MAX_IMAGE_SIZE_MB = 10
    MAX_PDF_PAGES = 100
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @staticmethod
    def validate():
        """
        Validate that required configuration is present.

        Raises:
            ValueError: If required configuration is missing
        """
        if not Config.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not found. Please create a .env file with your API key.\n"
                "Get your API key from: https://aistudio.google.com/app/apikey"
            )

        print("[OK] Configuration loaded successfully")
        print(f"[OK] Using model: {Config.MODEL_NAME}")

        return True


if __name__ == "__main__":
    # Test configuration
    try:
        Config.validate()
        print("\n[OK] All configuration valid!")
    except ValueError as e:
        print(f"\n[ERROR] Configuration error: {e}")
