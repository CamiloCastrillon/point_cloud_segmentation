import os
from PIL import Image
import pillow_heif

# Registra el plugin de HEIF para que Pillow lo pueda utilizar
pillow_heif.register_heif_opener()

def convert_heic_to_jpg(input_folder, output_folder):
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

# Define las rutas de las carpetas de entrada y salida
input_folder = 'C:/camilo/point_cloud/images/monumento/'
output_folder = 'C:/camilo/point_cloud/images/monumento_jpg/'

# Ejecuta la función de conversión
convert_heic_to_jpg(input_folder, output_folder)