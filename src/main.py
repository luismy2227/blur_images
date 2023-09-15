import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
from blur_images import create_dual_layer_image

# Create constants for default image size
DEFAULT_WIDTH = 1200
DEFAULT_HEIGHT = 900

# Create constants for all widgets rows

INSTRUCTIONS_ROW = 0
INPUT_FOLDER_ROW = INSTRUCTIONS_ROW + 1
OUTPUT_FOLDER_ROW = INPUT_FOLDER_ROW + 1
SIZE_FRAME_ROW = OUTPUT_FOLDER_ROW + 1
BUTTON_FRAME_ROW = SIZE_FRAME_ROW + 2

# Get the directory of the current script (src directory)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to icon.ico by joining the script directory and the icon filename
icon_path = os.path.join(script_dir, "..", "icon.ico")


def process_images():
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()
    final_width = int(final_width_entry.get())
    final_height = int(final_height_entry.get())

    final_size = (final_width, final_height)

    # Check if the input folder exists
    if not os.path.exists(input_folder):
        messagebox.showerror(
            "Error", f"Input folder '{input_folder}' does not exist.")
        return

    # check if the output folder exists, if not create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith((".jpg", ".png", ".jpeg")):
            input_image_path = os.path.join(input_folder, file_name)
            output_image_name = f"{os.path.splitext(file_name)[0]}_{final_width}x{final_height}.png"
            output_image_path = os.path.join(output_folder, output_image_name)
            create_dual_layer_image(
                input_image_path, output_image_path, final_size)

    # Enable the "Open Output Folder" button
    open_output_folder_button.config(state=tk.NORMAL)


# Function to reset all inputs and labels
def reset_all():
    input_folder_entry.delete(0, tk.END)
    output_folder_entry.delete(0, tk.END)
    final_width_entry.delete(0, tk.END)
    final_height_entry.delete(0, tk.END)
    final_width_entry.insert(0, f'{DEFAULT_WIDTH}')
    final_height_entry.insert(0, f'{DEFAULT_HEIGHT}')
    open_output_folder_button.config(state=tk.DISABLED)

# Create a function to select input and output folders


def browse_input_folder():
    folder_path = filedialog.askdirectory()
    input_folder_entry.delete(0, tk.END)
    input_folder_entry.insert(0, folder_path)

    # split the path and add the output folder in the same directory
    output_folder_path = os.path.split(folder_path)[0]
    output_folder_path = os.path.join(output_folder_path, "output_images")
    output_folder_entry.insert(0, output_folder_path)


def browse_output_folder():
    folder_path = filedialog.askdirectory()
    output_folder_entry.delete(0, tk.END)
    output_folder_entry.insert(0, folder_path)

# Function to open the output folder


def open_output_folder():
    output_folder = output_folder_entry.get()
    os.system(f"explorer {output_folder}")  # For Windows, open in Explorer
    input_folder_entry.delete(0, tk.END)
    output_folder_entry.delete(0, tk.END)
    open_output_folder_button.config(state=tk.DISABLED)
    final_width_entry.insert(0, f'{DEFAULT_WIDTH}')
    final_height_entry.insert(0, f'{DEFAULT_HEIGHT}')


# Create the main application window
app = tk.Tk()
app.title("Image Processor")

# Set a fixed window size (width x height)
app.geometry("500x220")  # You can change these dimensions as needed
app.resizable(False, False)
app.iconbitmap(icon_path)

# Padding top the first row of widgets
app.grid_rowconfigure(0, pad=20)
# Create and arrange widgets
tk.Label(app, text="Elige la carpeta", font=(
    "Helvetica", 12)).grid(row=INSTRUCTIONS_ROW, columnspan=3)

tk.Label(app, text="Carpeta Inicial:").grid(row=INPUT_FOLDER_ROW, column=0)
input_folder_entry = tk.Entry(app, width=50)

input_folder_entry.grid(row=INPUT_FOLDER_ROW, column=1)
tk.Button(app, text="Buscar", command=browse_input_folder).grid(
    row=1, column=2, padx=10)

tk.Label(app, text="Carpeta Resultante:").grid(
    row=OUTPUT_FOLDER_ROW, column=0, pady=20)
output_folder_entry = tk.Entry(app, width=50)
output_folder_entry.grid(row=OUTPUT_FOLDER_ROW, column=1)
tk.Button(app, text="Buscar", command=browse_output_folder).grid(
    row=2, column=2, padx=10)

# Create a frame for the size inputs
size_frame = tk.Frame(app)
size_frame.grid(row=SIZE_FRAME_ROW, columnspan=3)

tk.Label(size_frame, text="Ancho Final:").pack(side=tk.LEFT)
final_width_entry = tk.Entry(size_frame, width=10)
final_width_entry.pack(side=tk.LEFT)
final_width_entry.insert(0, f'{DEFAULT_WIDTH}')  # Prepopulate with 800

tk.Label(size_frame, text="Altura Final:").pack(side=tk.LEFT, padx=10)
final_height_entry = tk.Entry(size_frame, width=10)
final_height_entry.pack(side=tk.LEFT)
final_height_entry.insert(0, f'{DEFAULT_HEIGHT}')  # Prepopulate with 600

# Create a frame for the buttons in a single row
button_frame = tk.Frame(app)
button_frame.grid(row=BUTTON_FRAME_ROW, columnspan=3, pady=20, )

process_button = tk.Button(
    button_frame, text="Process Images", command=process_images)
process_button.pack(side=tk.LEFT, padx=10)

# Create a button to reset all inputs
reset_button = tk.Button(button_frame, text="Reset All", command=reset_all)
reset_button.pack(side=tk.LEFT, padx=10)

# Create a button to open the output folder (initially disabled)
open_output_folder_button = tk.Button(
    button_frame, text="Open Output Folder", command=open_output_folder, state=tk.DISABLED)
open_output_folder_button.pack(side=tk.LEFT, padx=10)


app.mainloop()
