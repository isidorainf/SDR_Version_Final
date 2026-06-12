INSTRUCCIONES DE INSTALACIÓN Y EJECUCIÓN

1. Descargar y extraer la carpeta del proyecto.

2. Abrir la carpeta "SDR_Version_Final-master" en Visual Studio Code (debes tener habilitado del Long Path en windows: https://pip.pypa.io/warnings/enable-long-paths ).

3. Crear y activar un entorno virtual para Python:
   - Opción 1: Ingresar el codigo python -m venv .venv y luego .\.venv\Scripts\activate en la terminal
   - Opción 2: 
      - Show and Run Commands (ctrl+shift+p)
         - Create environment
         - Python 3.14
         - Seleccionar "requirements.txt"
   - Activar .\.venv\Scripts\activate

4. Instalar todas las dependencias usando el script de ayuda:
   - python helper.py install --> Solo para primera vez de ejecución 
   - pip install PyInstaller
   - pip install PyQt5

5. Ejecutar los siguientes comandos siempre que se abrá nuevamente el programa
   - python helper.py test
   - python helper.py run    
   - python helper.py build

6. Ejecutar archivo 'launch.py' para abrir el sistema
   - Clave asignada: 123456
