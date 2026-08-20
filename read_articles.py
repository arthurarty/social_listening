import time

from app.agent_workflows.write_md import write_md_file
from app.services.instances import news_page_service
from app.utils.extract_text import extract_text_from_image


def main():
    """
    Runs a pipeline to create articles from a news page

    1. Reads unprocessed news_pages.
    2. Extracts the text from the images using OCR.
    3. Creates json using an visual model and the extracted text
    4. Updates the news page
    """
    news_pages = news_page_service.get_news_pages(limit=2)

    for news_page in news_pages:
        extracted_text = extract_text_from_image(news_page.file_path)
        start_time = time.time()
        write_md_file(
            image_path=news_page.file_path,
            ocr_text=extracted_text,
            output_file=f"{news_page.id}_file.MD",
        )
        print(f"write_md_file took {time.time() - start_time:.2f} seconds")


# news_page_service.update_news_page_articles(news_page_id=1, articles=articles)


main()
