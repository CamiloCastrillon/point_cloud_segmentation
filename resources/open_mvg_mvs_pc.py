import subprocess
import os
import open3d as o3d
import pickle
import numpy as np

def initialize_paths():
    project_dir         = 'C:/camilo/trabajo_de_grado/point_cloud_segmentation/point_cloud_project/'
    calib_dir           = os.path.join(project_dir, 'calibrations/xiaomi_redmi_note_11.pkl')
    images_dir          = os.path.join(project_dir, 'dataset').replace('/', '\\')
    matches_dir         = os.path.join(project_dir, 'matches').replace('/', '\\')
    reconstruction_dir  = os.path.join(project_dir, 'sequential_reconstruction/').replace('/', '\\')
    openmvg_bin_dir     = os.path.join(project_dir, 'recursos/vcpkg/installed/x64-windows/tools/openmvg/').replace('/', '\\')
    openmvs_bin_dir     = os.path.join(project_dir, 'recursos/vcpkg/installed/x64-windows/tools/openmvs/').replace('/', '\\')

    return images_dir, matches_dir, reconstruction_dir, calib_dir, openmvg_bin_dir, openmvs_bin_dir

def load_calibratrion(path_calib_params):
    # Cargar los datos desde el archivo .pkl
    with open(path_calib_params, 'rb') as file:
        calibration_data = pickle.load(file)

    # Extraer los coeficientes de distorsión
    camera_matrix   = calibration_data['camera_matrix']

    # Convertir a formato ndarray
    camera_matrix   = np.array(camera_matrix)
    Fx=camera_matrix[0][0]
    Cx=camera_matrix[0][2]
    Fy=camera_matrix[1][1]
    Cy=camera_matrix[1][2]
    text_matrix = f'{Fx};0;{Cx};0;{Fy};{Cy};0;0;1'
    #'3254.8108174801973;0;2030.0753918037567;0;3243.2048625811053;977.6552352878238;0;0;1'
    return text_matrix

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        output = result.stdout

        if output is not None:
            print("     Salida:\n", output)
        
    except subprocess.CalledProcessError as e:
        print("Error durante la ejecución del comando:")
        print("Código de salida:", e.returncode)
        print("Salida estándar:", e.stdout)
        print("Salida de error:", e.stderr)
    return None

def plot_cloud_point(reconstruction_dir):
    # Visualizar la nube de puntos con open3d
    pcd = o3d.io.read_point_cloud(f'{reconstruction_dir}scene_dense.ply')
    o3d.visualization.draw_geometries([pcd])

def work_flow(presets):

    print('\n🔽 Ejecutando el flujo de trabajo:\n')
    
    # Inizializa las rutas del proyecto
    print('   🟢 Inizializando las rutas del proyecto./n')
    images_dir, matches_dir, reconstruction_dir, calib_dir, openmvg_bin, openmvs_bin_dir = initialize_paths()

    # Carga los datos de calibración
    print('   🟢 Obteniendo datos de calibración./n')
    matrix = load_calibratrion(calib_dir)

    if 0 in presets:
        # 0 Inizializa la lista de imagenes
        print('   🟢 Inizializando la lista de imagenes.')
        command     = f'{openmvg_bin}openMVG_main_SfMInit_ImageListing -i {images_dir} -o {matches_dir} -k {matrix}' # -f 4.5 -k {matrix}
        run_command(command)
    
    if 1 in presets:
        # 1 Obtiene las caracteristicas
        print('   🟢 Obteniendo características.')
        command = (f'{openmvg_bin}openMVG_main_ComputeFeatures -i {matches_dir}\sfm_data.json -o {matches_dir} -m SIFT -p ULTRA')
        run_command(command)

    if 2 in presets:    
        # 2 Generando pares
        print('   🟢 Genera las coincidencias.')
        command = (f'{openmvg_bin}openMVG_main_PairGenerator -i {matches_dir}\sfm_data.json -o {matches_dir}\pairs.bin')
        run_command(command)
    if 3 in presets:
        # 3 Computa las coincidencias
        print('   🟢 Observando coincidencias.')
        command = (f'{openmvg_bin}openMVG_main_ComputeMatches -i {matches_dir}\sfm_data.json -p {matches_dir}\pairs.bin -o {matches_dir}\matches.putative.bin -n AUTO')
        run_command(command)
    if 4 in presets:    
        # 4 Filtra las geometrías
        print('   🟢 Filtrando geometrías.')
        command = (f'{openmvg_bin}openMVG_main_GeometricFilter -i {matches_dir}\sfm_data.json -m {matches_dir}\matches.putative.bin -o {matches_dir}\matches.f.bin')
        run_command(command)
    if 5 in presets:    
        # 5 Reconstruye caracteristicas
        print('   🟢 Reconstruyendo caracteristicas.')
        command = (f'{openmvg_bin}openMVG_main_SfM -i {matches_dir}\sfm_data.json -m {matches_dir} -o {reconstruction_dir} -s INCREMENTAL')
        run_command(command)
    if 6 in presets:    
        # 6 Convierte los datos SFM de bin a json
        print('   🟢 Conviertiendo los datos SFM de bin a json.')
        command = (f'{openmvg_bin}openMVG_main_ConvertSfM_DataFormat -i {reconstruction_dir}\sfm_data.bin -o {reconstruction_dir}\sfm_data.json')
        run_command(command)
    if 7 in presets:
        # 7 Convierte bin a formato mvs
        print('   🟢 Convirtiendo de formato mvg a mvs.')
        command = (f'{openmvg_bin}openMVG_main_openMVG2openMVS -i {reconstruction_dir}\sfm_data.bin -o {reconstruction_dir}\scene.mvs -d {reconstruction_dir}/undistorted_images')
        run_command(command)
    if 8 in presets:
        # 8 Densifica la nube de puntos
        print('   🟢 Densificando nube de puntos.')
        command = (f'{openmvs_bin_dir}DensifyPointCloud {reconstruction_dir}\scene.mvs --dense-config-file Densify.ini --resolution-level 1 --number-views 8 -w {reconstruction_dir}')
        run_command(command)
    if 9 in presets: 
        # 9 Reconstruye la maya
        print('   🟢 Reconstrueyndo la maya.')
        command = (f'{openmvs_bin_dir}ReconstructMesh {reconstruction_dir}\scene_dense.mvs -w {reconstruction_dir}')
        run_command(command)
    if 10 in presets:
        # 10 Refina la maya
        print('   🟢 Refinando la maya.')
        command = (f'{openmvs_bin_dir}RefineMesh {reconstruction_dir}\scene_dense_mesh.mvs -w {reconstruction_dir}')
        run_command(command)
    if 11 in presets:
        # 11 Crea texturas a la maya
        print('   🟢 Creando texturas.')
        command = (f'{openmvs_bin_dir}TextureMesh {reconstruction_dir}\scene_dense_mesh_refine.mvs -w {reconstruction_dir}')
        run_command(command)
    if 12 in presets:
        # 12 Grafica la nube de puntos
        print('   🟢 Graficando la nube de puntos.')
        plot_cloud_point(reconstruction_dir)

def only_densify(name_sfm, name_scene):

    print('\n🔽 Ejecutando el flujo de solo densificación:\n')
    
    # Inizializa las rutas del proyecto
    print('   🟢 Inizializando las rutas del proyecto./n')
    images_dir, matches_dir, reconstruction_dir, calib_dir, openmvg_bin, openmvs_bin_dir = initialize_paths()

    # Carga los datos de calibración
    print('   🟢 Obteniendo datos de calibración./n')
    matrix = load_calibratrion(calib_dir)

    # 0 Inizializa la lista de imagenes
    print('   🟢 Inizializando la lista de imagenes.')
    command     = f'{openmvg_bin}openMVG_main_SfMInit_ImageListing -i {images_dir} -o {matches_dir} -k {matrix}' # -f 4.5 -k {matrix}
    run_command(command)

    # 7 Convierte bin a formato mvs
    print('   🟢 Convirtiendo de formato mvg a mvs.')
    command = (f'{openmvg_bin}openMVG_main_openMVG2openMVS -i {reconstruction_dir}\{name_sfm}.bin -o {reconstruction_dir}\{name_scene}.mvs -d {reconstruction_dir}/undistorted_images')
    run_command(command)

    # 8 Densifica la nube de puntos
    print('   🟢 Densificando nube de puntos.')
    command = (f'{openmvs_bin_dir}DensifyPointCloud {reconstruction_dir}\{name_scene}.mvs --dense-config-file Densify.ini --resolution-level 1 --number-views 8 -w {reconstruction_dir}')
    run_command(command)


def main():
    entire_preset           = [0,1,2,3,4,5,6,7,8,9,10,11,12]
    to_smf_data_preset      = [0,1,2,3,4,5,6]
    name_sfm, name_scene    = 'pts_clase_0_sfm_data', 'pts_clase_0_scene'
    try:
        #work_flow(to_smf_data_preset)
        only_densify(name_sfm, name_scene)
    except Exception as e:
        print(f'\n⛔ Error:\n{e}\n')

# Ejecuta el flujo de trabajo
main()
