import json
import plotly.graph_objects as go
import pandas as pd
import numpy as np

print('inicializando rutas')
ruta_json   = 'C:/camilo/trabajo_de_grado/point_cloud_segmentation/point_cloud_project/sequential_reconstruction/pts_clase_2_sfm_data.json'
folder_npys = 'C:/camilo/trabajo_de_grado/imgs/aguacate_kmeans/'
save_points = 'C:/camilo/trabajo_de_grado/imgs/point_cloud/pc.npy'

# Cargar el archivo JSON
with open(ruta_json, 'r') as f:
    sfm_data = json.load(f)

print('Obteniendo diccionario de la relación de id e imagenes')
# Acceder a las vistas (views)
views = sfm_data.get('views', [])
dicc_class = {}
# Recorrer cada vista y obtener los atributos id_view y filename
for view in views:
    data = view['value']['ptr_wrapper']['data']
    id_view = data.get('id_view')
    filename = data.get('filename')
    path_np  = folder_npys+filename[:-4]+'_data.npy'
    source_np      = np.load(path_np)
    dicc_class[str(id_view)]  = source_np

print('Obteniendo estructura del json')
estructura = sfm_data.get('structure', [])
count = 0
puntos = []
for point in estructura:
    count           += 1
    punto_3D        = point.get('value', {}).get('X', [])
    observaciones   = point.get('value', {}).get('observations', [])
    
    obs = observaciones[1]
    np_key     = str(obs['key'])
    source_np  = dicc_class[np_key]
    y, x        = int(obs['value']['x'][0]), int(obs['value']['x'][1])
    value_class = source_np[x,y][3]
    """
    for obs in observaciones:
        np_key     = str(obs['key'])
        source_np  = dicc_class[np_key]
        x, y        = int(obs['value']['x'][0]), int(obs['value']['x'][1])
        value_class = source_np[x,y][3]

        #if [punto_3D[0], punto_3D[1], punto_3D[2]] in [punto[0], punto[1], punto[2] for punto in puntos[]]
    """
    puntos.append([punto_3D[0], punto_3D[1], punto_3D[2], value_class])

print('Exportando nube de puntos')
# Convertir el DataFrame a un array de NumPy
array_np = np.array(puntos)
# Guardar el array en un archivo .npy
#np.save(save_points, array_np)

print('Graficando')
# Extraer coordenadas y clases
x = [p[0] for p in puntos]
y = [p[1] for p in puntos]
z = [p[2] for p in puntos]
classes = [p[3] for p in puntos]

df = pd.DataFrame({'x': x, 'y': y, 'z': z, 'class': classes})

# Crear la nube de puntos usando `graph_objects`
fig = go.Figure(data=go.Scatter3d(
    x=df['x'],
    y=df['y'],
    z=df['z'],
    mode='markers',
    marker=dict(
        size=2,  # Tamaño de los puntos
        color=df['class'],  # Colores según las clases
        colorscale=['blue', 'green', 'red'],  # Mapear las clases a colores
        opacity=1
    )
))

# Personalizar el diseño
fig.update_layout(
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    ),
    title='Nube de Puntos Interactiva',
    showlegend=False  # Desactivar la leyenda
)

# Mostrar la gráfica
fig.show()