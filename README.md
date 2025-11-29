# AccessibleAI - Multi-Agent Content Accessibility System

**Making digital content accessible for 2.2 billion people with vision impairment**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Gemini 2.0](https://img.shields.io/badge/Gemini-2.0%20Flash-orange.svg)](https://ai.google.dev/)

---

## 📖 Table of Contents

- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Features](#-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Examples](#-usage-examples)
- [API Reference](#-api-reference)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚨 Problem Statement

### The Accessibility Crisis

- **2.2 billion people** worldwide have vision impairment or blindness
- Only **3% of web images** have meaningful alt-text descriptions
- **95% of PDFs** are completely inaccessible to screen readers
- This excludes people with disabilities from:
  - **Education**: Textbooks, research papers, course materials
  - **Employment**: Job applications, work documents, training materials
  - **Basic Information**: News, government documents, healthcare information

### Why This Matters

Without accessible digital content, people with visual impairments face:
- Barriers to education and career advancement
- Inability to access critical information independently
- Dependence on others for basic tasks
- Exclusion from digital society

---

## 💡 Solution

**AccessibleAI** is a multi-agent system that automatically makes digital content accessible by:

1. **Generating descriptive alt-text** for images using AI vision
2. **Extracting and structuring text** from PDF documents
3. **Orchestrating specialized agents** to handle different content types seamlessly

### Why Multi-Agent?

- **Specialization**: Each agent is optimized for its specific task
- **Scalability**: Easy to add new content types (audio, video, etc.)
- **Reliability**: Failure in one agent doesn't crash the entire system
- **Observability**: Track and log each agent's performance independently

---

## ✨ Features

### 🔥 Core Features

1. **Multi-Agent Architecture** ⭐
   - Image Description Agent (Gemini Vision)
   - PDF Processing Agent (PyPDF2)
   - Coordinator Agent (orchestration)

2. **Tools Integration** 🛠️
   - Google Gemini 2.0 Flash API
   - PyPDF2 for PDF extraction
   - Pillow for image processing

3. **Comprehensive Observability** 📊
   - Structured logging for all operations
   - Success/failure tracking
   - Performance metrics

### 🎁 Bonus Features

- **Batch Processing**: Process multiple files at once
- **Detailed Descriptions**: Toggle between concise and detailed alt-text
- **Error Handling**: Graceful handling of corrupt/invalid files
- **Summary Generation**: Human-readable processing reports

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────┐
│                   CoordinatorAgent                      │
│              (Orchestrates workflow)                    │
└─────────────────┬───────────────────────────────────────┘
                  │
        ┌─────────┴──────────┐
        │                    │
        ▼                    ▼
┌──────────────┐     ┌──────────────┐
│ImageAgent    │     │PDFAgent      │
│(Gemini Vision│     │(PyPDF2)      │
│ API)         │     │              │
└──────────────┘     └──────────────┘
```

### Agent Responsibilities

#### 1. CoordinatorAgent
- **Role**: Root orchestrator
- **Responsibilities**:
  - Detect file type (image vs PDF)
  - Route to appropriate specialized agent
  - Aggregate results
  - Generate summaries
- **Tools**: File type detection, routing logic

#### 2. ImageDescriptionAgent
- **Role**: Image accessibility specialist
- **Responsibilities**:
  - Analyze images using Gemini Vision
  - Generate descriptive alt-text
  - Support detailed descriptions
- **Tools**: Google Gemini 2.0 Flash, PIL/Pillow

#### 3. PDFProcessingAgent
- **Role**: Document accessibility specialist
- **Responsibilities**:
  - Extract text from PDFs
  - Handle multi-page documents
  - Manage corrupt/encrypted files
- **Tools**: PyPDF2

### Data Flow

```
Input File → Coordinator → File Type Detection → Specialized Agent
                                                        ↓
User ← Accessible Output ← Result Aggregation ← Agent Processing
```

---

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/accessible-ai-capstone.git
cd accessible-ai-capstone
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv agent-env

# Activate (Windows)
agent-env\Scripts\activate

# Activate (Mac/Linux)
source agent-env/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure API Key

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Gemini API key:
   ```bash
   GEMINI_API_KEY=your_actual_api_key_here
   ```

3. **IMPORTANT**: Never commit your `.env` file to GitHub!

---

## 🎯 Quick Start

### Basic Usage

```python
from src.agents.coordinator import CoordinatorAgent
import google.generativeai as genai
from src.config import Config

# Configure API
Config.validate()
genai.configure(api_key=Config.GEMINI_API_KEY)

# Create coordinator
coordinator = CoordinatorAgent()

# Process an image
result = coordinator.process_file("path/to/image.jpg")
print(result['result']['alt_text'])

# Process a PDF
result = coordinator.process_file("path/to/document.pdf")
print(f"Extracted {result['result']['char_count']} characters")
```

### Running the Demo

```bash
# Place test files in examples/
# - examples/sample_images/test_image_1.jpg
# - examples/sample_pdfs/test_doc_1.pdf

# Run the main agent
python src/agent.py
```

---

## 📚 Usage Examples

### Example 1: Single Image Processing

```python
from src.agents.coordinator import CoordinatorAgent

coordinator = CoordinatorAgent()

# Process image
result = coordinator.process_file("family_photo.jpg")

if result['success']:
    print("Alt-text:", result['result']['alt_text'])
else:
    print("Error:", result['error'])
```

**Output:**
```
Alt-text: A family of four standing on a beach at sunset. Two adults and two children smiling at the camera. The ocean is visible in the background with orange and pink hues in the sky. Everyone is wearing casual summer clothing.
```

### Example 2: Batch Processing

```python
from src.agents.coordinator import CoordinatorAgent

coordinator = CoordinatorAgent()

# Process multiple files
files = [
    "presentation_slide1.jpg",
    "presentation_slide2.jpg",
    "reference_document.pdf"
]

batch_result = coordinator.process_batch(files)

# Print summary
print(coordinator.generate_summary(batch_result))
```

**Output:**
```
============================================================
ACCESSIBILITY PROCESSING SUMMARY
============================================================
Total Files: 3
Successful: 3 ✓
Failed: 0 ✗
============================================================

1. presentation_slide1.jpg [image] ✓
   → A business presentation slide showing quarterly sales data with a bar ch...

2. presentation_slide2.jpg [image] ✓
   → A diagram illustrating the company's organizational structure with conne...

3. reference_document.pdf [pdf] ✓
   → 5 pages, 3,482 characters
```

### Example 3: Detailed Image Description

```python
from src.agents.image_agent import ImageDescriptionAgent
import google.generativeai as genai
from src.config import Config

Config.validate()
genai.configure(api_key=Config.GEMINI_API_KEY)

agent = ImageDescriptionAgent()

# Get detailed description
result = agent.generate_alt_text("complex_diagram.jpg", detailed=True)

print(result['alt_text'])
```

---

## 📖 API Reference

### CoordinatorAgent

#### `process_file(file_path, detailed=False)`

Process a single file (image or PDF).

**Parameters:**
- `file_path` (str): Path to the file
- `detailed` (bool): Whether to generate detailed descriptions (images only)

**Returns:**
- dict with keys: `success`, `file_type`, `file_path`, `result`, `error`

#### `process_batch(file_paths, detailed=False)`

Process multiple files in batch.

**Parameters:**
- `file_paths` (list): List of file paths
- `detailed` (bool): Whether to generate detailed descriptions

**Returns:**
- dict with keys: `total_files`, `successful`, `failed`, `results`

#### `generate_summary(batch_result)`

Generate human-readable summary of batch processing.

**Parameters:**
- `batch_result` (dict): Result from `process_batch()`

**Returns:**
- str: Formatted summary

### ImageDescriptionAgent

#### `generate_alt_text(image_path, detailed=False)`

Generate alt-text for an image.

**Parameters:**
- `image_path` (str): Path to image file
- `detailed` (bool): Whether to generate detailed description

**Returns:**
- dict with keys: `success`, `alt_text`, `image_path`, `error`

### PDFProcessingAgent

#### `extract_text(pdf_path, max_pages=100)`

Extract text from a PDF file.

**Parameters:**
- `pdf_path` (str): Path to PDF file
- `max_pages` (int): Maximum pages to process

**Returns:**
- dict with keys: `success`, `text`, `page_count`, `total_pages`, `file_path`, `char_count`, `error`

---

## 🧪 Testing

### Run All Tests

```bash
python run_tests.py
```

### Run Specific Test File

```bash
pytest tests/test_image_agent.py -v
pytest tests/test_pdf_agent.py -v
pytest tests/test_coordinator.py -v
```

### Test Coverage

- ✅ Agent initialization
- ✅ Error handling (missing files, corrupt files)
- ✅ Image alt-text generation
- ✅ PDF text extraction
- ✅ Batch processing
- ✅ Multi-agent coordination

---

## 🚀 Deployment

### Deploy to Google Cloud (Agent Engine)

```bash
# Install ADK CLI (if not already installed)
pip install google-adk

# Deploy to Agent Engine
adk deploy --project-id=YOUR_PROJECT_ID --region=us-central1

# Get deployment URL
adk info
```

### Local Development Server

```bash
# Run locally for testing
python src/agent.py
```

---

## 🛠️ Project Structure

```
accessible-ai-capstone/
├── src/
│   ├── agent.py              # Main entry point (ADK required)
│   ├── config.py             # Configuration management
│   ├── agents/
│   │   ├── coordinator.py    # Coordinator agent
│   │   ├── image_agent.py    # Image description agent
│   │   └── pdf_agent.py      # PDF processing agent
│   └── utils/
│       └── logging_config.py # Logging setup
├── tests/
│   ├── test_coordinator.py
│   ├── test_image_agent.py
│   └── test_pdf_agent.py
├── examples/
│   ├── sample_images/        # Test images
│   └── sample_pdfs/          # Test PDFs
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **Google Gemini Team** for the powerful vision API
- **PyPDF2 Contributors** for PDF processing capabilities
- **Accessibility Community** for highlighting the critical need for accessible content
- **Kaggle AI Agents Competition** for the opportunity to build this solution

---

## 📞 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ for accessibility. Powered by Google Gemini 2.0 Flash.**
