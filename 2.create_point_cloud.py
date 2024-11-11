from resources.point_cloud import work_flow

initial_variables_aguacate = {
    'pth_root'              : 'C:/camilo/trabajo_de_grado/pcs/',
    'pth_calib'             : 'calibration_matrix/xiaomi_redmi_note_11.pkl',
    'pth_images'            : 'image_datasets/aguacate/',
    'pth_matches'           : 'sfm_projects/aguacate/matches',
    'pth_reconstruction'    : 'sfm_projects/aguacate/sequential_reconstruction',
    'pth_openmvg_bin'       : 'sfm_projects/vcpkg/installed/x64-windows/tools/openmvg/',
    'pth_openmvs_bin'       : 'sfm_projects/vcpkg/installed/x64-windows/tools/openmvs/',
    'sfm_mode'              : 'ULTRA' # NORMAL, HIGH O ULTRA
}

initial_variables_monumento_summarized = {
    'pth_root'              : 'C:/camilo/trabajo_de_grado/pcs/',
    'pth_calib'             : 'calibration_matrix/iphone_12_pro_max.pkl',
    'pth_images'            : 'image_datasets/monumento_summarized/',
    'pth_matches'           : 'sfm_projects/monumento_summarized/matches',
    'pth_reconstruction'    : 'sfm_projects/monumento_summarized/sequential_reconstruction',
    'pth_openmvg_bin'       : 'sfm_projects/vcpkg/installed/x64-windows/tools/openmvg/',
    'pth_openmvs_bin'       : 'sfm_projects/vcpkg/installed/x64-windows/tools/openmvs/',
    'sfm_mode'              : 'NORMAL' # NORMAL, HIGH O ULTRA
}

initial_variables_banano = {
    'pth_root'              : 'C:/camilo/trabajo_de_grado/pcs/',
    'pth_calib'             : 'calibration_matrix/NIKON_D3200.pkl',
    'pth_images'            : 'image_datasets/banano/',
    'pth_matches'           : 'sfm_projects/banano/matches',
    'pth_reconstruction'    : 'sfm_projects/banano/sequential_reconstruction',
    'pth_openmvg_bin'       : 'sfm_projects/vcpkg/installed/x64-windows/tools/openmvg/',
    'pth_openmvs_bin'       : 'sfm_projects/vcpkg/installed/x64-windows/tools/openmvs/',
    'sfm_mode'              : 'ULTRA' # NORMAL, HIGH O ULTRA
}

initial_variables_banano_ultra = {
    'pth_root'              : 'C:/camilo/trabajo_de_grado/pcs/',
    'pth_calib'             : 'calibration_matrix/NIKON_D3200.pkl',
    'pth_images'            : 'image_datasets/banano/',
    'pth_matches'           : 'sfm_projects/banano_ultra/matches',
    'pth_reconstruction'    : 'sfm_projects/banano_ultra/sequential_reconstruction',
    'pth_openmvg_bin'       : 'sfm_projects/vcpkg/installed/x64-windows/tools/openmvg/',
    'pth_openmvs_bin'       : 'sfm_projects/vcpkg/installed/x64-windows/tools/openmvs/',
    'sfm_mode'              : 'ULTRA' # NORMAL, HIGH O ULTRA
}

initial_variables_parque = {
    'pth_root'              : 'C:/camilo/trabajo_de_grado/pcs/',
    'pth_calib'             : 'calibration_matrix/dji_FC300S.pkl',
    'pth_images'            : 'image_datasets/parque/',
    'pth_matches'           : 'sfm_projects/parque/matches',
    'pth_reconstruction'    : 'sfm_projects/parque/sequential_reconstruction',
    'pth_openmvg_bin'       : 'sfm_projects/vcpkg/installed/x64-windows/tools/openmvg/',
    'pth_openmvs_bin'       : 'sfm_projects/vcpkg/installed/x64-windows/tools/openmvs/',
    'sfm_mode'              : 'NORMAL' # NORMAL, HIGH O ULTRA
}

work_flow(initial_variables_parque)