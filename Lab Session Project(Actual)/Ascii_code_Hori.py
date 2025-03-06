from PIL import Image, ImageDraw, ImageFont
import numpy as np

# ASCII character sets for different font styles
ASCII_CHARS = {
    "basic": "@%#*+=-:. ",
    "detailed": "@%#*+=-:. ",
    "block": "█▓▒░ ",
    "minimal": "@#+ "
}

# Color schemes
COLOR_SCHEMES = {
    "retro_terminal": ("green", "black"),
    "futuristic_white": ("gray", "white")
}

def resize_image(image, new_width=100):
    """Resize the image while maintaining aspect ratio."""
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.55)  # Adjust for font aspect ratio
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayscale_image(image):
    """Convert the image to grayscale."""
    return image.convert("L")

def map_pixels_to_ascii(image, font_style="basic"):
    """Map grayscale pixels to ASCII characters."""
    pixels = np.array(image)
    ascii_chars = ASCII_CHARS.get(font_style, ASCII_CHARS["basic"])
    ascii_str = "".join([ascii_chars[pixel // 25] for pixel in pixels.flatten()])
    return "\n".join(ascii_str[i:(i + image.width)] for i in range(0, len(ascii_str), image.width))

def text_to_ascii(text, font_style="basic"):
    """Convert text to ASCII art."""
    ascii_chars = ASCII_CHARS.get(font_style, ASCII_CHARS["basic"])
    return text  # Return the text as a single line

def save_ascii_to_txt(ascii_art, filename="ascii_art.txt"):
    """Save ASCII art to a text file."""
    with open(filename, "w") as file:
        file.write(ascii_art)

def save_ascii_to_png(ascii_art, color_scheme="retro_terminal", filename="ascii_art.png"):
    """Save ASCII art as a PNG image."""
    text_color, bg_color = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["retro_terminal"])
    font_size = 20  # Increase font size for better visibility
    font = ImageFont.load_default()
    
    # Calculate image size based on text
    padding = 20
    lines = ascii_art.split("\n")
    max_line_length = max(len(line) for line in lines)
    img_width = max_line_length * font_size // 2 + padding
    img_height = len(lines) * font_size + padding
    
    # Create the image
    image = Image.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # Draw the text
    y = padding // 2
    for line in lines:
        draw.text((padding // 2, y), line, fill=text_color, font=font)
        y += font_size
    
    image.save(filename)

def main():
    """Main function to run the ASCII Art Generator."""
    print("ASCII Art Generator")
    print("1. Convert Image to ASCII")
    print("2. Convert Text to ASCII")
    choice = input("Choose an option (1/2): ")

    if choice == "1":
        image_path = input("Enter the image path (drag and drop the image file here): ").strip('"')
        try:
            image = Image.open(image_path)
            width = int(input("Enter the desired width (e.g., 100): "))
            font_style = input("Choose font style (basic/detailed/block/minimal): ")
            
            resized_image = resize_image(image, width)
            gray_image = grayscale_image(resized_image)  # Renamed variable
            ascii_art = map_pixels_to_ascii(gray_image, font_style)

        except Exception as e:
            print(f"Error: {e}")
            return
    elif choice == "2":
        text = input("Enter the text: ")
        font_style = input("Choose font style (basic/detailed/block/minimal): ")
        ascii_art = text_to_ascii(text, font_style)
    else:
        print("Invalid choice!")
        return

    # Live preview
    print("\nLive Preview:\n")
    print(ascii_art)

    # Dark Mode vs Light Mode
    mode = input("Choose mode (dark/light): ").lower()
    color_scheme = "retro_terminal" if mode == "dark" else "futuristic_white"

    # Save options
    save_option = input("Save as txt or png? (txt/png): ").lower()
    if save_option == "txt":
        save_ascii_to_txt(ascii_art)
        print("ASCII art saved as ascii_art.txt")
    elif save_option == "png":
        save_ascii_to_png(ascii_art, color_scheme)
        print("ASCII art saved as ascii_art.png")
    else:
        print("Invalid save option!")

if __name__ == "__main__":
    main()