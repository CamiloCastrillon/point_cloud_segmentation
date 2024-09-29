import json
ruta_archivo = 'C:/camilo/point_cloud/repositorio/aguacate/sfm/sfm_data.json'

# Cargar el archivo JSON
with open(ruta_archivo, 'r') as f:
    sfm_data = json.load(f)

# Extraer información de cámaras, poses, y estructura
camaras = sfm_data.get('intrinsics', [])
poses = sfm_data.get('extrinsics', [])
estructura = sfm_data.get('structure', [])
"""
# Mostrar las matrices intrínsecas de las cámaras
print("Matrices intrínsecas de las cámaras:")
for cam in camaras:
    intrinsic_matrix = cam.get('value', {}).get('ptr_wrapper', {}).get('data', {}).get('value0', [])
    print(intrinsic_matrix)

# Mostrar las matrices de rotación y vectores de traslación de las poses
print("\nMatrices de rotación y vectores de traslación de las poses:")
for pose in poses:
    rotation_matrix = pose.get('value', {}).get('rotation', [])
    translation_vector = pose.get('value', {}).get('center', [])
    print(f"Rotación: {rotation_matrix}")
    print(f"Traslación: {translation_vector}")
"""
# Opcional: Mostrar la estructura (puntos 3D y sus asociaciones con vistas 2D)
print("\nEstructura (puntos 3D y asociaciones 2D):")
count = 0
for point in estructura:
    count += 1
    punto_3D = point.get('value', {}).get('X', [])
    observaciones = point.get('value', {}).get('observations', [])
    print(f"Punto 3D: {punto_3D}")
    for obs in observaciones:
        print(f" - Imagen ID: {obs['key']} con punto 2D: {obs['value']['x']}")
        

print(count)