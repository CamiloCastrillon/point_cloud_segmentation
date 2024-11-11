import json
import numpy as np
import open3d as o3d

def open_json(json_path):
    # Cargar el archivo JSON
    with open(json_path, 'r') as f:
        sfm_data = json.load(f)
    return sfm_data

def identify_image_order(sfm_data, folder_npy):
    # Acceder a las vistas (views)
    views       = sfm_data.get('views', [])
    dict_correlation  = {}
    # Recorrer cada vista y obtener los atributos id_view y filename
    for view in views:
        data                            = view['value']['ptr_wrapper']['data']
        id_view                         = data.get('id_view')
        filename                        = data.get('filename')
        path_np                         = folder_npy+filename[:-4]+'.npy'
        source_np                       = np.load(path_np)
        dict_correlation[str(id_view)]  = source_np
    return dict_correlation

def get_sfm_point_cloud_clasify(json_path, save_points, folder_npy):
    sfm_data            = open_json(json_path)
    dict_correlation    = identify_image_order(sfm_data, folder_npy)
    estructura          = sfm_data.get('structure', [])
    count               = 0
    puntos              = []
    
    for point in estructura:
        count           += 1
        punto_3D        = point.get('value', {}).get('X', [])
        observaciones   = point.get('value', {}).get('observations', [])
        
        obs         = observaciones[1]
        np_key      = str(obs['key'])
        source_np   = dict_correlation[np_key]
        y, x        = int(obs['value']['x'][0]), int(obs['value']['x'][1])
        value_class = source_np[x,y][3]
        puntos.append([punto_3D[0], punto_3D[1], punto_3D[2], value_class])

    array_np = np.array(puntos)
    # Guardar el array en un archivo .npy
    np.save(save_points+'full_point_cloud', array_np)
    print(f'Puntos clasificados y guardados en:{save_points}')

def extract_point_classes(npy_path, folder_save):
    # Cargar el archivo .npy
    array_cargado = np.load(npy_path)

    # Suponemos que la clase está en la columna 3
    column_clases = array_cargado[:, 3]  # Extraemos la columna de clases

    # Encontrar valores únicos en la columna de clases
    list_clases = np.unique(column_clases)

    # Obtiene los puntos por cada clase
    for clase in list_clases:
        pts_clase = array_cargado[column_clases == int(clase)]
        ply_pts = pts_clase[:, :3]
        # Crear un objeto PointCloud en open3d y asignar las coordenadas
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(ply_pts)

        # Guardar el archivo como .ply
        o3d.io.write_point_cloud(folder_save+f'pts_clase_{int(clase)}.ply', point_cloud)
        # Guarda el archivo .npy
        np.save(folder_save+f'pts_clase_{int(clase)}.npy', pts_clase)
