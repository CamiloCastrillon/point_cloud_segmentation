from resources.densify import densify_pc

npy_folder = 'C:/camilo/trabajo_de_grado/pcs/point_clouds_segmented/aguacate/non_densified_classes/'
ply_dense_path      = 'C:/camilo/trabajo_de_grado/pcs/sfm_projects/pc_aguacate/sequential_reconstruction/scene_dense.ply'
npy_dense_folder    = 'C:/camilo/trabajo_de_grado/pcs/point_clouds_segmented/aguacate/densified_classes/'

npy_files = ['pts_clase_0.npy', 'pts_clase_1.npy', 'pts_clase_2.npy',]
k_values  = [1500, 500, 100]

for npy_file, k in zip(npy_files, k_values):
    npy_path = npy_folder+npy_file
    densify_pc(npy_path, npy_file, ply_dense_path, npy_dense_folder, k)