import re
import unicodedata
from pymongo import MongoClient # type: ignore

# Configuración de MongoDB Atlas
MONGO_URI = "mongodb+srv://admin:notoxicity67@cluster0.k7uvdoa.mongodb.net/?appName=Cluster0"

# Conectar a MongoDB (se hace UNA vez al cargar el módulo)
_cliente = MongoClient(MONGO_URI)
_db = _cliente['palabras_sensibles']  # Base de datos
_coleccion = _db['palabras_riesgo']  # Colección con las palabras

# Variable cache para evitar leer MongoDB cada vez (opcional)
_cache_palabras = None


def cargar_palabras_riesgo():
    """Carga palabras desde MongoDB (soporta formato anidado)"""
    global _cache_palabras
    
    if _cache_palabras is not None:
        return _cache_palabras
    
    palabras_por_categoria = {}
    
    # Buscar el documento principal
    doc = _coleccion.find_one({})
    
    if not doc:
        print("No se encontraron datos en MongoDB")
        return {}
    
    # Recorrer todas las categorías en el documento
    for categoria, palabras in doc.items():
        if categoria.startswith('_'):  # Saltar _id
            continue
        
        if isinstance(palabras, list):
            palabras_por_categoria[categoria] = palabras
    
    _cache_palabras = palabras_por_categoria
    print(f"Cargadas {sum(len(p) for p in palabras_por_categoria.values())} palabras en {len(palabras_por_categoria)} categorías")
    
    return palabras_por_categoria


def quitar_tildes(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )


def normalizar_texto(texto):
    if not isinstance(texto, str):
        return ""
    texto = texto.lower()
    texto = quitar_tildes(texto)
    texto = re.sub(r'[^a-zñ\s]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto


def detectar_riesgo(texto, palabras_riesgo=None):
    if palabras_riesgo is None:
        palabras_riesgo = cargar_palabras_riesgo()
    
    alertas = []
    texto_normalizado = normalizar_texto(texto)

    for tipo, lista_palabras in palabras_riesgo.items():
        for palabra in lista_palabras:
            palabra_norm = normalizar_texto(palabra)
            if re.search(rf'\b{re.escape(palabra_norm)}\b', texto_normalizado):
                alertas.append((tipo, palabra))

    return list(set(alertas))