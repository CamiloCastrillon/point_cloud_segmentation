from PIL import Image
import os

def remove_metadata(input_folder, output_folder):
    # Crea la carpeta de salida si no existe
    os.makedirs(output_folder, exist_ok=True)
    
    # Recorre todas las imágenes en la carpeta de entrada
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(input_folder, filename)
            with Image.open(img_path) as img:
                # Carga la imagen sin metadatos
                clean_img = Image.new(img.mode, img.size)
                clean_img.putdata(list(img.getdata()))
                
                # Guarda la imagen en la carpeta de salida
                output_path = os.path.join(output_folder, filename)
                clean_img.save(output_path)
                print(f"Guardada sin metadatos: {output_path}")

# Especifica la carpeta de entrada y salida
input_folder = 'C:/camilo/trabajo_de_grado/pcs/image_datasets/monumento_summarized_3/'
output_folder = 'C:/camilo/trabajo_de_grado/pcs/image_datasets/monumento_summarized_3_nm/'

remove_metadata(input_folder, output_folder)