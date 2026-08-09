from ollama import chat

from app.schemas.article_schema import ArticleList

SYSTEM_PROMPT = """
You are an expert at transcribing newspaper pages into clean json .

You will be given:
1. An image of a newspaper page.
2. The raw extracted text from that same page.

Your task:
- Reproduce all of the text from the raw text verbatim, with no summarizing, paraphrasing, or omissions.
- Use the image to identify the visual structure of the page (headline, body and author).
- If the page contains multiple articles or columns, append each to the ArticleList.
- Output only the final json content, with no commentary, explanations, or code fences.
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
        format=ArticleList.model_json_schema(),
    )

    with open(output_file, "w") as f:
        f.write(response.message.content or "")


write_md_file("pdf_scan.png", "pdf_scan.txt", "pfd_scan.json")
