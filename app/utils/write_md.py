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
- A "border" is a ruled line or box that visually separates one section of the page from another (e.g. a horizontal rule dividing the masthead from the body, or a box drawn around a sidebar/pull quote). If the image shows a border, place the exact marker "***---***" on its own line at the point in the transcription where that border appears — immediately before the content that follows it, and again immediately after a boxed section closes. Do not use this marker for anything other than a border you can actually see in the image.
- If the page contains multiple columns, separate each with a horizontal rule ("---").
- Output only the final markdown content, with no commentary, explanations, or code fences.
"""


def write_md_file(image_path: str, ocr_text: str, output_file: str):
    """
    Read image and txt_file and create an md file.
    """
    response = chat(
        model="gemma4",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": ocr_text,
                "images": [image_path],
            },
        ],
        options={
            "temperature": 0,
            "seed": 42,
        },
    )

    with open(output_file, "w") as f:
        f.write(response.message.content or "")
