# Instrucciones para correr los archivos del proyecto

## Visualizar el diagrama UML (`tarea4pilares.puml`)

1. Instala la extensión de PlantUML en VS Code (recomendada) o asegúrate de tener PlantUML y Java instalados en tu sistema.
2. Abre el archivo `tarea4pilares.puml` en VS Code.
3. Haz clic derecho en el editor y selecciona "Preview Current Diagram" o usa el atajo `Alt+D` para ver el diagrama.
   - Alternativamente, puedes generar la imagen desde terminal con:
     ```powershell
     java -jar plantuml.jar tarea4pilares.puml
     ```
   Esto generará un archivo PNG con el diagrama UML.

## Ejecutar el archivo de pruebas (`test_tarea4pilares.py`)

1. Asegúrate de tener Python 3 instalado.
2. Abre una terminal en la carpeta del proyecto.
3. Ejecuta el archivo con:
   ```powershell
   python tarea1/test_tarea4pilares.py
   ```
4. Verás en consola las notificaciones simuladas y los logs de alerta generados por los sensores.

---

Si tienes dudas, revisa los comentarios en cada archivo o consulta la documentación de PlantUML y Python.
