from resources.extract_points_classes import extract_point_classes

npy_path    = 'C:/camilo/trabajo_de_grado/pcs/point_clouds_segmented/aguacate/full_point_cloud.npy'
folder_save = 'C:/camilo/trabajo_de_grado/pcs/point_clouds_segmented/aguacate/non_densified_classes/'

extract_point_classes(npy_path, folder_save)