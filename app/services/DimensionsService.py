import cv2
import numpy as np
from io import BytesIO
from app.model.DimensionsModel import DimensionsResponse

async def calculate_dimensions(image: BytesIO) -> DimensionsResponse:
    # Convertir la imagen a un formato adecuado para OpenCV
    np_image = np.frombuffer(image.read(), np.uint8)
    img = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

    # Convertir a escala de grises para facilitar el procesamiento
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Cargar el diccionario de ArUco
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
    parameters = cv2.aruco.DetectorParameters_create()

    # Detectar los marcadores ArUco
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # Si no se encuentran los 4 marcadores, lanzar un error
    if len(corners) < 4:
        raise ValueError("No se detectaron 4 códigos ArUco")

    # Supongamos que los códigos están en las 4 esquinas de un rectángulo
    corner1 = corners[0][0][0]  # Primera esquina (arriba-izquierda)
    corner2 = corners[1][0][0]  # Segunda esquina (arriba-derecha)
    corner3 = corners[2][0][0]  # Tercera esquina (abajo-izquierda)
    corner4 = corners[3][0][0]  # Cuarta esquina (abajo-derecha)

    # Calcular el largo (distancia entre corner1 y corner2)
    width = np.linalg.norm(corner2 - corner1)

    # Calcular el alto (distancia entre corner1 y corner3)
    height = np.linalg.norm(corner3 - corner1)

    return DimensionsResponse(width=width, height=height, message="Dimensiones calculadas exitosamente")
