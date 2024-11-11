from resources.calibrate import calibrate, create_matrix, load_calibration

folder_imgs_root = 'C:/camilo/trabajo_de_grado/pcs/images_calibration/'
folder_imgs = {
    'aguacate'  : folder_imgs_root+'aguacate/',
    'monumento' : folder_imgs_root+'monumento/'
}

folder_save_root = 'C:/camilo/trabajo_de_grado/pcs/calibration_matrix/'
files_save = {
    'aguacate'  : folder_save_root+'xiaomi_redmi_note_11.pkl',
    'monumento' : folder_save_root+'iphone_12_pro_max.pkl',
    'park'      : folder_save_root+'dji_FC300S.pkl',
    'banano'    : folder_save_root+'NIKON_D3200.pkl'
}

"""
calibrate(folder_imgs['aguacate'], files_save['aguacate'], (17,11), 6, 'jpg')
"""

"""
# Para el conjunto de datos del parque
fx = 2555.9105431309904153354632587859
fy = 2555.9105431309904153354632587859
cx = 2000
cy = 1500

create_matrix(fx, cx, fy, cy, files_save['park'])
"""

"""
# Para el conjunto de datos del banano
fx = 5186.2068965517241379310344827586
fy = 5186.2068965517241379310344827586
cx = 1504
cy = 1000

create_matrix(fx, cx, fy, cy, files_save['banano'])
"""

"""
        "focal_x": 1.7269554217135585,
        "focal_y": 1.7269554217135585,
        "c_x": -0.0008813644367811352,
        "c_y": -0.0007272242436263701,
        
        '{Fx};0;{Cx};0;{Fy};{Cy};0;0;1'
"""
matrix = load_calibration(files_save['park'])
print(f'\nLos valores de la matriz de calibración son:\n    {matrix}')