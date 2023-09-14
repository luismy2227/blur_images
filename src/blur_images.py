from PIL import Image, ImageFilter
import os


def create_dual_layer_image(input_image_path, output_image_path, final_size):
    # Open the input image
    with Image.open(input_image_path) as img:
        # Calculate the dimensions for the foreground layer (centered and smaller image)
        width, height = img.size

        # Calculate the aspect ratio of the input image
        aspect_ratio = width / height

        # Calculate the dimensions for the foreground layer while maintaining aspect ratio
        foreground_width = round(
            min(final_size[0], final_size[1] * aspect_ratio))
        foreground_height = round(foreground_width / aspect_ratio)

        if foreground_width > final_size[0]:
            foreground_width = final_size[0]
            foreground_height = round(final_size[0] / aspect_ratio)
        elif foreground_height > final_size[1]:
            foreground_height = final_size[1]
            foreground_width = round(final_size[1] * aspect_ratio)

        # Calculate the dimensions for the background layer (blurred image)
        background_size = final_size

        # Resize and blur the input image for the background layer
        blurred_image = img.resize(background_size)
        blurred_image = blurred_image.filter(
            ImageFilter.GaussianBlur(radius=10))

        # Resize and position the input image for the foreground layer
        foreground_image = img.resize((foreground_width, foreground_height))
        x_offset = (final_size[0] - foreground_width) // 2
        y_offset = (final_size[1] - foreground_height) // 2

        # Create a new image with RGBA mode
        dual_layer_image = Image.new("RGBA", final_size)

        # Paste the blurred image on the background layer
        dual_layer_image.paste(blurred_image, (0, 0))

        # Paste the resized and positioned image on the foreground layer
        dual_layer_image.paste(foreground_image, (x_offset, y_offset))

        # Save the final dual-layer image
        dual_layer_image.save(output_image_path)


if __name__ == "__main__":
    input_folder = "img/input_images"
    output_folder = "img/output_images"
    final_sizes = [(1200, 900)]  # Add the desired final sizes here

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each image with different final sizes
    for file_name in os.listdir(input_folder):
        if file_name.endswith((".jpg", ".png", ".jpeg")):
            input_image_path = os.path.join(input_folder, file_name)
            for size in final_sizes:
                output_image_name = f"{os.path.splitext(file_name)[0]}_{size[0]}x{size[1]}.png"
                output_image_path = os.path.join(
                    output_folder, output_image_name)
                create_dual_layer_image(
                    input_image_path, output_image_path, size)
                print(f"Created: {output_image_path}")
