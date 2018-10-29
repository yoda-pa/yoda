from PIL import Image

ASCII_CHARS = ["#", "?", "%", ".", "S", "+", ".", "*", ":", ",", "@"]


def handle_image_conversion(image_filepath):
    image = None
    try:
        image = Image.open(image_filepath)
    except Exception as e:
        print(
            "Unable to open image file {image_filepath}.".format(
                image_filepath=image_filepath
            )
        )
        print(e)
        return
    new_width = 100
    range_width = 25
    (original_width, original_height) = image.size
    aspect_ratio = original_height / float(original_width)
    new_height = int(aspect_ratio * new_width)
    image = image.resize((new_width, new_height)).convert("L")
    pixels_to_chars = "".join(
        [
            ASCII_CHARS[pixel_value / range_width]
            for pixel_value in list(image.getdata())
        ]
    )
    image_ascii = [
        pixels_to_chars[index : index + new_width]
        for index in xrange(0, len(pixels_to_chars), new_width)
    ]
    return "\n".join(image_ascii)


def process(input_data):

    image_file_path = input_data
    data = handle_image_conversion(image_file_path)
    return data
