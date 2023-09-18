import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
from blur_images import create_dual_layer_image

# Create constants for all widgets rows

INSTRUCTIONS_ROW = 0
INPUT_FOLDER_ROW = INSTRUCTIONS_ROW + 1
OUTPUT_FOLDER_ROW = INPUT_FOLDER_ROW + 1
BUTTON_FRAME_ROW = OUTPUT_FOLDER_ROW + 2

# Get the directory of the current script (src directory)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to icon.ico by joining the script directory and the icon filename
icon_path = os.path.join(script_dir, "..", "icon.ico")


# Function to create a loading animation
def create_loading_animation(canvas):
    arc = canvas.create_arc(10, 10, 50, 50, extent=30, style=tk.ARC)
    return arc

# Function to reset all inputs and labels


def reset_all():
    input_folder_entry.delete(0, tk.END)
    output_folder_entry.delete(0, tk.END)
    open_output_folder_button.config(state=tk.DISABLED)


def process_images():
    try:
        input_folder = input_folder_entry.get()
        output_folder = output_folder_entry.get()

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
                output_image_name = f"{os.path.splitext(file_name)[0]}.png"
                output_image_path = os.path.join(
                    output_folder, output_image_name)
                create_dual_layer_image(
                    input_image_path, output_image_path)

        # Enable the "Open Output Folder" button
        open_output_folder_button.config(state=tk.NORMAL)
    except:
        messagebox.showerror(
            "Error", f"Algo inesperado salió mal")
        return


# Create a function to select input and output folders


def browse_input_folder():
    folder_path = filedialog.askdirectory()
    input_folder_entry.delete(0, tk.END)
    input_folder_entry.insert(0, folder_path)

    # split the path and add the output folder in the same directory
    output_folder_path = os.path.join(folder_path, "output_images")
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
