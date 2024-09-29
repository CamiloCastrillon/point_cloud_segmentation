import open3d as o3d
import numpy as np

def read_point_cloud(path_ply):
    # Leer la nube de puntos
    point_cloud = o3d.io.read_point_cloud(path_ply)
    points = np.asarray(point_cloud.points)
    return points

def project_points(points_3d, K, R, t):
    """
    Proyecta puntos 3D a coordenadas de píxeles 2D usando la matriz de proyección P = K[R|t].
    
    Args:
    - points_3d: numpy array de puntos 3D (N x 3).
    - K: Matriz intrínseca de la cámara (3 x 3).
    - R: Matriz de rotación (3 x 3).
    - t: Vector de traslación (3 x 1).

    Returns:
    - puntos_2d: numpy array de puntos 2D (N x 2).
    """
    # Convertir puntos 3D a homogéneos
    points_3d_homog = np.hstack((points_3d, np.ones((points_3d.shape[0], 1))))
    
    # Construir la matriz de proyección P
    P = K @ np.hstack((R, t.reshape(-1, 1)))
    
    # Proyectar puntos 3D a la imagen 2D
    points_2d_homog = points_3d_homog @ P.T
    
    # Convertir a coordenadas cartesianas dividiendo por z
    points_2d = points_2d_homog[:, :2] / points_2d_homog[:, 2].reshape(-1, 1)
    
    return points_2d

def backproject_pixel_to_ray(pixel, K_inv):
    """
    Calcula el rayo en 3D que corresponde a un píxel dado en la imagen.

    Args:
    - pixel: Coordenadas del píxel (u, v) en la imagen.
    - K_inv: Inversa de la matriz intrínseca de la cámara (3x3).

    Returns:
    - ray: Vector de dirección del rayo en el sistema de coordenadas de la cámara.
    """
    pixel_homog = np.array([pixel[0], pixel[1], 1.0])
    ray = K_inv @ pixel_homog
    return ray / np.linalg.norm(ray)  # Normalizar el vector

def workflow():
    """
    points = read_point_cloud("C:/camilo/point_cloud/reconstruction_sequential/aguacate/mvs/scene_dense.ply")
    
    # Supongamos que tienes los siguientes datos
    K = np.array([[f_x, 0, c_x], [0, f_y, c_y], [0, 0, 1]])  # Matriz intrínseca de la cámara
    R = np.eye(3)  # Matriz de rotación de la cámara
    t = np.array([0, 0, 0])  # Vector de traslación de la cámara

    # Proyectar puntos
    points_2d = project_points(points, K, R, t)
    
    # Ejemplo de uso de backproject_pixel_to_ray
    pixel = (x, y)
    K_inv = np.linalg.inv(K)
    ray = backproject_pixel_to_ray(pixel, K_inv)
    """
def main():
    """
    try:
        workflow()
    except Exception as e:
        print(f'\n⛔ Error:\n{e}\n')
    """
    workflow()

# Ejecuta el flujo de trabajo
main()