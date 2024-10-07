import open3d as o3d

# Cargar la nube de puntos desde un archivo PLY
ply_file = 'C:/camilo/trabajo_de_grado/point_cloud_segmentation/reconstruction_sequential/aguacate/mvs/scene_dense.ply'
point_cloud = o3d.io.read_point_cloud(ply_file)

# Mostrar la nube de puntos
print(point_cloud)

# Visualizar la nube de puntos
o3d.visualization.draw_geometries([point_cloud])