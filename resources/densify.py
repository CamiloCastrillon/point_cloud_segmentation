import numpy as np
from scipy.spatial import KDTree
import open3d as o3d

# Paso 1: Cargar la nube de puntos NPY
npy_folder  = 'C:/camilo/trabajo_de_grado/imgs/point_cloud/'
npy_file    = npy_folder + 'pts_clase_2.npy'
nube_npy    = np.load(npy_file)  # Asume que es un array Nx3

# Usar solo las coordenadas x, y, z
nube_npy_xyz = nube_npy[:, :3]

# Paso 2: Cargar la nube de puntos PLY
ply_file = 'C:/camilo/trabajo_de_grado/point_cloud_segmentation/point_cloud_project/sequential_reconstruction/scene_dense.ply'
nube_ply = o3d.io.read_point_cloud(ply_file)
nube_ply = np.asarray(nube_ply.points)  # Convertir la nube PLY a array Nx3

# Paso 3: Construir un KDTree con la nube de puntos PLY
tree = KDTree(nube_ply)

# Paso 4: Encontrar los puntos más cercanos de la nube NPY en la nube PLY (usando solo x, y, z)
distancias, indices = tree.query(nube_npy_xyz, k=1500)  # k=1 para el punto más cercano

# Obtener los puntos más cercanos
puntos_cercanos = nube_ply[indices]

# Obtener los puntos más cercanos y asegurarnos de que sean un arreglo 2D
puntos_cercanos = nube_ply[indices].reshape(-1, 3)  # Asegurarse de que sea 2D (Nx3)

# Paso 5: Eliminar puntos duplicados
puntos_cercanos = np.unique(puntos_cercanos, axis=0)

# (Opcional) Guardar los puntos cercanos si es necesario
save_npy = npy_folder + 'pts_clase_2_dense.npy'
np.save(save_npy, puntos_cercanos)
