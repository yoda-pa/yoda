from PIL import Image
import os
import typer

app = typer.Typer()

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
    range_width = 25
    (original_width, original_height) = image.size
    aspect_ratio = original_height / float(original_width)
    new_height = int(aspect_ratio * new_width)
    
    # Resize and convert the image to grayscale
    image = image.resize((new_width, new_height)).convert("L")
    
    # Map pixel values to ASCII characters
    pixels_to_chars = "".join(
        [
            ASCII_CHARS[pixel_value // range_width]
            for pixel_value in list(image.getdata())
        ]
    )
    
    # Create a list of strings for each row of ASCII characters
    image_ascii = [
        pixels_to_chars[index: index + new_width]
        for index in range(0, len(pixels_to_chars), new_width)
    ]
    
    return "\n".join(image_ascii)

@app.command()
def process(input_data):
    image_file_path = input_data
    data = handle_image_conversion(image_file_path)
    
    if data:
        # Get the directory and original file name without extension
        directory = os.path.dirname(image_file_path)
        base_name = os.path.splitext(os.path.basename(image_file_path))[0]
        
        # Define the output file path
        output_file_path = os.path.join(directory, f"{base_name}_ascii.txt")
        
        # Save the ASCII art to a text file
        with open(output_file_path, 'w') as f:
            f.write(data)
        
        print(f"ASCII art saved to {output_file_path}")

