from resources.extract_points_classes import get_sfm_point_cloud_clasify

json_path   = 'C:/camilo/trabajo_de_grado/pcs/sfm_projects/pc_aguacate/sequential_reconstruction/sfm_data.json'
folder_npys = 'C:/camilo/trabajo_de_grado/pcs/images_arrays_segmented/aguacate/'
save_points = 'C:/camilo/trabajo_de_grado/pcs/point_clouds_segmented/aguacate/'

get_sfm_point_cloud_clasify(json_path, save_points, folder_npys)