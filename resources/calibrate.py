import cv2
import glob
import numpy as np
import pickle

def calibrate(folder_imgs:str, save_calibration:str, chessboard_size:tuple, square_size:float, format:str):
    # Configurar el tamaño del tablero de ajedrez
    chessboard_size = (17, 11)  # Número de esquinas internas por fila y columna
    square_size = 6  # Tamaño del cuadrado en unidades del mundo real (e.g., 1 cm)

    # Prepara los puntos de objeto (coordenadas 3D) para el tablero de ajedrez
    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
    objp *= square_size

    # Arreglos para guardar puntos del objeto y puntos de la imagen en todas las imágenes
    objpoints = []  # Puntos 3D en el espacio del mundo real
    imgpoints = []  # Puntos 2D en el espacio de la imagen

    # Cargar las imágenes de calibración
    images = glob.glob(folder_imgs+f'*.{format}')

    # Detectar las esquinas del tablero de ajedrez
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Encuentra las esquinas del tablero de ajedrez
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

        # Si las esquinas son encontradas, agrega puntos de objeto y puntos de imagen
        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)

            # Dibuja y muestra las esquinas
            cv2.namedWindow('Esquinas del Tablero', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Esquinas del Tablero', 1020, 459)
            cv2.drawChessboardCorners(img, chessboard_size, corners, ret)
            cv2.imshow('Esquinas del Tablero', img)
            cv2.waitKey(1000)

    cv2.destroyAllWindows()

    # Calibra la cámara
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    # Mostrar los resultados de la calibración
    print('/nMatriz de la cámara:/n', camera_matrix)
    print('/nCoeficientes de distorsión:/n', dist_coeffs)
    print('/nVectores de rotación:/n', rvecs)
    print('/nVectores de traslación:/n', tvecs)

    # Guardar los parámetros de calibración en un archivo
    calibration_data = {
        'camera_matrix': camera_matrix,
        'dist_coeffs': dist_coeffs,
        'rvecs': rvecs,
        'tvecs': tvecs
    }

    print('/nGuardando datos de calibración.')
    with open(save_calibration, 'wb') as f:
        pickle.dump(calibration_data, f)

    print('Parámetros de calibración guardados exitosamente.')

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
    return text_matrix

folder_imgs_root = 'C:/camilo/trabajo_de_grado/point_cloud_segmentation/images_calibration/'
folder_imgs = {
    'aguacate'  : folder_imgs_root+'aguacate/',
    'monumento' : folder_imgs_root+'monumento/'
}
folder_save_root = 'C:/camilo/trabajo_de_grado/point_cloud_segmentation/calibration_matrix/'
files_save = {
    'aguacate'  : folder_save_root+'xiaomi_redmi_note_11.pkl',
    'monumento' : folder_save_root+'iphone_12_pro_max.pkl'
}

#calibrate(folder_imgs['aguacate'], files_save['aguacate'], (17,11), 6, 'jpg')

t = load_calibratrion('C:/camilo/trabajo_de_grado/point_cloud_segmentation/calibration_matrix/iphone_12_pro_max.pkl')
print(t)