import flet as ft
import os
from blur_images import create_dual_layer_image


def main(page: ft.Page):

    # Add base properties to the page
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "EH Procesador de imágenes"

    # Create a text to show the number of selected files
    selected_files = ft.Text(f'Tienes {0} archivos seleccionados')

    # Create a list of selected files
    images = ft.Row(expand=1, wrap=False, scroll="always")

    def close_dialog():
        dialog.open = False
        dialog.update()

    dialog = ft.AlertDialog(
        modal=True, on_dismiss=lambda _: close_dialog(), actions=[ft.TextButton(text="Cerrar", on_click=lambda _: close_dialog())])

    pb = ft.ProgressBar(width=400, visible=False)

    page.add(dialog)

    def reset():
        open_output_folder_button.disabled = True
        open_output_folder_button.update()

        process_button.disabled = True
        process_button.update()

        selected_files.value = (f'Tienes {0} archivos seleccionados')
        selected_files.update()

        images.controls.clear()
        images.update()

        dialog.open = False
        dialog.update()

        directory_path.value = ""
        directory_path.update()

    # Open directory dialog
    def get_directory_result(e: ft.FilePickerResultEvent):
        if e.path:
            directory_path.value = f'Origen: {e.path}'
            directory_path.update()
            all_items = os.listdir(e.path)
            # Filter out only the files from the list

            files_count = 0
            files_list = os.listdir(e.path)

            for file_name in files_list:
                if file_name.endswith((".jpg", ".png", ".jpeg")):
                    files_count += 1
                    input_image_path = os.path.join(e.path, file_name)

                    images.controls.append(
                        ft.Image(
                            src=input_image_path,
                            fit=ft.ImageFit.NONE,
                            repeat=ft.ImageRepeat.NO_REPEAT,
                            border_radius=ft.border_radius.all(10),
                        )
                    )
            images.update()

            selected_files.value = (
                f'Tienes {files_count} archivos seleccionados')
            selected_files.update()

            if files_count > 0:
                process_button.disabled = False
                process_button.update()
        else:
            print("No directory selected")

    def open_output_folder():
        output_folder = directory_path.value.removeprefix("Origen: ")
        os.startfile(output_folder)

    def process_images():
        try:
            if not directory_path.value:
                dialog.title = ft.Text('Error')
                dialog.content = ft.Text(
                    f"Porfavor, selecciona una carpeta con imágenes")
                dialog.open = True
                dialog.update()
                return

            input_folder = directory_path.value.removeprefix("Origen: ")
            # Check if the input folder exists
            if not os.path.exists(input_folder):
                dialog.title = ft.Text('Error')
                dialog.content = ft.Text(
                    f'La carpeta "{input_folder}" no existe.')
                dialog.open = True
                dialog.update()
                return

            # check if the input folder is empty
            files_list = os.listdir(input_folder)
            images_list = [file_name for file_name in files_list if file_name.endswith(
                ("jpg", "png", "jpeg"))]

            if not images_list or len(images_list) == 0:
                dialog.title = ft.Text('Error')
                dialog.content = ft.Text(
                    f'La carpeta "{input_folder}" está vacía.')
                dialog.open = True
                dialog.update()
                return

            # check if the output folder exists, if not create it
            output_folder = input_folder+"/output_images"
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # update the progress bar
            pb.visible = True
            pb.value = 0
            pb.update()

            # process each image
            for file_name in images_list:
                input_image_path = os.path.join(input_folder, file_name)

                output_image_name = f"{os.path.splitext(file_name)[0]}.png"
                output_image_path = os.path.join(
                    output_folder, output_image_name)
                create_dual_layer_image(
                    input_image_path, output_image_path)

                pb.value += 1/len(images_list)
                pb.update()

            # update the progress bar
            pb.visible = False
            pb.value = 0
            pb.update()

            # Enable the "Open Output Folder" button
            open_output_folder_button.disabled = False
            open_output_folder_button.update()

            # Disable the "Process Images" button
            process_button.disabled = True
            process_button.update()

            # Show a dialog to notify the user that the images were processed
            dialog.title = ft.Text('¡Listo! :D')
            dialog.content = ft.Row(
                controls=[ft.Text(f"Las imágenes fueron procesadas"), open_output_folder_button], alignment="center")
            dialog.open = True
            dialog.update()

        except Exception as e:
            print(e)
            dialog.title = ft.Text('Error')
            dialog.content = ft.Text(f"Algo inesperado salió mal")
            dialog.open = True
            dialog.update()
            return

    get_directory_dialog = ft.FilePicker(on_result=get_directory_result)
    directory_path = ft.Text()

    page.overlay.append(get_directory_dialog)

    # Create a button to process the images
    process_button = ft.ElevatedButton(
        "Procesar Imágenes", icon=ft.icons.PLAY_ARROW, disabled=True, on_click=lambda _: process_images())

    # Create a button to reset all inputs
    reset_button = ft.ElevatedButton(
        "Limpiar", icon="refresh", on_click=lambda _: reset())
    # Create a button to open the output folder
    open_output_folder_button = ft.ElevatedButton(
        "Abrir Resultado", icon=ft.icons.FOLDER_SPECIAL, disabled=True, on_click=lambda _: open_output_folder())

    input_folder_button = ft.ElevatedButton(
        "Abrir Carpeta",
        icon=ft.icons.FOLDER_OPEN,
        on_click=lambda _: get_directory_dialog.get_directory_path(),
        disabled=page.web,
    )

    page.add(ft.Row(controls=[directory_path], alignment="center"))
    page.add(ft.Row(controls=[pb], alignment="center"))
    # Add actions row
    page.add(ft.Row(
        controls=[input_folder_button, process_button, reset_button, open_output_folder_button], alignment="center"))

    # if images isn't empty, show a preview of all the images:
    page.add(ft.Row(
        controls=[selected_files], alignment="center"))

    page.add(images)


ft.app(target=main, name="EH Procesador de imágenes")
