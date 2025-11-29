# 🚀 Quick Start Guide

Get AccessibleAI running in 5 minutes!

## Step 1: Clone & Setup (2 minutes)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/accessible-ai-capstone.git
cd accessible-ai-capstone

# Create virtual environment
python -m venv agent-env

# Activate (Windows)
agent-env\Scripts\activate

# Activate (Mac/Linux)
source agent-env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Get API Key (1 minute)

1. Go to https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

## Step 3: Configure (1 minute)

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your API key
# GEMINI_API_KEY=paste_your_key_here
```

## Step 4: Add Test Files (1 minute)

Place test files in:
- `examples/sample_images/test_image_1.jpg` (any image)
- `examples/sample_pdfs/test_doc_1.pdf` (any PDF)

## Step 5: Run Demo! (30 seconds)

```bash
python demo.py
```

## That's it! 🎉

You should see:
- Image descriptions being generated
- PDF text being extracted
- Batch processing results
- Detailed image analysis

## Next Steps

1. **Try the API directly:**
   ```python
   from src.agents.coordinator import CoordinatorAgent
   coordinator = CoordinatorAgent()
   result = coordinator.process_file("your_file.jpg")
   print(result['result']['alt_text'])
   ```

2. **Run tests:**
   ```bash
   python run_tests.py
   ```

3. **Deploy to production:**
   ```bash
   adk deploy --project-id=YOUR_PROJECT_ID
   ```

## Troubleshooting

**"Configuration error"**
- Make sure you created the `.env` file
- Make sure you added your API key to it

**"No sample files found"**
- Add images to `examples/sample_images/`
- Add PDFs to `examples/sample_pdfs/`

**"Import error"**
- Make sure you activated the virtual environment
- Run `pip install -r requirements.txt` again

---

Need help? Check the full [README.md](README.md) for detailed documentation.
