import subprocess
import os
import open3d as o3d
import pickle
import numpy as np

def initialize_paths():
    project_dir         = 'C:/camilo/point_cloud/'
    calib_dir           = 'C:/camilo/calibrate_camera/xiaomi_redmi_note_11.pkl'
    images_dir          = os.path.join(project_dir, 'images/aguacate/')
    matches_dir         = os.path.join(project_dir, 'matches/aguacate/')
    reconstruction_dir  = os.path.join(project_dir, 'reconstruction_sequential/aguacate/')

    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(matches_dir, exist_ok=True)
    os.makedirs(reconstruction_dir, exist_ok=True)

    return images_dir, matches_dir, reconstruction_dir, calib_dir

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
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f'Error: {result.stderr}')
    else:
        print(result.stdout)
    
    return result

def plot_cloud_point(reconstruction_dir):
    # Visualizar la nube de puntos con open3d
    pcd = o3d.io.read_point_cloud(f'{reconstruction_dir}scene_dense.ply')
    o3d.visualization.draw_geometries([pcd])
    
def work_flow():
    print('\n🔽 Ejecutando el flujo de trabajo:\n')
    
    # Inizializa las rutas del proyecto
    print('   🟢 Inizializando las rutas del proyecto.\n')
    images_dir, matches_dir, reconstruction_dir, calib_dir = initialize_paths()
    
    # Carga los datos de calibración
    print('   🟢 Obteniendo datos de calibración.\n')
    #matrix = load_calibratrion(calib_dir)

    # 0 Inizializa la lista de imagenes
    print('   🟢 Inizializando la lista de imagenes.')
    command     = f'openMVG_main_SfMInit_ImageListing -i {images_dir} -o {matches_dir} -k 3254.8108174801973;0;2030.0753918037567;0;3243.2048625811053;977.6552352878238;0;0;1' # -f 4.5 -k {matrix}
    run_command(command)
    
    # 1 Obtiene las caracteristicas
    print('   🟢 Obteniendo características.')
    command = (f'openMVG_main_ComputeFeatures -i {matches_dir}sfm_data.json -o {matches_dir} -m SIFT -p ULTRA')
    run_command(command)
    
    # 2 Generando pares
    print('   🟢 Genera las coincidencias.')
    command = (f'openMVG_main_PairGenerator -i {matches_dir}sfm_data.json -o {matches_dir}pairs.bin')
    run_command(command)
    
    # 3 Computa las coincidencias
    print('   🟢 Observando coincidencias.')
    command = (f'openMVG_main_ComputeMatches -i {matches_dir}sfm_data.json -p {matches_dir}pairs.bin -o {matches_dir}mmatches.putative.bin -n AUTO')
    run_command(command)
    
    # 4 Filtra las geometrías
    print('   🟢 Filtrando geometrías.')
    command = (f'openMVG_main_GeometricFilter -i {matches_dir}sfm_data.json -m {matches_dir}matches.putative.bin -o {matches_dir}matches_final.txt')
    run_command(command)
       
    # 5 Reconstruye caracteristicas
    print('   🟢 Reconstruyendo caracteristicas.')
    command = (f'openMVG_main_SfM -i {matches_dir}sfm_data.json --match_file {matches_dir}matches_final.txt -o {reconstruction_dir} -s INCREMENTAL')
    run_command(command)
    
    # 6 Convierte a formato mvs
    print('   🟢 Convirtiendo de formato mvg a mvs.')
    command = (f'openMVG_main_openMVG2openMVS -i {reconstruction_dir}sfm_data.bin -o {reconstruction_dir}scene.mvs')
    run_command(command)
    
    # 7 Densifica la nube de puntos
    print('   🟢 Densificando nube de puntos.')
    command = (f'DensifyPointCloud {reconstruction_dir}scene.mvs')
    run_command(command)
    
    # Convierte la nube de puntos a un formato diferente
    print('   🟢 Convirtiendo de formato mvs a ply.')
    command = (f'ReconstructMesh -i {reconstruction_dir}scene_dense.mvs -o {reconstruction_dir}scene_dense.ply')
    run_command(command)
    
    # Grafica la nube de puntos
    print('   🟢 Graficando la nube de puntos.')
    plot_cloud_point(reconstruction_dir)

def main():
    try:
        work_flow()
    except Exception as e:
        print(f'\n⛔ Error:\n{e}\n')

# Ejecuta el flujo de trabajo
main()
