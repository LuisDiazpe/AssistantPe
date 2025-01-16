# Virtual Assistant: Peruvian Style 🌎🤖🇵🇪

## Descripción 📜

Este es un **asistente virtual único** con un toque peruano. Diseñado para entretener, informar y sorprender a los usuarios, el asistente tiene una amplia gama de funciones interactivas. Ya sea para mantenerse al día con las noticias internacionales, recibir recomendaciones musicales, o simplemente pasar un buen rato jugando, este asistente tiene algo para todos.

## Características ✨

1. **Chat interactivo (¡mejorado!)**:  
   - La función de chat ahora funciona tanto en **inglés** como en **español**.  
   - Interactúa con el asistente en el idioma que prefieras.

2. **Recomendaciones musicales**:  
   - El asistente proporciona una lista de **30 canciones** seleccionadas para que disfrutes.

3. **Textos aleatorios en pantalla**:  
   - Aparecen textos al azar desde un lado de la pantalla por un tiempo limitado para sorprenderte.

4. **Noticias en múltiples idiomas**:  
   - Noticias internacionales disponibles en:  
     - Español 🇪🇸  
     - Inglés 🇺🇸  
     - Portugués 🇧🇷  
     - Italiano 🇮🇹  
   - Noticias locales de Perú en español 🇵🇪.

5. **Clima personalizado**:  
   - Informa sobre el clima actual basado en la ubicación del usuario.

6. **Entretenimiento**:  
   - Juega a las escondidas con el usuario. El asistente se esconde en la pantalla y el usuario debe encontrarlo.  
   - Muestra memes al azar para alegrar el día.  
   - Envía mensajes aleatorios cada 90 segundos para mantener la interacción.

7. **Humor impredecible**:  
   - ¡A veces "roba" el mouse del usuario para sorprenderlo! 🖱️😜

8. **Estilo único**:  
   - El asistente tiene una personalidad alegre y auténtica basada en la cultura peruana.

## Librerías utilizadas 📚

- `tkinter` - Para la interfaz gráfica de usuario.  
- `random` - Para generar acciones impredecibles y entretenidas.  
- `time` - Para gestionar tiempos y pausas en las funciones.  
- `pyautogui` - Para trabajar con coordenadas de pantalla globales.  
- `requests` - Para obtener noticias desde una API.  
- `math` - Para cálculos matemáticos en las funciones internas.  
- `Pillow (PIL)` - Para manipulación y visualización de imágenes.  
- `io` - Para gestionar flujos de datos.  
- `webbrowser` - Para abrir enlaces en el navegador.

## Instalación 🚀

1. Clona este repositorio:  
   ```bash
   git clone https://github.com/LuisDiazpe/AssistantPe.git
   ```

2. Ve al directorio del proyecto:  
   ```bash
   cd AssistantPe
   ```

3. Instala las dependencias necesarias:  
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta el asistente:  
   ```bash
   python main.py
   ```

## Requisitos 🛠️

- Python 3.8 o superior.  
- Conexión a Internet.  
- Sistema operativo compatible (Windows, macOS o Linux).

## Uso 📚

- Haz clic en los botones de la interfaz para consultar noticias internacionales en el idioma deseado.  
- Usa el botón del clima para obtener información basada en tu ubicación actual.  
- Recibe una lista de 30 canciones seleccionadas al presionar el botón de recomendaciones musicales.  
- Juega con el asistente presionando el botón "Jugar a las escondidas".  
- Interactúa con el chat en inglés o español.

## Ejemplo de interacción 💬

```plaintext
Usuario: Presiona el botón de noticias internacionales.
Asistente: Aquí están las últimas noticias internacionales: [enlace a noticias]

Usuario: Presiona el botón del clima.
Asistente: Actualmente está soleado con 25°C en tu ubicación.

Usuario: Presiona el botón para jugar a las escondidas.
Asistente: ¡Me estoy escondiendo! 👀 Encuéntrame en la pantalla

Usuario: Presiona el botón de recomendaciones musicales.
Asistente: Aquí tienes una lista de 30 canciones que podrías disfrutar:  
1. Song Title 1  
2. Song Title 2  
...  
30. Song Title 30

Usuario: Hi! How are you?
Asistente: I'm doing well, thank you. How about yourself? Do you have any plans for the weekend?

Usuario: Hablas español?
Asistente: ¡Claro que sí! ¿Cómo puedo ayudarte hoy?
```

## Contribución 🤝

1. Haz un fork del repositorio.  
2. Crea una rama para tu nueva funcionalidad:  
   ```bash
   git checkout -b nueva-funcionalidad
   ```  
3. Realiza tus cambios y haz commit:  
   ```bash
   git commit -m "Añadida nueva funcionalidad"
   ```  
4. Sube tus cambios:  
   ```bash
   git push origin nueva-funcionalidad
   ```  
5. Crea un pull request en GitHub.

## Licencia 📄

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Estructura del proyecto 📂

- **Assistant.py**: El archivo principal que contiene el código del asistente virtual.  
- **Imagenes/**: Carpeta que almacena los recursos gráficos.  
- **README.md**: Este archivo, que proporciona una descripción detallada del proyecto, cómo instalarlo, usarlo y contribuir.
- **Base de datos/**:Carpeta que contiene datos para poder mostrar en algunas funciones
