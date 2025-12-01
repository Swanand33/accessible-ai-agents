# AccessibleAI: Multi-Agent System for Digital Content Accessibility

**Kaggle 5-Day AI Agents Intensive Course - Capstone Project**
**Track:** Agents for Good
**GitHub:** https://github.com/Swanand33/accessible-ai-agents

---

## Quick Links

- **GitHub Repository:** https://github.com/Swanand33/accessible-ai-agents
- **ADK Implementation:** `/adk_version/` folder
- **Capabilities Documentation:** `/CAPABILITIES.md`
- **Quick Start Guide:** `/README.md`

---

## Project Summary

AccessibleAI is a multi-agent system built with Google's Agent Development Kit (ADK) that makes digital content accessible for 2.2 billion people with vision impairment worldwide. The system automatically generates alt-text for images and extracts text from PDFs, enabling screen readers to make content accessible.

### Key Features
- **3 specialized ADK agents** with coordinator pattern
- **Gemini Vision API integration** for intelligent alt-text generation
- **PDF text extraction** with structure preservation
- **Production-ready** with comprehensive testing and documentation
- **Solves real problem** affecting billions of people

---

## Technical Implementation

### Framework: Google ADK ✅
Fully implemented using Google's Agent Development Kit as taught in the course.

**Files:**
- `adk_version/agent.py` - Complete ADK implementation with 3 agents
- `adk_version/agent.yaml` - ADK deployment configuration
- `adk_version/test_adk_agents.py` - Comprehensive test suite

**Evidence:**
```python
from google.adk.agents.llm_agent import Agent

# Three ADK agents with proper configuration
image_agent = Agent(
    model='gemini-pro-vision',
    name='image_description_agent',
    tools=[generate_image_description_tool]
)

pdf_agent = Agent(
    model='gemini-pro-vision',
    name='pdf_processing_agent',
    tools=[extract_pdf_text_tool]
)

root_agent = Agent(
    model='gemini-pro-vision',
    name='accessibility_coordinator',
    tools=[detect_file_type_tool, generate_image_description_tool, extract_pdf_text_tool]
)
```

---

## Capabilities Demonstrated

We demonstrate **6 core capabilities** from the course (exceeds 3+ requirement):

| # | Capability | Evidence | Day |
|---|------------|----------|-----|
| 1 | **Google ADK Framework** | Full ADK implementation | 1-5 |
| 2 | **Multi-Agent Orchestration** | 3 specialized agents | 1 |
| 3 | **Tools & Integration** | Gemini Vision + PyPDF2 | 2 |
| 4 | **Error Handling** | Comprehensive error handling | 4 |
| 5 | **Production Readiness** | Tests, docs, deployment | 5 |
| 6 | **Real-World Impact** | Accessibility for 2.2B people | All |

**Detailed breakdown:** See `/CAPABILITIES.md` in repository

---

## Multi-Agent Architecture

### Agent 1: Root Coordinator (`accessibility_coordinator`)
- **Purpose:** Orchestrates image and PDF processing
- **Responsibilities:** File type detection, routing, result aggregation
- **Tools:** All 3 tools (detect, image, PDF)

### Agent 2: Image Description Agent (`image_description_agent`)
- **Purpose:** Generate accessible alt-text for images
- **Integration:** Gemini Vision API
- **Features:** Concise and detailed description modes

### Agent 3: PDF Processing Agent (`pdf_processing_agent`)
- **Purpose:** Extract text from PDFs for screen readers
- **Integration:** PyPDF2 library
- **Features:** Multi-page processing, structure preservation

**Why Multi-Agent:**
1. **Specialization** - Each agent optimized for its domain
2. **Scalability** - Easy to add new content types
3. **Fault Isolation** - Failures don't cascade
4. **Maintainability** - Clear separation of concerns

---

## Tools Integrated

### Tool 1: Image Description Tool
**Integration:** Google Gemini Vision API
```python
def generate_image_description_tool(image_path: str, detail_level: str = "concise"):
    """Generate accessible alt-text for images using Gemini Vision."""
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([prompt, image])
    return {"success": True, "alt_text": alt_text, ...}
```

### Tool 2: PDF Text Extraction Tool
**Integration:** PyPDF2 Library
```python
def extract_pdf_text_tool(pdf_path: str, max_pages: int = 100):
    """Extract text from PDF documents."""
    pdf_reader = PyPDF2.PdfReader(file)
    # Extract with page structure preservation
    return {"success": True, "text": full_text, ...}
```

### Tool 3: File Type Detection Tool
**Purpose:** Identify file types for intelligent routing

---

## Real-World Impact

### The Problem
- **2.2 billion people** worldwide have vision impairment
- **Only 3% of web images** have alt-text
- **95% of PDFs** are inaccessible to screen readers

### Our Solution
Automated, intelligent accessibility at scale:
- **Images:** Auto-generated alt-text in seconds (vs. 2-5 minutes manually)
- **PDFs:** Text extraction with structure preservation
- **Scale:** Can process thousands of documents per day

### Use Cases
1. **Educational institutions** - Make course materials accessible
2. **Libraries** - Convert archives to accessible formats
3. **Businesses** - Comply with accessibility laws (ADA, WCAG)
4. **NGOs** - Democratize access to information

**Impact:** Potential to help millions of people access digital content

---

## Production Readiness

### Testing
- **6 comprehensive tests** covering all agents and tools
- **File:** `adk_version/test_adk_agents.py`
- Tests: file detection, image processing, PDF extraction, agent initialization, end-to-end workflows

### Documentation
- **Comprehensive README** (500+ lines)
- **Quick Start Guide**
- **API Reference**
- **Deployment instructions**
- **Capabilities documentation**

### Configuration
- Environment variable management
- Secure API key handling (`.env` file)
- No hardcoded secrets
- Deployment-ready structure

### Error Handling
- Input validation on all tools
- Try-except blocks for all operations
- Structured error responses
- Graceful degradation

---

## How to Run

### Prerequisites
```bash
pip install -r adk_version/requirements.txt
```

### Setup
1. Clone repository
2. Add API key to `.env` file: `GOOGLE_API_KEY=your_key`
3. Navigate to `adk_version/`

### Run with ADK
```bash
# CLI mode
adk run

# Web interface
adk web --port 8000
```

### Test
```bash
python test_adk_agents.py
```

---

## Technical Excellence

### Code Quality
- ✅ Type hints on all functions
- ✅ Comprehensive docstrings
- ✅ Clean, readable code structure
- ✅ Proper error handling
- ✅ No code duplication

### ADK Best Practices
- ✅ Proper agent configuration
- ✅ Tool registration and schemas
- ✅ Deployment configuration (agent.yaml)
- ✅ Environment management
- ✅ Production-ready structure

### Documentation
- ✅ README with examples
- ✅ Quick start guide
- ✅ API documentation
- ✅ Capabilities mapping
- ✅ Architecture diagrams (in main README)

---

## Competition Compliance

| Requirement | Status | Evidence |
|------------|--------|----------|
| Uses Google ADK | ✅ YES | `adk_version/agent.py` + `agent.yaml` |
| 3+ capabilities | ✅ YES | 6 capabilities (see CAPABILITIES.md) |
| Multi-agent | ✅ YES | 3 specialized agents |
| Real problem | ✅ YES | Accessibility for 2.2B people |
| Production-ready | ✅ YES | Tests, docs, deployment config |
| Documentation | ✅ YES | Comprehensive README + guides |
| Code quality | ✅ YES | Type hints, error handling, clean code |

**Overall Compliance:** 7/7 (100%) ✅

---

## What Makes This Project Stand Out

1. **Exceeds requirements** - 6 capabilities instead of 3
2. **Real social impact** - Agents for Good track alignment
3. **Production-ready** - Not just a demo, actually deployable
4. **Proper ADK implementation** - Follows framework best practices
5. **Comprehensive testing** - 6 test scenarios with automation
6. **Excellent documentation** - Easy to understand and use
7. **Scalable architecture** - Multi-agent pattern enables growth

---

## Future Enhancements

The multi-agent architecture makes it easy to add:
- **Video captioning agent** - Automatically generate subtitles
- **Audio transcription agent** - Convert speech to text
- **HTML optimization agent** - Improve web accessibility
- **Memory capability** - Remember user preferences
- **Evaluation framework** - ADK-based quality metrics

---

## Repository Structure

```
accessible-ai-agents/
├── adk_version/              # ADK implementation (MAIN)
│   ├── agent.py             # 3 ADK agents implementation
│   ├── agent.yaml           # ADK deployment configuration
│   ├── test_adk_agents.py   # Comprehensive test suite
│   ├── requirements.txt     # Dependencies
│   └── README.md            # ADK-specific documentation
├── src/                     # Original implementation
├── tests/                   # Additional tests
├── docs/                    # Documentation
├── examples/                # Sample files
├── CAPABILITIES.md          # Detailed capabilities breakdown
├── README.md                # Main documentation
└── .env.example             # Environment template
```

---

## Conclusion

AccessibleAI demonstrates:
- ✅ **Technical excellence** - Proper ADK implementation
- ✅ **Social impact** - Solving real accessibility problems
- ✅ **Production readiness** - Tested, documented, deployable
- ✅ **Learning depth** - 6 capabilities from the course

This is not just a capstone project—it's a system that could actually help millions of people access digital content, built with the proper tools and frameworks learned in the 5-Day AI Agents Intensive Course.

---

## For Evaluators

**All code is available on GitHub:** https://github.com/Swanand33/accessible-ai-agents

**Key files to review:**
1. `/adk_version/agent.py` - Main ADK implementation
2. `/adk_version/agent.yaml` - Deployment configuration
3. `/CAPABILITIES.md` - Detailed capability documentation
4. `/README.md` - Complete project documentation
5. `/adk_version/test_adk_agents.py` - Test suite

**The system is ready for deployment and evaluation.**

---

**Built with Google ADK | Agents for Good | Making accessibility accessible**

