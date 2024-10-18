from PIL import Image
import os
import typer
from rich import print

app = typer.Typer(help="""
    Asciiator plugin. Convert an image to ASCII art.

    Example:

        $ yoda asciiator file "{path to image file}" // save output locally
        $ yoda asciiator show "{path to image file}" // display output on terminal
        $ yoda asciiator both "{path to image file}" // both the actions
    """)

ASCII_CHARS = ["#", "?", "%", ".", "S", "+", ".", "*", ":", ",", "@"]

def handle_image_conversion(image_filepath):
    image = None
    try:
        image = Image.open(image_filepath)
    except Exception as e:
        print(f"Unable to open image file {image_filepath}.")
        print(e)
        return None
    
    new_width = 100
    (original_width, original_height) = image.size
    aspect_ratio = original_height / float(original_width)
    new_height = int(aspect_ratio * new_width)
    
    image = image.resize((new_width, new_height)).convert("L")
    
    range_width = 256 // len(ASCII_CHARS)
    
    pixels_to_chars = "".join(
        [
            ASCII_CHARS[min(pixel_value // range_width, len(ASCII_CHARS) - 1)]
            for pixel_value in list(image.getdata())
        ]
    )
    
    image_ascii = [
        pixels_to_chars[index: index + new_width]
        for index in range(0, len(pixels_to_chars), new_width)
    ]
    
    return "\n".join(image_ascii)

def save_ascii_art(image_ascii, image_file_path):
    directory = os.path.dirname(image_file_path)
    base_name = os.path.splitext(os.path.basename(image_file_path))[0]
    output_file_path = os.path.join(directory, f"{base_name}_ascii.txt")
    
    with open(output_file_path, 'w') as f:
        f.write(image_ascii)
    
    print(f"ASCII art saved to {output_file_path}")

@app.command()
def file(image_path: str):
    """
    Save the ASCII art to a text file.
    """
    data = handle_image_conversion(image_path)
    
    if data:
        save_ascii_art(data, image_path)
    else:
        print("Error converting image.")

@app.command()
def show(image_path: str):
    """
    Display the ASCII art in the terminal.
    """
    data = handle_image_conversion(image_path)
    
    if data:
        print(data)
    else:
        print("Error converting image.")

@app.command()
def both(image_path: str):
    """
    Save the ASCII art to a file and display it in the terminal.
    """
    data = handle_image_conversion(image_path)
    
    if data:
        save_ascii_art(data, image_path)
        print(data)
    else:
        print("Error converting image.")

if __name__ == "__main__":
    app()
