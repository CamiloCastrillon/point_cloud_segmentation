import subprocess
import os

def bin2json(path_openmvg, path_bin, path_output):
    
    mvgtool     = path_openmvg.replace('/', '\\')+'\openMVG_main_ConvertSfM_DataFormat'
    path_bin    = path_bin.replace('/', '\\')
    path_output = path_output.replace('/', '\\')
    
    command     = f'{mvgtool} -i {path_bin} -o {path_output}'

    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        output = result.stdout
        print("Salida:\n", output)
    except subprocess.CalledProcessError as e:
        print("Error durante la ejecución del comando:")
        print("Código de salida:", e.returncode)
        print("Salida estándar:", e.stdout)
        print("Salida de error:", e.stderr)

path_openmvg    = 'C:/camilo/trabajo_de_grado/point_cloud_segmentation/recursos/vcpkg/installed/x64-windows/tools/openmvg'
path_bin        = 'C:/camilo/trabajo_de_grado/point_cloud_segmentation/reconstruction_sequential_own/aguacate/sfm_data.bin'
path_output     = 'C:/camilo/trabajo_de_grado/point_cloud_segmentation/reconstruction_sequential_own/aguacate/smf_data.json'

bin2json(path_openmvg, path_bin, path_output)