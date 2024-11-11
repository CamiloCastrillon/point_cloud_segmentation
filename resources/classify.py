import cv2
import numpy as np
import glob
import os

def load_images(folder_path):
    images = []
    for img_path in glob.glob(f"{folder_path}/*.jpg"):  # Cambia *.jpg si tienes otro formato
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        images.append(img_rgb)
    return images

def create_color_mapping(images):
    # Extraer colores únicos de todas las imágenes
    unique_colors = set()
    for img in images:
        # Convertir cada color a tupla antes de añadirlo al conjunto
        unique_colors.update([tuple(color) for color in np.unique(img.reshape(-1, 3), axis=0)])
    
    # Asignar una clase a cada color único
    color_to_class = {color: idx for idx, color in enumerate(unique_colors)}
    return color_to_class

def add_class_band(images, color_to_class):
    images_with_class = []
    for img in images:
        # Crear una banda para la clase
        class_band = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
        
        # Asignar clase a cada pixel
        for color, cls in color_to_class.items():
            # Crear una máscara para los pixeles con el color exacto
            mask = np.all(img == color, axis=-1)
            class_band[mask] = cls

        # Añadir la banda de clase a la imagen RGB
        img_with_class = np.dstack((img, class_band))
        images_with_class.append(img_with_class)
    
    return np.array(images_with_class)

def save_images(images, output_folder):
    # Crear la carpeta si no existe
    os.makedirs(output_folder, exist_ok=True)
    
    # Guardar cada imagen como archivo .npy
    for idx, img in enumerate(images):
        file_path = os.path.join(output_folder, f"image_{idx}.npy")
        np.save(file_path, img)
        print(f"Imagen guardada en: {file_path}")

def create_array_class(input_folder, output_folder):
    # Paso 1: Cargar imágenes
    images = load_images(input_folder)
    
    # Paso 2: Crear el mapeo de colores a clases
    color_to_class = create_color_mapping(images)
    print(f"Colores únicos y sus clases: {color_to_class}")
    
    # Paso 3: Añadir banda de clase a cada imagen
    images_with_class = add_class_band(images, color_to_class)
    
    # Paso 4: Guardar imágenes en formato .npy
    save_images(images_with_class, output_folder)