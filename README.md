# AccessibleAI - Multi-Agent System for Digital Content Accessibility

**Kaggle 5-Day AI Agents Intensive - Capstone Project**  
**Track:** Agents for Good  
**Status:** ✅ Production Ready

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Gemini 2.0](https://img.shields.io/badge/Gemini-2.0%20Flash-orange.svg)](https://ai.google.dev/)

---

## 🎯 Quick Links

- **GitHub Repository:** [https://github.com/Swanand33/accessible-ai-agents](https://github.com/Swanand33/accessible-ai-agents)
- **Main Implementation:** `/adk_version/agent.py`
- **Full Capabilities:** `/CAPABILITIES.md`
- **Kaggle Submission:** `/KAGGLE_FINAL_SUBMISSION.md`

---

## 📖 Table of Contents

- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Capabilities Demonstrated](#-capabilities-demonstrated)
- [Quick Start](#-quick-start)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
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
  - 📚 **Education**: Textbooks, research papers, course materials
  - 💼 **Employment**: Job applications, work documents, training materials
  - 📰 **Information**: News, government documents, healthcare information

### Impact

Without accessible digital content, people with visual impairments face:
- Barriers to education and career advancement
- Inability to access critical information independently
- Dependence on others for basic tasks
- Exclusion from digital society

---

## 💡 Solution

**AccessibleAI** is a production-ready multi-agent system built with Google's Agent Development Kit (ADK) that automatically makes digital content accessible by:

1. **Generating descriptive alt-text** for images using AI vision
2. **Extracting and structuring text** from PDF documents
3. **Orchestrating specialized agents** to handle different content types seamlessly

### Why Multi-Agent Architecture?

- **Specialization**: Each agent optimized for its specific task
- **Scalability**: Easy to add new content types (audio, video, HTML, etc.)
- **Reliability**: Failure in one agent doesn't crash the entire system
- **Observability**: Track and log each agent's performance independently
- **Maintainability**: Clear separation of concerns and responsibilities

---

## ✨ Features

### 🔥 Core Features

1. **Multi-Agent Architecture** ⭐
   - **Coordinator Agent** (orchestration & routing)
   - **Image Description Agent** (Gemini Vision)
   - **PDF Processing Agent** (PyPDF2)

2. **Tools Integration** 🛠️
   - Google Gemini 2.0 Flash API (vision AI)
   - PyPDF2 (PDF text extraction)
   - Pillow (image processing)

3. **Comprehensive Observability** 📊
   - Structured logging for all operations
   - Success/failure tracking
   - Performance metrics & statistics

### 🎁 Bonus Features

- **Batch Processing**: Process multiple files at once
- **Flexible Detail Levels**: Concise or detailed descriptions
- **Error Handling**: Graceful handling of corrupt/invalid files
- **Summary Generation**: Human-readable processing reports
- **Demo Mode**: Works without API key for testing

---

## 📊 Capabilities Demonstrated

We demonstrate **6 core capabilities** from the course (exceeds 3+ requirement):

| # | Capability | Evidence | Day |
|---|-----------|----------|-----|
| 1 | **Google ADK Framework** | Full ADK implementation with 3 agents | Days 1-5 |
| 2 | **Multi-Agent Orchestration** | Coordinator pattern for agent collaboration | Day 1 |
| 3 | **Tools & Integration** | Gemini Vision API + PyPDF2 | Day 2 |
| 4 | **Error Handling** | Comprehensive error management | Day 4 |
| 5 | **Quality & Testing** | 6 tests, 100% pass rate | Day 4 |
| 6 | **Production Readiness** | Tested, documented, deployable | Day 5 |

**Total: 6 capabilities ✓ (Exceeds 3+ requirement)**

See `/CAPABILITIES.md` for detailed breakdown.

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────────────────────────────────────┐
│           COORDINATOR AGENT                     │
│       (Orchestrates workflow)                   │
└─────────────┬───────────────────────────────────┘
              │
    ┌─────────┴──────────┐
    │                    │
    ▼                    ▼
┌──────────────┐  ┌──────────────┐
│ Image Agent  │  │ PDF Agent    │
│(Gemini Vision│  │(PyPDF2)      │
│ API)         │  │              │
└──────────────┘  └──────────────┘
```

### Agent Responsibilities

**1. CoordinatorAgent** (Root Orchestrator)
- File type detection and routing
- Result aggregation
- Batch processing support
- Error handling and fault isolation

**2. ImageDescriptionAgent** (Vision AI)
- Analyzes images using Gemini Vision
- Generates descriptive alt-text
- Concise & detailed description modes

**3. PDFProcessingAgent** (Document Processing)
- Extracts text from PDFs
- Preserves document structure
- Handles multi-page documents

See `/ARCHITECTURE_DIAGRAM.md` for detailed diagrams.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### 1. Clone Repository

```bash
git clone https://github.com/Swanand33/accessible-ai-agents.git
cd accessible-ai-agents
```

### 2. Create Virtual Environment

```bash
# Create
python -m venv agent-env

# Activate (Windows)
agent-env\Scripts\activate

# Activate (Mac/Linux)
source agent-env/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure API Key

```bash
# Copy example file
cp .env.example .env

# Edit .env and add your API key
# GEMINI_API_KEY=your_actual_api_key_here
```

### 5. Run Demo

```bash
# Run with ADK (requires ADK CLI)
adk run

# Or test locally
python adk_version/test_adk_agents.py
```

---

## 💻 Usage

### Basic Python Usage

```python
import google.generativeai as genai
from adk_version.agent import generate_image_description_tool, extract_pdf_text_tool

# Configure API
genai.configure(api_key="your_api_key")

# Process an image
result = generate_image_description_tool("path/to/image.jpg", detail_level="concise")
if result['success']:
    print(f"Alt-text: {result['alt_text']}")

# Process a PDF
result = extract_pdf_text_tool("path/to/document.pdf")
if result['success']:
    print(f"Extracted {result['char_count']} characters from {result['page_count']} pages")
```

### Batch Processing

```python
# Process multiple files
files = ["image1.jpg", "image2.png", "document.pdf"]

results = {
    "total": len(files),
    "processed": [],
    "failed": []
}

for file_path in files:
    if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
        result = generate_image_description_tool(file_path)
    elif file_path.lower().endswith('.pdf'):
        result = extract_pdf_text_tool(file_path)
    
    if result['success']:
        results["processed"].append(file_path)
    else:
        results["failed"].append(file_path)

print(f"Success: {len(results['processed'])}/{len(files)}")
```

---

## 🧪 Testing

### Run All Tests

```bash
cd adk_version
python test_adk_agents.py
```

### Test Coverage

- ✅ File type detection
- ✅ Image description generation
- ✅ PDF text extraction
- ✅ ADK agent initialization
- ✅ End-to-end image processing
- ✅ End-to-end PDF processing

**Result:** 6/6 tests passing (100%)

---

## 📁 Project Structure

```
accessible-ai-agents/
├── adk_version/                    # ADK Implementation (MAIN)
│   ├── agent.py                   # 3 ADK agents + tools
│   ├── agent.yaml                 # ADK deployment config
│   ├── test_adk_agents.py         # Test suite (6 tests)
│   ├── requirements.txt           # Dependencies
│   └── README.md                  # ADK-specific docs
├── src/                           # Original implementation
│   ├── agents/
│   │   ├── coordinator.py
│   │   ├── image_agent.py
│   │   └── pdf_agent.py
│   ├── config.py
│   └── utils/
├── tests/                         # Additional tests
├── examples/                      # Sample files
│   ├── sample_images/
│   └── sample_pdfs/
├── docs/                          # Documentation
├── CAPABILITIES.md                # Capabilities breakdown
├── ARCHITECTURE_DIAGRAM.md        # System diagrams
├── KAGGLE_FINAL_SUBMISSION.md    # Competition submission
├── README.md                      # Main documentation
├── requirements.txt               # All dependencies
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
└── LICENSE                       # MIT License
```

---

## 🚀 Deployment

### Google Cloud (Agent Engine)

```bash
# Navigate to ADK version
cd adk_version

# Deploy with ADK
adk deploy --project-id=YOUR_PROJECT_ID --region=us-central1

# Check deployment
adk info

# Access web interface
adk web --port 8000
```

### Local Development

```bash
# Run ADK locally
adk run

# Run tests locally
python test_adk_agents.py

# Use as library
python
>>> from agent import generate_image_description_tool
>>> result = generate_image_description_tool("image.jpg")
```

---

## 🎓 Real-World Impact

### Use Cases

1. **Educational Institutions** 🎓
   - Make course materials accessible (ADA compliance)
   - Convert textbooks for all students
   - Support diverse learning needs

2. **Digital Libraries** 📚
   - Convert archives to accessible formats
   - Preserve historical documents accessibly
   - Enable researchers with disabilities

3. **E-commerce** 🛒
   - Product images accessible to all users
   - Improve customer experience
   - Expand market reach

4. **Government** 🏛️
   - Meet legal accessibility requirements
   - Serve constituents with disabilities
   - Ensure equal access to services

5. **Businesses** 💼
   - Comply with accessibility laws (ADA, WCAG)
   - Reduce legal liability
   - Expand customer base

### Impact Numbers

- **Manual alt-text:** 2-5 minutes per image
- **Our system:** Seconds per image
- **Cost:** $50-100/hour manual vs. $0.001 per image
- **100x faster** and more cost-effective
- **Reach:** 2.2 billion people with vision impairment

---

## 🛠️ Technical Excellence

### Code Quality
- ✅ Type hints on all functions
- ✅ Comprehensive docstrings
- ✅ Error handling with fallbacks
- ✅ Input validation
- ✅ Structured return values

### ADK Best Practices
- ✅ Proper agent configuration
- ✅ Tool registration and schemas
- ✅ Deployment configuration (agent.yaml)
- ✅ Environment management
- ✅ Production-ready structure

### Testing & Documentation
- ✅ 6 comprehensive tests (100% pass rate)
- ✅ README with examples
- ✅ API documentation
- ✅ Capabilities mapping
- ✅ Architecture diagrams

---

## 📊 Competition Compliance

| Requirement | Status | Evidence |
|-----------|--------|----------|
| Uses Google ADK | ✅ YES | `adk_version/agent.py` + `agent.yaml` |
| 3+ Capabilities | ✅ YES | 6 capabilities (see CAPABILITIES.md) |
| Multi-agent System | ✅ YES | 3 specialized agents |
| Solves Real Problem | ✅ YES | Accessibility for 2.2B people |
| Working Implementation | ✅ YES | 6/6 tests passing |
| Documentation | ✅ YES | Comprehensive README + guides |
| Production-Ready | ✅ YES | Tests, deployment config, error handling |

**Overall Compliance:** 7/7 (100%) ✅

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

- **Google Gemini Team** for the powerful vision API
- **PyPDF2 Contributors** for PDF processing capabilities
- **Accessibility Community** for highlighting critical needs
- **Kaggle** for the 5-Day AI Agents Intensive Course
- **Course Instructors** for excellent teaching

---

## 📞 Contact & Support

- **GitHub Issues:** [Report bugs or request features](https://github.com/Swanand33/accessible-ai-agents/issues)
- **GitHub Discussions:** [Ask questions or discuss ideas](https://github.com/Swanand33/accessible-ai-agents/discussions)

---

## 🎯 What's Next?

### Future Enhancements

The multi-agent architecture makes it easy to add:

- **Video Captioning Agent** - Automatic subtitle generation
- **Audio Transcription Agent** - Speech-to-text conversion
- **HTML Optimization Agent** - Web accessibility improvements
- **Memory Capability** - Remember user preferences
- **Evaluation Framework** - Quality metrics

### Roadmap

- [ ] Add video support
- [ ] Add audio transcription
- [ ] Web API interface
- [ ] Dashboard for monitoring
- [ ] Scaling for enterprise use

---

**Built with ❤️ for accessibility. Powered by Google Gemini 2.0 Flash.**

**Making digital content accessible for everyone. One file at a time.**
