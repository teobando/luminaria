import cv2
import numpy as np
from fastapi import UploadFile
from app.model.DimensionsModel import DimensionsResponse

# Diccionario ArUco (versión contrib) y parámetros de detección
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
params = cv2.aruco.DetectorParameters()
params.adaptiveThreshConstant = 20   # prueba de 0–20
params.adaptiveThreshWinSizeMin = 3
params.adaptiveThreshWinSizeMax = 101
params.adaptiveThreshWinSizeStep = 10
detector = cv2.aruco.ArucoDetector(aruco_dict, params)

async def calculate_dimensions(image: UploadFile) -> DimensionsResponse:
    # Leer los bytes de la imagen
    data = await image.read()
    np_img = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("No se pudo cargar la imagen correctamente")

    # Gris y suavizado
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detección de marcadores
    corners, ids, rejected = detector.detectMarkers(gray)

    # Visualización de debug
    vis = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    vis = cv2.aruco.drawDetectedMarkers(vis, corners, ids)
    for pts in rejected:
        pts = pts.reshape(-1, 2).astype(int)
        cv2.polylines(vis, [pts], True, (0, 0, 255), 2)
    # Guardar en /mnt/data para poder inspeccionarlo
    cv2.imwrite("debug_detect.jpg", vis)

    # Validación
    found = 0 if ids is None else len(ids)
    if found < 4:
        raise ValueError(f"No se detectaron 4 códigos ArUco (encontrados: {found})")

    # Calcular ancho y alto con los cuatro primeros marcadores
    tl = corners[0][0][0]
    tr = corners[1][0][0]
    bl = corners[2][0][0]

    width = np.linalg.norm(tr - tl)
    height = np.linalg.norm(bl - tl)

    return DimensionsResponse(
        width=width,
        height=height,
        message="Dimensiones calculadas exitosamente"
    )
