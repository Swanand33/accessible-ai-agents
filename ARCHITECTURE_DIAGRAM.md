# AccessibleAI - System Architecture Diagram

## High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                           USER INPUT                                │
│                    (Image files / PDF files)                        │
│                                                                     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                      COORDINATOR AGENT                              │
│                     (Root Orchestrator)                             │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │  1. Accept file input                                       │   │
│  │  2. Detect file type (.jpg, .png, .pdf, etc.)              │   │
│  │  3. Route to specialized agent                              │   │
│  │  4. Aggregate results                                       │   │
│  │  5. Generate summary report                                 │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────┬───────────────────────────────────┬───────────────────┘
              │                                   │
              │                                   │
    ┌─────────▼──────────┐           ┌───────────▼──────────┐
    │                    │           │                      │
    │  IMAGE AGENT       │           │   PDF AGENT          │
    │  (Vision AI)       │           │   (Text Extraction)  │
    │                    │           │                      │
    └─────────┬──────────┘           └───────────┬──────────┘
              │                                   │
              │                                   │
              ▼                                   ▼
    ┌──────────────────┐              ┌────────────────────┐
    │  Gemini 2.0      │              │     PyPDF2         │
    │  Flash Vision    │              │  Text Extractor    │
    │     API          │              │                    │
    └─────────┬────────┘              └───────────┬────────┘
              │                                   │
              │                                   │
              ▼                                   ▼
    ┌──────────────────┐              ┌────────────────────┐
    │  Descriptive     │              │  Structured Text   │
    │  Alt-Text        │              │  + Metadata        │
    └─────────┬────────┘              └───────────┬────────┘
              │                                   │
              └───────────────┬───────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │                               │
              │    ACCESSIBLE CONTENT         │
              │  (JSON Response Format)       │
              │                               │
              └───────────────┬───────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │                               │
              │         USER OUTPUT           │
              │  (Screen readers, TTS, etc.)  │
              │                               │
              └───────────────────────────────┘
```

---

## Detailed Agent Responsibilities

```
╔═══════════════════════════════════════════════════════════════════╗
║                     COORDINATOR AGENT                             ║
╠═══════════════════════════════════════════════════════════════════╣
║ Model: gemini-2.0-flash-exp                                       ║
║ Role: Root orchestrator and workflow manager                      ║
║                                                                   ║
║ Capabilities:                                                     ║
║   ✓ File type detection (extension-based)                        ║
║   ✓ Intelligent routing to specialized agents                    ║
║   ✓ Batch processing support (multiple files)                    ║
║   ✓ Result aggregation and formatting                            ║
║   ✓ Summary report generation                                    ║
║   ✓ Error handling and fault isolation                           ║
║                                                                   ║
║ Input: file_path (str), detailed (bool)                           ║
║ Output: {success, file_type, result, error}                       ║
╚═══════════════════════════════════════════════════════════════════╝

           │                                    │
           │                                    │
           ▼                                    ▼

╔════════════════════════════╗    ╔════════════════════════════╗
║   IMAGE DESCRIPTION AGENT  ║    ║   PDF PROCESSING AGENT     ║
╠════════════════════════════╣    ╠════════════════════════════╣
║ Model: gemini-2.0-flash    ║    ║ Library: PyPDF2            ║
║ Tool: Gemini Vision API    ║    ║ Processing: Local          ║
║                            ║    ║                            ║
║ Capabilities:              ║    ║ Capabilities:              ║
║  ✓ Image analysis          ║    ║  ✓ Text extraction         ║
║  ✓ Alt-text generation     ║    ║  ✓ Multi-page support      ║
║  ✓ Concise mode (2-3 sent) ║    ║  ✓ Encrypted PDF handling  ║
║  ✓ Detailed mode (5+ sent) ║    ║  ✓ Page statistics         ║
║  ✓ Text transcription      ║    ║  ✓ Character counting      ║
║  ✓ Context awareness       ║    ║  ✓ Error recovery          ║
║  ✓ Batch processing        ║    ║  ✓ Batch processing        ║
║                            ║    ║                            ║
║ Formats: JPG, PNG, WebP,   ║    ║ Formats: PDF (all versions)║
║          GIF, BMP          ║    ║                            ║
║                            ║    ║ Safety: 100 page limit     ║
║ Input: image_path, detail  ║    ║ Input: pdf_path, max_pages ║
║ Output: {alt_text, ...}    ║    ║ Output: {text, pages, ...} ║
╚════════════════════════════╝    ╚════════════════════════════╝
```

---

## Data Flow Diagram

```
START
  │
  ├─→ User provides file path(s)
  │
  ▼
┌─────────────────────────────┐
│ CoordinatorAgent.           │
│ process_file(path)          │
└───────────┬─────────────────┘
            │
            ├─→ Validate file exists
            │
            ▼
      ┌───────────┐
      │ Detect    │
      │ file type │
      └─────┬─────┘
            │
            ├──────┬──────┐
            │      │      │
      .jpg/.png  .pdf   other
            │      │      │
            │      │      └──→ Error: Unsupported
            │      │
            ▼      ▼
     ┌──────────┐ ┌──────────┐
     │  Image   │ │   PDF    │
     │  Agent   │ │  Agent   │
     └────┬─────┘ └────┬─────┘
          │            │
          ▼            ▼
    ┌─────────┐  ┌──────────┐
    │ Gemini  │  │ PyPDF2   │
    │ Vision  │  │ Extract  │
    └────┬────┘  └────┬─────┘
         │            │
         ▼            ▼
    [alt-text]    [text + stats]
         │            │
         └─────┬──────┘
               │
               ▼
      ┌────────────────┐
      │ Result         │
      │ Aggregation    │
      └────────┬───────┘
               │
               ▼
      ┌────────────────┐
      │ JSON Response  │
      │ {success, ...} │
      └────────┬───────┘
               │
               ▼
           RETURN TO USER
```

---

## Batch Processing Flow

```
User: process_batch([file1, file2, file3, ...])
  │
  ▼
┌──────────────────────────────────────────┐
│  CoordinatorAgent                        │
│  ┌────────────────────────────────────┐  │
│  │ For each file in batch:            │  │
│  │  1. Call process_file(file)        │  │
│  │  2. Collect result                 │  │
│  │  3. Continue on errors (no crash)  │  │
│  └────────────────────────────────────┘  │
└──────────────────┬───────────────────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ Aggregate all   │
          │ results         │
          │                 │
          │ Statistics:     │
          │ - Total files   │
          │ - Successful    │
          │ - Failed        │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ Generate        │
          │ Summary Report  │
          └────────┬────────┘
                   │
                   ▼
            RETURN TO USER
```

---

## Error Handling Flow

```
Any Operation
      │
      ▼
  Try Block
      │
      ├─→ Success? ──→ Return {success: true, result: ...}
      │
      ▼
  Exception Caught
      │
      ├─→ FileNotFoundError ──→ Log + Return {success: false, error: "..."}
      │
      ├─→ ValueError ────────→ Log + Return {success: false, error: "..."}
      │
      ├─→ APIError ──────────→ Log + Return {success: false, error: "..."}
      │
      └─→ Other Exception ───→ Log + Return {success: false, error: "..."}

NO CRASHES - Always returns structured response
```

---

## Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  CoordinatorAgent                                    │   │
│  │  ImageDescriptionAgent                               │   │
│  │  PDFProcessingAgent                                  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│                      TOOLS LAYER                            │
│  ┌──────────────────┐  ┌─────────────────┐                 │
│  │ Google Gemini    │  │ PyPDF2          │                 │
│  │ 2.0 Flash API    │  │ (PDF Parser)    │                 │
│  └──────────────────┘  └─────────────────┘                 │
│                                                             │
│  ┌──────────────────┐  ┌─────────────────┐                 │
│  │ PIL/Pillow       │  │ Logging Module  │                 │
│  │ (Image Loading)  │  │ (Observability) │                 │
│  └──────────────────┘  └─────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│                   INFRASTRUCTURE LAYER                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Python 3.10+                                        │   │
│  │  python-dotenv (Config)                              │   │
│  │  pytest (Testing)                                    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Scalability & Extensibility

```
Current Architecture:
    CoordinatorAgent
         │
    ├────┼────┐
    │    │    │
  Image PDF  ?

Future Extensions (Easy to Add):
    CoordinatorAgent
         │
    ├────┼────┼────┼────┼────┐
    │    │    │    │    │    │
  Image PDF Audio Video HTML Table
                   Agent Agent Agent
```

**Why This Works:**
- Coordinator uses file extension detection
- Adding new agent = implement same interface
- No changes to existing agents required
- Fault isolation maintained across all agents

---

## Key Architectural Benefits

1. **Separation of Concerns**
   - Each agent has one clear responsibility
   - Changes to one agent don't affect others

2. **Fault Isolation**
   - Failure in one agent doesn't crash the system
   - Errors are caught and returned gracefully

3. **Independent Scaling**
   - Can scale Image Agent separately from PDF Agent
   - Different resource requirements handled independently

4. **Observable & Debuggable**
   - Each agent logs its operations
   - Easy to trace which agent failed and why

5. **Testable**
   - Each agent can be tested in isolation
   - Integration tests verify coordination

6. **Extensible**
   - Add new content types without modifying existing code
   - Coordinator pattern supports unlimited agents

---

**Built with production-ready multi-agent architecture for digital accessibility**
