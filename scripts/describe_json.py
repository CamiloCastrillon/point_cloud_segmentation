import json
import os
import re
import plotly.express as px
import pandas as pd
import numpy as np

print('inicializando rutas')
ruta_json           = 'C:/camilo/trabajo_de_grado/point_cloud_segmentation/reconstruction_sequential_own/aguacate/sfm_data.json'
ruta_imgs_colored   = 'C:/camilo/trabajo_de_grado/imgs/aguacate_kmeans/'

print('Creando diccionario de dataframes')
np_ordered = sorted(os.listdir(ruta_imgs_colored), key=lambda x: int(re.match(r'\d+', x).group()))

dicc_class = {}
np_index = 0
for file_np in np_ordered:
    path_source_np = ruta_imgs_colored+np_ordered[np_index]
    np_index       += 1
    source_np      = np.load(path_source_np)
    dicc_class[str(np_index)] = source_np

print('Obteniendo estructura del json')
# Cargar el archivo JSON
with open(ruta_json, 'r') as f:
    sfm_data = json.load(f)
estructura = sfm_data.get('structure', [])

print('Obteniendo la información')
count = 0
puntos = []
for point in estructura:
    count           += 1
    punto_3D        = point.get('value', {}).get('X', [])
    observaciones   = point.get('value', {}).get('observations', [])
    for obs in observaciones:
        np_key     = str(obs['key']+1)
        source_np  = dicc_class[np_key]
        x, y        = int(obs['value']['x'][0]), int(obs['value']['x'][1])
        value_class = source_np[x,y][3]
    puntos.append([punto_3D[0], punto_3D[1], punto_3D[2], value_class])

print('Graficando')
# Extraer coordenadas y clases
x = [p[0] for p in puntos]
y = [p[1] for p in puntos]
z = [p[2] for p in puntos]
classes = [p[3] for p in puntos]

df = pd.DataFrame({'x': x, 'y': y, 'z': z, 'class': classes})

# Asignar colores según las clases
color_map = {0: 'red', 1: 'blue', 2: 'green'}  # Asigna un color a cada clase
df['color'] = df['class'].map(color_map)  # Mapea los colores en el DataFrame

# Crear la nube de puntos
fig = px.scatter_3d(df, x='x', y='y', z='z', color='class',
                    color_discrete_map=color_map,  # Usar el color_map definido
                    title='Nube de Puntos Interactiva',
                    opacity=1)

# Personalizar el diseño
fig.update_traces(marker=dict(size=2))  # Tamaño de los puntos
fig.update_layout(scene=dict(xaxis_title='X',
                              yaxis_title='Y',
                              zaxis_title='Z'))

# Desactivar la leyenda
fig.update_layout(showlegend=False)

# Mostrar la figura
fig.show()
