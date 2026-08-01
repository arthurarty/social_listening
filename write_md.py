from ollama import chat



SYSTEM_PROMPT = """
You are an expert at transcribing newspaper pages into clean markdown.

You will be given:
1. An image of a newspaper page.
2. The raw extracted text from that same page.

Your task:
- Reproduce all of the text from the raw text verbatim, with no summarizing, paraphrasing, or omissions.
- Use the image to identify the visual structure of the page (headline, byline, subheadings, captions, pull quotes) and apply matching markdown headings and formatting.
- Use a single "#" for the main headline, "##" for section/article subheadings, and "###" for any smaller subheadings, matching their visual hierarchy in the image.
- Render bylines and captions as italics, and pull quotes as blockquotes.
- If the page contains multiple articles or columns, separate each with a horizontal rule ("---").
- Output only the final markdown content, with no commentary, explanations, or code fences.
"""


def write_md_file(image_path: str, txt_file: str, output_file: str):
    """
    Read image and txt_file and create an md file.
    """

    # You can also pass in base64 encoded image data
    # img = base64.b64encode(Path(path).read_bytes()).decode()
    # or the raw bytes
    # img = Path(path).read_bytes()

    with open(txt_file, 'r') as f:
        txt_content = f.read()

    response = chat(
        model='gemma4',
        messages=[
            {
                'role': 'system',
                'content': SYSTEM_PROMPT,
            },
            {
                'role': 'user',
                'content': txt_content,
                'images': [image_path],
            },
        ],
    )

    with open(output_file, 'w') as f:
        f.write(response.message.content or '')


write_md_file("pdf_scan.png", "pdf_scan.txt", "pfd_scan.MD")
