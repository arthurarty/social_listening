import pytesseract
from PIL import Image


def extract_text_from_image(image_path: str) -> str:
    """
    Use OCR to extract the text from an image.
    Function uses pytesseract to read the text.
    """
    # Load the image using Pillow
    image = Image.open(image_path)

    # Extract text as a single string
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text
