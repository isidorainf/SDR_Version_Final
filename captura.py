import mss
import numpy as np
import easyocr
import cv2

# Inicializar el lector una sola vez (fuera de la función para eficiencia)
reader = easyocr.Reader(['es', 'en'])

def capturar_y_extraer():
    with mss.mss() as sct:
        # Capturar el monitor principal
        screenshot = sct.grab(sct.monitors[1])
        
        # Convertir a array numpy
        img_np = np.array(screenshot)
        
        # Extraer texto
        resultado = reader.readtext(img_np, detail=0)
        texto = " ".join(resultado)
        return texto