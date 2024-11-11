import numpy as np
import matplotlib.pyplot as plt
import open3d as o3d
from plyfile import PlyData

def plot_npy_rgb_image(npy_file):
    # Cargar el archivo .npy
    img_array = np.load(npy_file)
    print(img_array.shape)
    # Verificar que la imagen tenga 4 bandas
    if img_array.shape[-1] == 4:
        # Extraer solo las primeras 3 bandas (RGB)
        img_rgb = img_array[:, :, :3]

        # Graficar la imagen RGB rotada
        plt.imshow(img_rgb)
        plt.axis('off')  # Ocultar los ejes
        plt.show()
    else:
        print("El archivo .npy no contiene exactamente 4 bandas")

# Función para convertir color hex a RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')  # Eliminar el símbolo '#' si está presente
    rgb = [int(hex_color[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]  # Convertir a [0, 1]
    return rgb

def plot_nubes_juntas(paths, colors):
    vis = o3d.visualization.Visualizer()
    vis.create_window()

    for path, color_hex in zip(paths, colors):
        array_cargado = np.load(path)

        # Crear un objeto de nube de puntos Open3D
        nube_puntos = o3d.geometry.PointCloud()
        nube_puntos.points = o3d.utility.Vector3dVector(array_cargado[:, :3])  # x, y, z

        # Convertir a formato de color a RGB
        rgb_color = hex_to_rgb(color_hex)

        # Pintar toda la nube de puntos con el color uniforme
        nube_puntos.paint_uniform_color(rgb_color)

        # Agregar la nube de puntos al visualizador
        vis.add_geometry(nube_puntos)
        
    # Iniciar la visualización
    vis.get_view_control().set_zoom(0.5)
    vis.run()
    vis.destroy_window()

def plot_npy_xyz(path, color_hex):
    array_cargado = np.load(path)

    # Crear un objeto de nube de puntos Open3D
    nube_puntos = o3d.geometry.PointCloud()
    nube_puntos.points = o3d.utility.Vector3dVector(array_cargado[:, :3])  # x, y, z

    # Convertir a formato de color a RGB
    rgb_color = hex_to_rgb(color_hex)

    # Pintar toda la nube de puntos con el color uniforme
    nube_puntos.paint_uniform_color(rgb_color)

    # Crear la visualización
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name=f'Nube de Puntos - {path}')  # Dar un nombre a la ventana
    vis.add_geometry(nube_puntos)

    vis.get_view_control().set_zoom(0.5)  # Ajustar el zoom inicial
    
    # Iniciar la visualización
    vis.run()
    vis.destroy_window()

def plot_point_cloud_from_ply(ply_file):
    # Leer el archivo PLY
    plydata = PlyData.read(ply_file)

    # Imprimir toda la estructura del archivo PLY
    print(plydata)

    point_cloud = o3d.io.read_point_cloud(ply_file)

    # Mostrar la nube de puntos
    print(point_cloud)

    # Visualizar la nube de puntos
    o3d.visualization.draw_geometries([point_cloud])