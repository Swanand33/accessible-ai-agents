# Sample PDFs

Place your test PDF documents here for testing the PDF Processing Agent.

## Recommended Test PDFs

1. **test_doc_1.pdf** - A simple 1-2 page document
2. **test_doc_2.pdf** - A multi-page document (5-10 pages)

## Supported Features

- Multi-page PDFs
- Text extraction
- Handles up to 100 pages (configurable)

## Where to Get Sample PDFs

- Create your own in Word/Google Docs and export as PDF
- Download from [Project Gutenberg](https://www.gutenberg.org) (free books)
- Use any document, research paper, or report

## Testing Tips

1. **Text PDFs**: Make sure PDFs contain actual text (not scanned images)
2. **Size**: Start with smaller PDFs (< 10 pages) for faster testing
3. **Variety**: Test with different document types

## Not Supported (Yet)

- Scanned PDFs (images of text) - use OCR preprocessing
- Password-protected PDFs
- Forms with fillable fields

---

Once you add PDFs here, run:
```bash
python demo.py
```
