# afectivo.py
from detoxify import Detoxify

# Inicializar modelo UNA vez
_modelo = Detoxify('multilingual')

def analizar_intencion(texto):
    """
    Recibe texto, devuelve un string con la intención afectiva del mensaje.
    Ejemplo: "El mensaje es negativo porque contiene un insulto y tiene tono de amenaza"
    """
    if not texto or len(texto) < 3:
        return "El mensaje es demasiado corto para analizar."
    
    resultado = _modelo.predict(texto)
    
    # Extraer puntuaciones
    toxicidad = resultado.get('toxicity', 0)
    insulto = resultado.get('insult', 0)
    amenaza = resultado.get('threat', 0)
    odio = resultado.get('identity_hate', 0)
    obsceno = resultado.get('obscene', 0)
    
    # Construir la explicación
    problemas = []
    
    if insulto > 0.6:
        problemas.append("contiene un insulto directo")
    elif insulto > 0.3:
        problemas.append("podría contener un insulto")
        
    if amenaza > 0.5:
        problemas.append("incluye una amenaza")
    elif amenaza > 0.3:
        problemas.append("podría interpretarse como amenaza")
        
    if odio > 0.6:
        problemas.append("expresa discurso de odio")
    elif odio > 0.3:
        problemas.append("tiene carga de odio")
        
    if obsceno > 0.6:
        problemas.append("usa lenguaje obsceno")
        
    if toxicidad > 0.7 and not problemas:
        problemas.append("tiene un tono agresivo o negativo")
    
    # Si no hay nada detectado
    if not problemas:
        return "El mensaje no muestra intenciones negativas significativas."
    
    # Armar la frase final
    if len(problemas) == 1:
        return f"La intención de este mensaje es negativa porque {problemas[0]}."
    else:
        return f"La intención de este mensaje es negativa porque {', '.join(problemas[:-1])} y además {problemas[-1]}."