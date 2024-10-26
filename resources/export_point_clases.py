import numpy as np

# Define las rutas
ruta_archivo    = 'C:/camilo/trabajo_de_grado/imgs/point_cloud/pc.npy'
save_points     = 'C:/camilo/trabajo_de_grado/imgs/point_cloud/'

# Cargar el archivo .npy
array_cargado = np.load(ruta_archivo)

# Suponemos que la clase está en la columna 3
column_clases = array_cargado[:, 3]  # Extraemos la columna de clases

# Encontrar valores únicos en la columna de clases
list_clases = np.unique(column_clases)

# Obtiene los puntos por cada clase
for clase in list_clases:
    pts_clase = array_cargado[column_clases == int(clase)]
    np.save(save_points+f'pts_clase_{int(clase)}.npy', pts_clase)
