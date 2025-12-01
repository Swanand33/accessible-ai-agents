"""
Test script for ADK Agents - Comprehensive Testing
Tests all agents and tools with real files
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agent import (
    root_agent,
    image_agent,
    pdf_agent,
    generate_image_description_tool,
    extract_pdf_text_tool,
    detect_file_type_tool,
    ADK_AVAILABLE
)

def test_file_detection():
    """Test file type detection tool"""
    print("\n" + "="*60)
    print("TEST 1: File Type Detection")
    print("="*60)

    # Test with image
    image_path = "../examples/sample_images/test_image_1.jpg"
    result = detect_file_type_tool(image_path)
    print(f"Image file test: {result}")
    assert result['success'] == True
    assert result['file_type'] == 'image'
    print("[PASS] Image detection PASSED")

    # Test with PDF
    pdf_path = "../examples/sample_pdfs/test_doc_1.pdf"
    result = detect_file_type_tool(pdf_path)
    print(f"PDF file test: {result}")
    assert result['success'] == True
    assert result['file_type'] == 'pdf'
    print("[PASS] PDF detection PASSED")

    print("\n[SUCCESS] File detection tests PASSED")
    return True

def test_image_description():
    """Test image description generation"""
    print("\n" + "="*60)
    print("TEST 2: Image Description Tool")
    print("="*60)

    image_path = "../examples/sample_images/test_image_1.jpg"

    # Test concise description
    result = generate_image_description_tool(image_path, detail_level="concise")
    print(f"\nConcise description result:")
    print(f"Success: {result['success']}")
    if result['success']:
        print(f"Alt-text: {result['alt_text']}")
        print(f"Characters: {result['character_count']}")
        assert len(result['alt_text']) > 10
        print("[PASS] Concise description PASSED")
    else:
        print(f"[ERROR] Image processing failed: {result.get('error', 'Unknown error')}")
        return False

    # Test detailed description
    result = generate_image_description_tool(image_path, detail_level="detailed")
    print(f"\nDetailed description result:")
    print(f"Success: {result['success']}")
    if result['success']:
        print(f"Alt-text: {result['alt_text'][:200]}...")
        print(f"Characters: {result['character_count']}")
        assert len(result['alt_text']) > 50
        print("[PASS] Detailed description PASSED")

    print("\n[SUCCESS] Image description tests PASSED")
    return True

def test_pdf_extraction():
    """Test PDF text extraction"""
    print("\n" + "="*60)
    print("TEST 3: PDF Text Extraction Tool")
    print("="*60)

    pdf_path = "../examples/sample_pdfs/test_doc_1.pdf"

    result = extract_pdf_text_tool(pdf_path)
    print(f"\nPDF extraction result:")
    print(f"Success: {result['success']}")
    if result['success']:
        print(f"Pages: {result['page_count']}")
        print(f"Characters: {result['character_count']}")
        print(f"Words: {result['word_estimate']}")
        print(f"Text preview: {result['text'][:200]}...")
        assert result['page_count'] > 0
        assert len(result['text']) > 0
        print("[PASS] PDF extraction PASSED")

    print("\n[SUCCESS] PDF extraction tests PASSED")
    return True

def test_adk_agents():
    """Test ADK agents are properly initialized"""
    print("\n" + "="*60)
    print("TEST 4: ADK Agent Initialization")
    print("="*60)

    if not ADK_AVAILABLE:
        print("[ERROR] ADK not available!")
        return False

    # Check root agent
    assert root_agent is not None
    assert root_agent.name == 'accessibility_coordinator'
    assert len(root_agent.tools) == 3
    print(f"[PASS] Root agent initialized: {root_agent.name}")
    print(f"[PASS] Tools available: {len(root_agent.tools)}")

    # Check image agent
    assert image_agent is not None
    assert image_agent.name == 'image_description_agent'
    assert len(image_agent.tools) == 1
    print(f"[PASS] Image agent initialized: {image_agent.name}")

    # Check PDF agent
    assert pdf_agent is not None
    assert pdf_agent.name == 'pdf_processing_agent'
    assert len(pdf_agent.tools) == 1
    print(f"[PASS] PDF agent initialized: {pdf_agent.name}")

    print("\n[SUCCESS] All ADK agents initialized correctly")
    return True

def test_end_to_end_image():
    """Test end-to-end image processing workflow"""
    print("\n" + "="*60)
    print("TEST 5: End-to-End Image Processing")
    print("="*60)

    # This would test the full agent conversation flow
    # For now, we test the tools directly
    image_path = "../examples/sample_images/test_image_1.jpg"

    # 1. Detect file type
    file_info = detect_file_type_tool(image_path)
    print(f"1. File detected as: {file_info['file_type']}")

    # 2. Process image
    result = generate_image_description_tool(image_path)
    print(f"2. Image processed: {result['success']}")
    print(f"3. Alt-text generated: {len(result.get('alt_text', ''))} chars")

    assert file_info['file_type'] == 'image'
    assert result['success'] == True

    print("\n[SUCCESS] End-to-end image processing PASSED")
    return True

def test_end_to_end_pdf():
    """Test end-to-end PDF processing workflow"""
    print("\n" + "="*60)
    print("TEST 6: End-to-End PDF Processing")
    print("="*60)

    pdf_path = "../examples/sample_pdfs/test_doc_1.pdf"

    # 1. Detect file type
    file_info = detect_file_type_tool(pdf_path)
    print(f"1. File detected as: {file_info['file_type']}")

    # 2. Process PDF
    result = extract_pdf_text_tool(pdf_path)
    print(f"2. PDF processed: {result['success']}")
    print(f"3. Text extracted: {result.get('character_count', 0)} chars")

    assert file_info['file_type'] == 'pdf'
    assert result['success'] == True

    print("\n[SUCCESS] End-to-end PDF processing PASSED")
    return True

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("RUNNING COMPREHENSIVE ADK AGENT TESTS")
    print("="*60)

    tests = [
        ("File Detection", test_file_detection),
        ("Image Description", test_image_description),
        ("PDF Extraction", test_pdf_extraction),
        ("ADK Agents", test_adk_agents),
        ("E2E Image Processing", test_end_to_end_image),
        ("E2E PDF Processing", test_end_to_end_pdf),
    ]

    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n[ERROR] {name} failed: {str(e)}")
            results.append((name, False))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for name, success in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status} {name}")

    total = len(results)
    passed = sum(1 for _, s in results if s)
    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n[SUCCESS] ALL TESTS PASSED! ADK agents are working correctly.")
        return True
    else:
        print(f"\n[WARNING] {total - passed} tests failed. Review errors above.")
        return False

if __name__ == "__main__":
    if not ADK_AVAILABLE:
        print("[ERROR] Google ADK not installed. Cannot run tests.")
        sys.exit(1)

    success = run_all_tests()
    sys.exit(0 if success else 1)
