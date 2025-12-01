# AccessibleAI - ADK Version

**Multi-Agent System for Digital Content Accessibility**
Built with Google Agent Development Kit (ADK)

Making digital content accessible for 2.2 billion people with vision impairment.

---

## 🎯 What Is This?

This is the **ADK-compliant version** of AccessibleAI, rebuilt using Google's Agent Development Kit framework for the Kaggle 5-Day AI Agents Intensive Capstone Project.

### Key Difference from Original Version
- **Original:** Direct Gemini API calls with custom multi-agent architecture
- **ADK Version:** Uses ADK framework with proper agent definitions, tools, and orchestration

---

## 🏗️ Architecture

### Three ADK Agents

1. **Image Description Agent**
   - Generates accessible alt-text using Gemini Vision
   - Tool: `generate_image_description_tool()`
   - Model: `gemini-2.0-flash-exp`

2. **PDF Processing Agent**
   - Extracts text from PDFs for screen readers
   - Tool: `extract_pdf_text_tool()`
   - Model: `gemini-2.0-flash-exp`

3. **Root Coordinator Agent**
   - Orchestrates image and PDF agents
   - Detects file types and routes to appropriate agent
   - Tools: All tools + sub-agents

### ADK Multi-Agent Pattern

```python
from google.adk.agents.llm_agent import Agent

# Specialized agents
image_agent = Agent(model='gemini-2.0-flash-exp', tools=[...])
pdf_agent = Agent(model='gemini-2.0-flash-exp', tools=[...])

# Coordinator with sub-agents
root_agent = Agent(
    model='gemini-2.0-flash-exp',
    tools=[...],
    agents=[image_agent, pdf_agent]  # Sub-agents!
)
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `google-adk` - Agent Development Kit framework
- `google-generativeai` - Gemini API
- `Pillow` - Image processing
- `PyPDF2` - PDF text extraction

### 2. Configure API Key

Create `.env` file:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 3. Run with ADK

```bash
# Interactive CLI mode
adk run

# Web interface (recommended)
cd .. && adk web --port 8000
```

Then open `http://localhost:8000` in your browser.

---

## 💻 Usage Examples

### Process an Image

```python
# ADK automatically routes to image_agent
result = root_agent.run("Process this image: examples/sample_images/campus.jpg")
```

### Process a PDF

```python
# ADK automatically routes to pdf_agent
result = root_agent.run("Extract text from: examples/sample_pdfs/syllabus.pdf")
```

### Batch Processing

```python
files = [
    "image1.jpg",
    "document.pdf",
    "image2.png"
]

for file in files:
    result = root_agent.run(f"Process: {file}")
    print(result)
```

---

## 🔧 How It Works (ADK Framework)

### Tool Definition
ADK tools are Python functions with type hints and docstrings:

```python
def generate_image_description_tool(
    image_path: str,
    detail_level: str = "concise"
) -> Dict[str, Any]:
    """
    Generate accessible alt-text for images.

    Args:
        image_path: Path to image file
        detail_level: "concise" or "detailed"

    Returns:
        Dictionary with alt-text and metadata
    """
    # Tool implementation...
```

### Agent Definition
Agents are created with ADK's `Agent` class:

```python
from google.adk.agents.llm_agent import Agent

agent = Agent(
    model='gemini-2.0-flash-exp',
    name='agent_name',
    description="What this agent does",
    instruction="How to behave and what to do",
    tools=[tool1, tool2],  # Tools this agent can use
    agents=[sub_agent1]     # Sub-agents for orchestration
)
```

### Multi-Agent Orchestration
The root agent coordinates sub-agents:

```python
root_agent = Agent(
    name='coordinator',
    agents=[image_agent, pdf_agent],  # Sub-agents
    instruction="Route files to the right agent"
)
```

---

## 📊 Capabilities Demonstrated

This project demonstrates **5 core capabilities** from the course:

| # | Capability | Evidence |
|---|------------|----------|
| 1 | **Tools & Integration** | Gemini Vision API + PyPDF2 tools |
| 2 | **Multi-Agent Orchestration** | ADK coordinator pattern with 3 agents |
| 3 | **Model Integration** | Gemini 2.0 Flash (latest experimental) |
| 4 | **Error Handling** | Comprehensive try-except in all tools |
| 5 | **Production Ready** | ADK framework, proper structure, documentation |

**Meets requirement:** ✅ 3+ capabilities (we have 5!)

---

## 🎓 ADK Framework Benefits

### Why ADK vs Custom Implementation?

| Feature | Custom (Original) | ADK (This Version) |
|---------|------------------|-------------------|
| Framework | Manual | Google ADK ✅ |
| Agent Structure | Custom classes | ADK `Agent` class ✅ |
| Tool System | Custom decorators | ADK tools ✅ |
| Multi-Agent | Manual routing | ADK orchestration ✅ |
| Deployment | Manual | ADK deployment tools ✅ |
| Evaluation | pytest | ADK eval framework ✅ |

---

## 📁 Project Structure

```
adk_version/
├── agent.py              # Main ADK agent definitions
├── __init__.py           # Package init
├── .env                  # API keys (gitignored)
├── requirements.txt      # Dependencies
└── README.md             # This file
```

---

## 🧪 Testing

```bash
# Test agent initialization
python agent.py

# Run with ADK CLI
adk run

# Run web interface
adk web --port 8000
```

---

## 🔒 Security & Best Practices

- ✅ API keys in `.env` (never committed)
- ✅ Input validation in all tools
- ✅ Error handling with try-except
- ✅ Type hints for all functions
- ✅ Docstrings for all tools and agents
- ✅ ADK framework best practices

---

## 📝 Differences from Original Version

| Aspect | Original | ADK Version |
|--------|----------|-------------|
| File structure | `src/agents/` folder | Single `agent.py` file |
| Agent classes | Custom Python classes | ADK `Agent` objects |
| API calls | Direct `genai.GenerativeModel()` | ADK handles internally |
| Multi-agent | Custom coordinator | ADK `agents=[]` parameter |
| Execution | `python demo.py` | `adk run` or `adk web` |
| Tests | pytest with custom tests | ADK testing framework |

---

## 🎯 Competition Compliance

**Kaggle 5-Day AI Agents Intensive Capstone Requirements:**

- ✅ **Uses ADK framework** (google-adk package)
- ✅ **Demonstrates 3+ capabilities** (we have 5)
- ✅ **Solves real problem** (digital accessibility)
- ✅ **Multi-agent architecture** (coordinator + 2 specialists)
- ✅ **Production-ready** (error handling, documentation)

---

## 🚀 Deployment Options

### Option 1: Local Development
```bash
adk run  # CLI mode
```

### Option 2: Web Interface
```bash
adk web --port 8000
```

### Option 3: Cloud Run (Production)
```bash
adk deploy --project-id=YOUR_PROJECT_ID
```

### Option 4: Vertex AI Agent Engine
```bash
adk deploy --agent-engine
```

---

## 📚 Learn More

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Python Quickstart](https://google.github.io/adk-docs/get-started/python/)
- [Original Project README](../README.md)

---

## 🏆 About This Project

**Competition:** Kaggle - 5-Day AI Agents Intensive Capstone
**Track:** Agents for Good - Accessibility
**Framework:** Google Agent Development Kit (ADK)
**Impact:** Making digital content accessible for 2.2 billion people with vision impairment

**GitHub:** [Original Version](https://github.com/Swanand33/accessible-ai-agents)

---

**Built with ❤️ using Google ADK**
