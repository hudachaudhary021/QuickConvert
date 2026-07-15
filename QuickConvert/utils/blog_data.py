"""
blog_data.py
------------
Static blog content for QuickConvert. Each post is a dictionary with
metadata plus a list of section dicts (heading + paragraphs) that the
blog_post.html template renders.
"""

BLOG_POSTS = [
    {
        "slug": "word-to-pdf-without-losing-formatting",
        "title": "How to Convert Word to PDF Without Losing Formatting",
        "description": (
            "A practical guide to keeping your fonts, spacing, images, and "
            "layout intact when turning a Word document into a PDF."
        ),
        "read_time": "5 min read",
        "sections": [
            {
                "heading": "Why formatting breaks in the first place",
                "paragraphs": [
                    "Word documents store text as flexible, reflowable content — paragraphs "
                    "can wrap differently depending on the fonts installed on the viewer's "
                    "device, the page size, and even the version of Word used to open the "
                    "file. A PDF, on the other hand, is a fixed-layout format: every line "
                    "break, margin, and font is locked in place exactly as it was when the "
                    "PDF was created.",
                    "Most formatting problems happen during the conversion step itself, when "
                    "a converter has to make decisions about how to translate flexible Word "
                    "elements into fixed PDF elements. Fonts that aren't embedded, complex "
                    "tables, and unusual spacing are the most common casualties.",
                ],
            },
            {
                "heading": "Use standard, widely available fonts",
                "paragraphs": [
                    "If your document uses a font that isn't installed on the system doing "
                    "the conversion, the converter has to substitute a similar-looking font. "
                    "That substitution can shift line breaks and page counts. Sticking to "
                    "common fonts like Calibri, Arial, Times New Roman, or Georgia dramatically "
                    "reduces the chance of a mismatch.",
                ],
            },
            {
                "heading": "Check your tables and images before converting",
                "paragraphs": [
                    "Tables that are wider than the page margins, or images anchored with "
                    "unusual text-wrapping settings, are the most likely elements to shift "
                    "or overflow during conversion. Before converting, scroll through your "
                    "document in Print Layout view and confirm nothing crosses the printable "
                    "page boundary.",
                    "It also helps to avoid manually resizing images by dragging their "
                    "corners repeatedly — each resize can subtly distort the image's aspect "
                    "ratio, which becomes more noticeable once locked into a fixed PDF page.",
                ],
            },
            {
                "heading": "Review the PDF immediately after conversion",
                "paragraphs": [
                    "Always open the converted PDF and skim through every page before sharing "
                    "it. Pay particular attention to page breaks, since a paragraph that looked "
                    "fine in Word can sometimes get split awkwardly across two PDF pages. If "
                    "something looks off, adjusting the spacing in the original Word document "
                    "and reconverting is usually faster than trying to fix the PDF directly.",
                ],
            },
        ],
    },
    {
        "slug": "pdf-to-word-conversion-issues",
        "title": "Why Your PDF to Word Conversion Looks Messy (And How to Fix It)",
        "description": (
            "Understanding the common causes of broken formatting when converting "
            "PDFs back into editable Word documents — and how to work around them."
        ),
        "read_time": "6 min read",
        "sections": [
            {
                "heading": "PDFs were never meant to be edited",
                "paragraphs": [
                    "A PDF doesn't actually store paragraphs, tables, or headings the way "
                    "Word does. Instead, it stores individual pieces of text positioned at "
                    "exact coordinates on the page, along with separate instructions for "
                    "lines, shapes, and images. Converting a PDF back to Word means a "
                    "converter has to reverse-engineer that positioned text into a document "
                    "structure — guessing where paragraphs start and end, which lines belong "
                    "to which table cell, and so on.",
                    "This is why PDF-to-Word conversion is inherently harder than Word-to-PDF, "
                    "and why some formatting loss is expected, especially with complex layouts.",
                ],
            },
            {
                "heading": "Scanned PDFs need OCR, not just conversion",
                "paragraphs": [
                    "If a PDF was created by scanning a physical page, it may contain no real "
                    "text at all — just a picture of text. A standard PDF-to-Word converter "
                    "can't extract text from an image; it needs Optical Character Recognition "
                    "(OCR) first, which is a separate process. If your converted document comes "
                    "back completely empty or full of garbled symbols, this is almost always "
                    "the reason.",
                    "A quick way to check: try selecting text inside the original PDF with your "
                    "finger or cursor. If nothing highlights, it's an image-based scan and will "
                    "need an OCR-capable tool rather than a standard converter.",
                ],
            },
            {
                "heading": "Multi-column layouts and tables are the trickiest",
                "paragraphs": [
                    "Newsletters, brochures, and academic papers often use multiple text "
                    "columns or nested tables. Converters can sometimes misread the reading "
                    "order in these layouts, resulting in sentences that jump between columns "
                    "in the wrong sequence. If you're converting this kind of document, it's "
                    "worth double-checking the reading order in the resulting Word file rather "
                    "than assuming it converted correctly.",
                ],
            },
            {
                "heading": "What to do after converting",
                "paragraphs": [
                    "Treat the converted Word document as a strong starting draft rather than "
                    "a perfect copy. Re-apply heading styles where needed, check that bullet "
                    "lists are still recognized as lists (rather than plain text with dashes), "
                    "and confirm tables have the right number of rows and columns. These quick "
                    "manual passes usually take just a few minutes and save a lot of frustration "
                    "later.",
                ],
            },
        ],
    },
    {
        "slug": "common-document-sharing-mistakes",
        "title": "5 Common Mistakes When Sharing Documents Online",
        "description": (
            "Simple habits that prevent formatting disasters, security issues, and "
            "confusion when you send a document to someone else."
        ),
        "read_time": "4 min read",
        "sections": [
            {
                "heading": "1. Sending an editable file when you meant to share a final version",
                "paragraphs": [
                    "If a document is finished and you don't want the recipient accidentally "
                    "changing it, send a PDF rather than the original Word file. PDFs display "
                    "consistently across devices and discourage casual edits, while still "
                    "allowing the recipient to comment or print easily.",
                ],
            },
            {
                "heading": "2. Forgetting to check the file on a different device",
                "paragraphs": [
                    "A document that looks perfect on your laptop can shift or break on a "
                    "phone, tablet, or a different operating system, especially if it uses "
                    "unusual fonts or precise pixel-based positioning. Before sending "
                    "something important, it's worth a quick preview on a second device if "
                    "you have one available.",
                ],
            },
            {
                "heading": "3. Leaving personal metadata in the file",
                "paragraphs": [
                    "Word and PDF files can quietly store metadata such as the author's name, "
                    "company, or editing history. This is usually harmless, but for sensitive "
                    "documents it's worth checking your document's properties/metadata panel "
                    "and clearing anything you don't want shared.",
                ],
            },
            {
                "heading": "4. Using vague file names",
                "paragraphs": [
                    "\"Document1.pdf\" or \"final_final_v2.docx\" might make sense to you in the "
                    "moment, but becomes confusing fast once a recipient has several files from "
                    "different people. A clear, descriptive file name saves everyone time later.",
                ],
            },
            {
                "heading": "5. Not compressing large files before sending",
                "paragraphs": [
                    "Documents with high-resolution images can balloon in size. Many email "
                    "providers cap attachments around 20-25MB, and large files are slower for "
                    "recipients to download on mobile connections. Compressing images before "
                    "inserting them into your document, or converting to PDF (which often "
                    "compresses images automatically), usually keeps file sizes manageable.",
                ],
            },
        ],
    },
]