import os
from PIL import Image

def convert_images_to_webp(input_dir, output_dir, quality=80, target_size=(1920, 1080)):
    """
    Convert and resize all JPEG and PNG images in the input directory and its subdirectories to WebP format.

    Parameters:
    - input_dir: str, path to the directory containing input images.
    - output_dir: str, path to the directory to save converted images.
    - quality: int, quality of the output WebP images (1-100 for lossy compression).
    - target_size: tuple, target size for resizing the images (width, height).
    """
    # Supported formats for conversion
    supported_formats = (".jpg", ".jpeg", ".png")

    # Walk through the input directory
    for root, dirs, files in os.walk(input_dir):
        # Create corresponding directory in the output directory
        relative_path = os.path.relpath(root, input_dir)
        output_path = os.path.join(output_dir, relative_path)
        os.makedirs(output_path, exist_ok=True)

        # Iterate through files in the current directory
        for filename in files:
            if filename.lower().endswith(supported_formats):
                input_file_path = os.path.join(root, filename)
                output_file_path = os.path.join(output_path, os.path.splitext(filename)[0] + ".webp")

                try:
                    # Open the image file
                    with Image.open(input_file_path) as img:
                        # Calculate the aspect ratio of the target size
                        target_ratio = target_size[0] / target_size[1]
                        img_ratio = img.width / img.height

                        if img_ratio > target_ratio:
                            # Image is wider than target, crop the width
                            new_width = int(target_ratio * img.height)
                            offset = (img.width - new_width) // 2
                            img = img.crop((offset, 0, offset + new_width, img.height))
                        else:
                            # Image is taller than target, crop the height
                            new_height = int(img.width / target_ratio)
                            offset = (img.height - new_height) // 2
                            img = img.crop((0, offset, img.width, offset + new_height))

                        # Resize the image to the target size
                        img = img.resize(target_size, Image.LANCZOS)

                        # Convert and save the image in WebP format
                        img.save(output_file_path, "WEBP", quality=quality)
                    print(f"Converted and resized: {input_file_path} -> {output_file_path} (Quality: {quality})")
                except Exception as e:
                    print(f"Failed to convert {input_file_path}: {e}")

# Example usage
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_directory = os.path.join(script_dir, "input")
    output_directory = os.path.join(script_dir, "output")

    # Ensure input and output directories exist
    os.makedirs(input_directory, exist_ok=True)
    os.makedirs(output_directory, exist_ok=True)

    # Conversion quality
    webp_quality = 50

    # Run the conversion
    convert_images_to_webp(input_directory, output_directory, quality=webp_quality)