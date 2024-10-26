import json
import os
import re
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

print('inicializando rutas')
ruta_json   = 'C:/camilo/trabajo_de_grado/point_cloud_segmentation/point_cloud_project/sequential_reconstruction/sfm_data.json'
ruta_npys   = 'C:/camilo/trabajo_de_grado/imgs/aguacate_normal/'

print('Creando diccionario de dataframes')
np_ordered = sorted(os.listdir(ruta_npys), key=lambda x: int(re.match(r'\d+', x).group()))

      #1, 2,  3,  4,  5,  6,  7,  8,  9, 10, 11,12,13,14,15,16,17,18,19, 20, 21, 22, 23, 24, 25, 26, 27
ids = [0, 11, 20, 21, 22, 23, 24, 25, 26, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19]
dicc_class = {}
np_index = 0
for file_np in np_ordered:
    path_source_np = ruta_npys+file_np
    source_np      = np.load(path_source_np)
    dicc_class[str(ids[np_index])] = source_np
    np_index       += 1

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
    
    obs         = observaciones[1]
    np_key      = str(obs['key'])
    source_np   = dicc_class[np_key]
    x, y        = int(obs['value']['x'][0]), int(obs['value']['x'][1])
    rgb         = source_np[x,y]
    """
    for obs in observaciones:
        np_key     = str(obs['key'])
        source_np  = dicc_class[np_key]
        x, y        = int(obs['value']['x'][0]), int(obs['value']['x'][1])
        value_class = source_np[x,y][3]

        #if [punto_3D[0], punto_3D[1], punto_3D[2]] in [punto[0], punto[1], punto[2] for punto in puntos[]]
    """
    puntos.append([punto_3D[0], punto_3D[1], punto_3D[2], rgb[2], rgb[1], rgb[0]])

print('Graficando')
# Extraer coordenadas y clases
x = [p[0] for p in puntos]
y = [p[1] for p in puntos]
z = [p[2] for p in puntos]
r = [p[3] for p in puntos]
g = [p[4] for p in puntos]
b = [p[5] for p in puntos]

df = pd.DataFrame({'x': x, 'y': y, 'z': z, 'r': r, 'g': g, 'b': b})

# Convertir los colores RGB a un formato que Plotly pueda usar
df['color'] = df.apply(lambda row: f'rgb({row["r"]}, {row["g"]}, {row["b"]})', axis=1)

"""
# Crear la gráfica 3D
fig = px.scatter_3d(
    df, 
    x='x', 
    y='y', 
    z='z', 
    color='color',
    title='Nube de Puntos 3D',
    labels={'x': 'X', 'y': 'Y', 'z': 'Z'},
    color_discrete_sequence=df['color'],
    opacity=0.8# Utilizar los colores RGB
)

# Personalizar el diseño
fig.update_traces(marker=dict(size=2))  # Tamaño de los puntos
fig.update_layout(scene=dict(xaxis_title='X',
                              yaxis_title='Y',
                              zaxis_title='Z'))

# Desactivar la leyenda
fig.update_layout(showlegend=False)

# Mostrar la gráfica
fig.show()
"""

# Crear la gráfica 3D usando graph_objects
fig = go.Figure(data=go.Scatter3d(
    x=df['x'],
    y=df['y'],
    z=df['z'],
    mode='markers',
    marker=dict(
        size=2,  # Ajusta el tamaño de los marcadores
        color=df['color'],  # Usar los colores RGB
        opacity=0.8,  # Ajusta la opacidad si es necesario
    )
))

# Actualizar el layout de la gráfica
fig.update_layout(
    title='Nube de Puntos 3D',
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    )
)

# Mostrar la gráfica
fig.show()