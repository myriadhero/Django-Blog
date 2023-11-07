import argparse

from PIL import Image


def resize_image(image_path: str, width: int, height: int, quality: int = 100):
    start, extension = image_path.rsplit(".", maxsplit=1)
    resized_path = f"{start}_{width}x{height}.{extension}"

    # Open the image using Pillow
    image = Image.open(image_path)

    # Resize the image
    resized_image = image.resize((width, height), Image.LANCZOS)

    # Save the resized image (overwrite the original file or save as a new file)
    resized_image.save(resized_path, quality=quality)

    # Close the image files
    image.close()
    resized_image.close()

    print(f"Image '{image_path}' resized successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize an image.")
    parser.add_argument("image_path", help="Path to the image file.")
    parser.add_argument("width", help="Width of the image file.")
    parser.add_argument("height", help="Height of the image file.")
    parser.add_argument("-q", help="Quality of the image file.", default=100)
    args = parser.parse_args()

    resize_image(args.image_path, int(args.width), int(args.height))
