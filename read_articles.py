from app.schemas.article_schema import Article
from app.services.instances import news_page_service
from app.utils.extract_text import extract_text_from_image

articles = [
    Article(
        headline="Uganda airlines to Kigali",
        body="Uganda Airlines will be flying to kigali",
        author="Jack Ma",
    )
]


def main():
    """
    Runs a pipeline to create articles from a news page

    1. Reads unprocessed news_pages.
    2. Extracts the text from the images using OCR.
    3. Creates json using an visual model and the extracted text
    4. Updates the news page
    """
    news_pages = news_page_service.get_news_pages(limit=1)

    for news_page in news_pages:
        extracted_text = extract_text_from_image(news_page.file_path)
        print(extracted_text)


# print(news_pages)

# news_page_service.update_news_page_articles(news_page_id=1, articles=articles)


main()
