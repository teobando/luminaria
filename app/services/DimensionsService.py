import cv2
import numpy as np
from app.model.DimensionsModel import DimensionsResponse

# Diccionario ArUco (versión contrib)
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
# Parámetros del detector (nueva forma en OpenCV >=4.7)
parameters = cv2.aruco.DetectorParameters()

async def calculate_dimensions(image) -> DimensionsResponse:
    # Leer los bytes de la imagen y convertir a array de NumPy
    image_data = await image.read()
    np_image = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("No se pudo cargar la imagen correctamente")

    # Convertir a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detectar los marcadores ArUco
    corners, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # Verificar que haya al menos 4 marcadores
    if len(corners) < 4:
        raise ValueError("No se detectaron 4 códigos ArUco")

    # Tomar las esquinas de los primeros 4 marcadores
    corner1 = corners[0][0][0]  # arriba-izquierda
    corner2 = corners[1][0][0]  # arriba-derecha
    corner3 = corners[2][0][0]  # abajo-izquierda
    corner4 = corners[3][0][0]  # abajo-derecha

    # Calcular ancho (distancia entre corner1 y corner2)
    width = np.linalg.norm(corner2 - corner1)

    # Calcular alto (distancia entre corner1 y corner3)
    height = np.linalg.norm(corner3 - corner1)

    return DimensionsResponse(
        width=width,
        height=height,
        message="Dimensiones calculadas exitosamente"
    )
