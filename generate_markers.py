import cv2
import numpy as np
import os

# --- Configuración ---

# IMPORTANTE: Este diccionario DEBE COINCIDIR con el que se usa en DimensionsService.py
# El servicio usa: cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

# Número de marcadores a generar (se crearán los IDs desde 0 hasta N-1).
# La aplicación necesita al menos 4 para las esquinas (IDs 0, 1, 2, 3).
NUM_MARKERS_TO_GENERATE = 5

# Tamaño en píxeles de la imagen del marcador que se guardará (ancho y alto).
# Un tamaño mayor dará más resolución para imprimir.
MARKER_IMAGE_SIZE_PX = 500

# Carpeta donde se guardarán los marcadores generados.
OUTPUT_DIRECTORY = "generated_markers"


def generate_aruco_markers():
    """
    Genera imágenes de marcadores ArUco y las guarda como archivos PNG.
    Los marcadores se deben imprimir y colocar en el objeto a medir.
    """
    print("--- Iniciando la generación de marcadores ArUco ---")
    print(f"Diccionario seleccionado: DICT_4X4_50")
    print(f"Directorio de salida: ./{OUTPUT_DIRECTORY}/")

    # Crear el directorio de salida si no existe para evitar errores.
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
        print(f"Directorio '{OUTPUT_DIRECTORY}' creado exitosamente.")

    # Iterar para generar un marcador para cada ID solicitado.
    for marker_id in range(NUM_MARKERS_TO_GENERATE):
        print(f"Generando marcador con ID={marker_id}...")

        # --- LÍNEA CORREGIDA ---
        # Usamos la función moderna 'generateImageMarker' que directamente crea y devuelve la imagen del marcador.
        tag_image = cv2.aruco.generateImageMarker(ARUCO_DICT, marker_id, MARKER_IMAGE_SIZE_PX)

        # Construir el nombre del archivo de forma descriptiva.
        file_name = f"aruco_4x4_50_id_{marker_id}.png"
        file_path = os.path.join(OUTPUT_DIRECTORY, file_name)

        # Guardar la imagen del marcador en el disco.
        cv2.imwrite(file_path, tag_image)

        print(f" -> Marcador guardado correctamente en: {file_path}")

    print("\n¡Generación completada!")
    print("Ahora puedes imprimir estos marcadores desde la carpeta 'generated_markers'.")
    print("\nRECOMENDACIÓN DE COLOCACIÓN para que la API funcione:")
    print("=========================================================")
    print("  - Marcador con ID 0: Colócalo en la esquina SUPERIOR IZQUIERDA del objeto.")
    print("  - Marcador con ID 1: Colócalo en la esquina SUPERIOR DERECHA del objeto.")
    print("  - Marcador con ID 2: Colócalo en la esquina INFERIOR IZQUIERDA del objeto.")
    print("  - (ID 3 y otros son de reserva por ahora)")
    print("=========================================================")


if __name__ == "__main__":
    generate_aruco_markers()