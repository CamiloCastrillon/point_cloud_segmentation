import os
from PIL import Image
import pillow_heif
import cv2
import numpy as np

def convert_heic_to_jpg(input_folder, output_folder):
    # Registra el plugin de HEIF para que Pillow lo pueda utilizar
    pillow_heif.register_heif_opener()

    # Asegúrate de que la carpeta de salida exista
    os.makedirs(output_folder, exist_ok=True)

    # Recorre todos los archivos en la carpeta de entrada
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.heic'):
            heic_image_path = os.path.join(input_folder, filename)
            jpg_image_path = os.path.join(output_folder, filename.replace('.heic', '.jpg').replace('.HEIC', '.jpg'))

            try:
                # Abre la imagen HEIC utilizando Pillow
                with Image.open(heic_image_path) as img:
                    # Leer los metadatos EXIF
                    exif_data = img.info.get('exif')

                    # Guarda la imagen en formato JPG y conserva los metadatos EXIF si están disponibles
                    if exif_data:
                        img.save(jpg_image_path, 'JPEG', exif=exif_data)
                    else:
                        img.save(jpg_image_path, 'JPEG')

                print(f"Conversión exitosa: {filename} -> {jpg_image_path}")

            except Exception as e:
                print(f"Error al convertir {filename}: {e}")

def images_to_npy(input_folder, output_folder):
    # Listar todos los archivos en la carpeta de entrada
    for filename in os.listdir(input_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):  # Puedes agregar más extensiones según sea necesario
            # Construir la ruta completa de la imagen
            image_path = os.path.join(input_folder, filename)
            
            # Cargar la imagen usando OpenCV
            img = cv2.imread(image_path)

            if img is not None:
                # Convertir la imagen de BGR a RGB
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                # Convertir la imagen a un array de NumPy
                img_array = np.transpose(img_rgb, (1, 0, 2))

                # Construir la ruta para guardar el archivo .npy
                output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_data.npy")

                # Guardar el array como archivo .npy
                np.save(output_path, img_array)

                print(f"Guardado {output_path} con forma {img_array.shape}")
