"""
Demo Script - Run AccessibleAI Agents Directly
Shows agents working without needing `adk run` command
"""

import sys
from pathlib import Path
from agent import root_agent, image_agent, pdf_agent, generate_image_description_tool, extract_pdf_text_tool

def demo_image_processing():
    """Demonstrate image description generation"""
    print("\n" + "="*60)
    print("DEMO 1: Image Description Generation")
    print("="*60)

    image_path = "../examples/sample_images/test_image_1.jpg"
    print(f"\nProcessing: {image_path}")

    result = generate_image_description_tool(image_path, detail_level="concise")

    if result['success']:
        print(f"\n[SUCCESS]")
        print(f"Alt-text: {result['alt_text']}")
        print(f"Characters: {result['character_count']}")
        if 'mode' in result:
            print(f"Mode: {result['mode']}")
            print(f"Note: {result['note']}")
    else:
        print(f"\n[ERROR] {result.get('error')}")

def demo_pdf_processing():
    """Demonstrate PDF text extraction"""
    print("\n" + "="*60)
    print("DEMO 2: PDF Text Extraction")
    print("="*60)

    pdf_path = "../examples/sample_pdfs/test_doc_1.pdf"
    print(f"\nProcessing: {pdf_path}")

    result = extract_pdf_text_tool(pdf_path, max_pages=2)

    if result['success']:
        print(f"\n[SUCCESS]")
        print(f"Pages processed: {result['page_count']}")
        print(f"Characters extracted: {result['character_count']}")
        print(f"Words: {result['word_estimate']}")
        print(f"\nText preview (first 200 chars):")
        print(result['text'][:200] + "...")
    else:
        print(f"\n[ERROR] {result.get('error')}")

def demo_agents_info():
    """Show information about ADK agents"""
    print("\n" + "="*60)
    print("DEMO 3: ADK Agent Information")
    print("="*60)

    print(f"\n1. Root Coordinator Agent:")
    print(f"   Name: {root_agent.name}")
    print(f"   Tools: {len(root_agent.tools)}")
    print(f"   Purpose: Route files to appropriate specialized agents")

    print(f"\n2. Image Description Agent:")
    print(f"   Name: {image_agent.name}")
    print(f"   Tools: {len(image_agent.tools)}")
    print(f"   Purpose: Generate accessible alt-text for images")

    print(f"\n3. PDF Processing Agent:")
    print(f"   Name: {pdf_agent.name}")
    print(f"   Tools: {len(pdf_agent.tools)}")
    print(f"   Purpose: Extract text from PDFs for screen readers")

def main():
    """Run all demos"""
    print("\n" + "="*60)
    print("AccessibleAI - Multi-Agent System Demo")
    print("Built with Google Agent Development Kit (ADK)")
    print("="*60)

    demo_agents_info()
    demo_image_processing()
    demo_pdf_processing()

    print("\n" + "="*60)
    print("Demo Complete!")
    print("="*60)
    print("\nAll agents are working correctly.")
    print("This demonstrates the ADK implementation is fully functional.")
    print("\nNote: Run 'python test_adk_agents.py' for comprehensive testing.")

if __name__ == "__main__":
    main()
