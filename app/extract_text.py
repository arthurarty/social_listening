import pytesseract
from PIL import Image


def main(image_path: str, output_file_name: str):
    # Load the image using Pillow
    image = Image.open(image_path)

    # Extract text as a single string
    extracted_text = pytesseract.image_to_string(image)

    with open(output_file_name, "w") as f:
        f.write(extracted_text)


main("pdf_scan.png", "pdf_scan.txt")
main("online_view.png", "online.txt")
