import cv2
import numpy as np
from fastapi import UploadFile
from app.model.DimensionsModel import DimensionsResponse

# --- CONSTANTES DE CALIBRACIÓN ---
# Medida real de un lado del marcador ArUco, en centímetros.
# ¡Este es el valor clave que nos diste!
REAL_MARKER_SIDE_CM = 13.23

# IDs de los marcadores que definen las esquinas del rectángulo a medir.
# Esquina Superior Izquierda (Top-Left)
ID_TL = 0
# Esquina Superior Derecha (Top-Right)
ID_TR = 1
# Esquina Inferior Izquierda (Bottom-Left)
ID_BL = 2
# Esquina Inferior Derecha (Bottom-Right) - Opcional, pero bueno para promediar
ID_BR = 3


# Configuración del detector ArUco (sin cambios)
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
params = cv2.aruco.DetectorParameters()
params.adaptiveThreshConstant = 20
params.adaptiveThreshWinSizeMin = 3
params.adaptiveThreshWinSizeMax = 101
params.adaptiveThreshWinSizeStep = 10
detector = cv2.aruco.ArucoDetector(aruco_dict, params)


async def calculate_dimensions(image: UploadFile) -> DimensionsResponse:
    data = await image.read()
    np_img = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("No se pudo cargar la imagen correctamente")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    corners, ids, rejected = detector.detectMarkers(gray)

    # --- LÓGICA DE DETECCIÓN MEJORADA ---

    # Validar que se detectaron marcadores
    if ids is None or len(ids) < 3:
        found_count = 0 if ids is None else len(ids)
        raise ValueError(f"Se necesitan al menos 3 marcadores (IDs {ID_TL}, {ID_TR}, {ID_BL}). Encontrados: {found_count}")

    # Aplanar el array de IDs para facilitar la búsqueda (de [[0], [2], [1]] a [0, 2, 1])
    ids_flat = ids.flatten()

    # Crear un diccionario para mapear cada ID con su array de esquinas.
    # Esta es la clave para un cálculo fiable.
    marker_map = dict(zip(ids_flat, corners))

    # Verificar si tenemos los marcadores necesarios para el cálculo.
    required_ids = [ID_TL, ID_TR, ID_BL]
    if not all(id_ in marker_map for id_ in required_ids):
        raise ValueError(f"No se encontraron todos los marcadores necesarios. Se necesitan IDs: {required_ids}. Encontrados: {list(marker_map.keys())}")

    # --- CÁLCULO DE LA RELACIÓN PÍXEL-CENTÍMETRO (CALIBRACIÓN) ---

    # Usaremos el marcador de la esquina superior izquierda (ID_TL) para calibrar.
    # Obtenemos sus 4 esquinas. El formato es [[esquina_0], [esquina_1], [esquina_2], [esquina_3]]
    # por eso el [0] extra.
    tl_marker_corners = marker_map[ID_TL][0]
    
    # Calculamos la distancia en píxeles entre su esquina superior izquierda y superior derecha.
    marker_side_px = np.linalg.norm(tl_marker_corners[0] - tl_marker_corners[1])

    # Calculamos el ratio. ¿Cuántos centímetros representa un solo píxel?
    cm_per_pixel = REAL_MARKER_SIDE_CM / marker_side_px

    # --- CÁLCULO DE DIMENSIONES FIABLE Y EN CENTÍMETROS ---

    # Obtenemos las esquinas específicas de los marcadores que nos interesan.
    # El orden de las esquinas de un marcador es: 0:TL, 1:TR, 2:BR, 3:BL
    corner_tl = marker_map[ID_TL][0][0]  # Esquina TL del marcador TL
    corner_tr = marker_map[ID_TR][0][1]  # Esquina TR del marcador TR
    corner_bl = marker_map[ID_BL][0][3]  # Esquina BL del marcador BL

    # Calcular ancho y alto en píxeles
    width_px = np.linalg.norm(corner_tr - corner_tl)
    height_px = np.linalg.norm(corner_bl - corner_tl)
    
    # Convertir las medidas finales a centímetros
    width_cm = width_px * cm_per_pixel
    height_cm = height_px * cm_per_pixel

    # (Opcional pero recomendado) Si el marcador ID 3 está presente, promediar alturas para más precisión
    if ID_BR in marker_map:
        corner_br = marker_map[ID_BR][0][2] # Esquina BR del marcador BR
        height_px_right = np.linalg.norm(corner_br - corner_tr)
        height_cm = ((height_px * cm_per_pixel) + (height_px_right * cm_per_pixel)) / 2


    # Generar la imagen de depuración (sin cambios)
    vis = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    cv2.aruco.drawDetectedMarkers(vis, corners, ids)
    for pts in rejected:
        pts = pts.reshape(-1, 2).astype(int)
        cv2.polylines(vis, [pts], True, (0, 0, 255), 2)
    cv2.imwrite("debug_detect.jpg", vis)

    return DimensionsResponse(
        width=round(width_cm, 2),
        height=round(height_cm, 2),
        unit="cm",
        message="Dimensiones calculadas exitosamente en centímetros."
    )