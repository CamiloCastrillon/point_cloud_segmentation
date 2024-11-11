import subprocess
import os
import sys
from resources.calibrate import load_calibration

def initialize_paths(initial_variables:dict):
    project_dir         = initial_variables['pth_root']
    calib_dir           = os.path.join(project_dir, initial_variables['pth_calib']).replace('/', '\\')
    images_dir          = os.path.join(project_dir, initial_variables['pth_images']).replace('/', '\\')
    matches_dir         = os.path.join(project_dir, initial_variables['pth_matches']).replace('/', '\\')
    reconstruction_dir  = os.path.join(project_dir, initial_variables['pth_reconstruction']).replace('/', '\\')
    openmvg_bin_dir     = os.path.join(project_dir, initial_variables['pth_openmvg_bin']).replace('/', '\\')
    openmvs_bin_dir     = os.path.join(project_dir, initial_variables['pth_openmvs_bin']).replace('/', '\\')
    sfm_mode            = initial_variables['sfm_mode']
    return images_dir, matches_dir, reconstruction_dir, calib_dir, openmvg_bin_dir, openmvs_bin_dir, sfm_mode

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        output = result.stdout

        if output is not None or output != ' ':
            print("     Salida:\n", output)
        
    except subprocess.CalledProcessError as e:
        print("Error durante la ejecución del comando:")
        print("Código de salida:", e.returncode)
        print("Salida estándar:", e.stdout)
        print("Salida de error:", e.stderr)
        sys.exit(1)
    return None

def work_flow(initial_variables):

    print('\n🔽 Ejecutando el flujo de trabajo:\n')
    
    # Inizializa las rutas del proyecto
    print('   🟢 Inizializando las rutas del proyecto.\n')
    images_dir, matches_dir, reconstruction_dir, calib_dir, openmvg_bin_dir, openmvs_bin_dir, sfm_mode = initialize_paths(initial_variables)
    for key, value in initial_variables.items():
        print(f'    ->{key} = {value}')
        
    # Carga los datos de calibración
    print('\n   🟢 Obteniendo datos de calibración.\n')
    matrix = load_calibration(calib_dir)
    
    # 0 Inizializa la lista de imagenes
    print('   🟢 Inizializando la lista de imagenes.')
    command     = f'{openmvg_bin_dir}openMVG_main_SfMInit_ImageListing -i {images_dir} -o {matches_dir} -k {matrix}'
    run_command(command)

    # 1 Obtiene las caracteristicas
    print('   🟢 Obteniendo características.')
    command = (f'{openmvg_bin_dir}openMVG_main_ComputeFeatures -i {matches_dir}\sfm_data.json -o {matches_dir} -m SIFT -p {sfm_mode}')
    run_command(command)

    # 2 Generando pares
    print('   🟢 Genera las coincidencias.')
    command = (f'{openmvg_bin_dir}openMVG_main_PairGenerator -i {matches_dir}\sfm_data.json -o {matches_dir}\pairs.bin')
    run_command(command)

    # 3 Computa las coincidencias
    print('   🟢 Observando coincidencias.')
    command = (f'{openmvg_bin_dir}openMVG_main_ComputeMatches -i {matches_dir}\sfm_data.json -p {matches_dir}\pairs.bin -o {matches_dir}\matches.putative.bin -n AUTO')
    run_command(command)

    # 4 Filtra las geometrías
    print('   🟢 Filtrando geometrías.')
    command = (f'{openmvg_bin_dir}openMVG_main_GeometricFilter -i {matches_dir}\sfm_data.json -m {matches_dir}\matches.putative.bin -o {matches_dir}\matches.f.bin')
    run_command(command)

    # 5 Reconstruye caracteristicas
    print('   🟢 Reconstruyendo caracteristicas.')
    command = (f'{openmvg_bin_dir}openMVG_main_SfM -i {matches_dir}\sfm_data.json -m {matches_dir} -o {reconstruction_dir} -s INCREMENTAL')
    run_command(command)

    # 6 Convierte los datos SFM de bin a json
    print('   🟢 Conviertiendo los datos SFM de bin a json.')
    command = (f'{openmvg_bin_dir}openMVG_main_ConvertSfM_DataFormat -i {reconstruction_dir}\sfm_data.bin -o {reconstruction_dir}\sfm_data.json')
    run_command(command)

    # 7 Convierte bin a formato mvs
    print('   🟢 Convirtiendo de formato mvg a mvs.')
    command = (f'{openmvg_bin_dir}openMVG_main_openMVG2openMVS -i {reconstruction_dir}\sfm_data.bin -o {reconstruction_dir}\scene.mvs -d {reconstruction_dir}/undistorted_images')
    run_command(command)

    # 8 Densifica la nube de puntos
    print('   🟢 Densificando nube de puntos.')
    command = (f'{openmvs_bin_dir}DensifyPointCloud {reconstruction_dir}\scene.mvs --dense-config-file Densify.ini --resolution-level 1 --number-views 8 -w {reconstruction_dir}')
    run_command(command)

    # 9 Reconstruye la maya
    print('   🟢 Reconstrueyndo la maya.')
    command = (f'{openmvs_bin_dir}ReconstructMesh {reconstruction_dir}\scene_dense.mvs -w {reconstruction_dir}')
    run_command(command)

    # 10 Refina la maya
    print('   🟢 Refinando la maya.')
    command = (f'{openmvs_bin_dir}RefineMesh {reconstruction_dir}\scene_dense_mesh.mvs -w {reconstruction_dir}')
    run_command(command)

    # 11 Crea texturas a la maya
    print('   🟢 Creando texturas.')
    command = (f'{openmvs_bin_dir}TextureMesh {reconstruction_dir}\scene_dense_mesh_refine.mvs -w {reconstruction_dir}')
    run_command(command)

    print('\n\nPROCESO FINALIZADO.')