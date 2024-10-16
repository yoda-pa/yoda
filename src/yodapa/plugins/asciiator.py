from PIL import Image
import os
import typer

app = typer.Typer(help="""
    Asciiator plugin. Convert an image to ASCII art.

    Example:

        $ yoda asciiator process "{path to image file}" -s // save output locally
        $ yoda asciiator process "{path to image file}" -t // display output on terminal
        $ yoda asciiator process "{path to image file}" -s -t // both the actions
      
    """)

ASCII_CHARS = ["#", "?", "%", ".", "S", "+", ".", "*", ":", ",", "@"]

def handle_image_conversion(image_filepath):
    image = None
    try:
        image = Image.open(image_filepath)
    except Exception as e:
        print(f"Unable to open image file {image_filepath}.")
        print(e)
        return
    
    new_width = 100
    (original_width, original_height) = image.size
    aspect_ratio = original_height / float(original_width)
    new_height = int(aspect_ratio * new_width)
    
    image = image.resize((new_width, new_height)).convert("L")
    
    # Adjust the range width to scale pixel values correctly
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

@app.command()
def process(input_data: str, save: bool = typer.Option(False, "-s", help="Save output to a file"), display: bool = typer.Option(False, "-t", help="Display output in terminal")):
    """
    Process an image and convert it to ASCII.
    
    Args:
    - input_data: Path to the image file.
    - save: Save the ASCII output to a text file.
    - display: Display the ASCII output in the terminal.
    """
    image_file_path = input_data
    data = handle_image_conversion(image_file_path)
    
    if not data:
        print("Error converting image.")
        return
    
    if save:
        directory = os.path.dirname(image_file_path)
        base_name = os.path.splitext(os.path.basename(image_file_path))[0]
        output_file_path = os.path.join(directory, f"{base_name}_ascii.txt")
        
        with open(output_file_path, 'w') as f:
            f.write(data)
        
        print(f"ASCII art saved to {output_file_path}")
    
    if display:
        print(data)

if __name__ == "__main__":
    app()
