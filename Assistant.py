import tkinter as tk
import random
import time
import pyautogui  
import requests  
import math
from PIL import Image, ImageTk
import io
import webbrowser

class Assistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Asistente Personal")

        # Hacer la ventana sin bordes y siempre visible
        self.root.overrideredirect(1)  # Sin bordes
        self.root.attributes('-topmost', True)  # Siempre encima
        self.root.attributes('-transparentcolor', 'white')  # Color transparente

        # Obtener dimensiones de la pantalla
        self.screen_width = pyautogui.size().width
        self.screen_height = pyautogui.size().height

        # Configuración del canvas con fondo transparente
        self.canvas = tk.Canvas(self.root, width=100, height=100, bg="white", highlightthickness=0)
        self.canvas.pack()

        # Crear personaje
        self.character = self.canvas.create_oval(10, 10, 90, 90, fill="blue", outline="black")

        # Variables de movimiento
        self.angle = random.uniform(0, 2 * math.pi)  # Ángulo de dirección inicial
        self.speed = 5  # Velocidad inicial
        self.following = False
        self.mouse_captured = False
        self.hidden = False

        # Evento para clic en el personaje
        self.canvas.tag_bind(self.character, "<Button-1>", self.show_menu)

        # Movimiento inicial
        self.move_character()

        # Iniciar temporizador para persecución
        self.schedule_mouse_chase()

    def move_character(self):
        if self.hidden:  # Detener movimiento si el asistente está escondido
            return

        # Obtener posición actual de la ventana
        window_x = self.root.winfo_x()
        window_y = self.root.winfo_y()

        if random.random() < 0.01:  # Pausa breve
            self.root.after(300, self.move_character)
            return

        # Cambiar ligeramente el ángulo para crear movimiento curvo
        self.angle += random.uniform(-0.1, 0.1)

        # Calcular nueva posición
        dx = math.cos(self.angle) * self.speed
        dy = math.sin(self.angle) * self.speed
        new_x = window_x + dx
        new_y = window_y + dy

        # Ajustar dirección cerca de los bordes
        if new_x <= 0 or new_x + 100 >= self.screen_width:
            self.angle = math.pi - self.angle  # Invertir ángulo horizontal
            new_x = max(0, min(self.screen_width - 100, new_x))
        if new_y <= 0 or new_y + 100 >= self.screen_height:
            self.angle = -self.angle  # Invertir ángulo vertical
            new_y = max(0, min(self.screen_height - 100, new_y))

        # Actualizar posición de la ventana
        self.root.geometry(f"+{int(new_x)}+{int(new_y)}")

        # Continuar movimiento si no está siguiendo el mouse o capturando el mouse
        if not self.following and not self.mouse_captured:
            self.root.after(50, self.move_character)

    def schedule_mouse_chase(self):
        # Configurar para que cada 30 minutos verifique si persigue el mouse
        def check_chase():
            if random.random() < 0.63:  # 63% de probabilidad
                self.start_mouse_chase()
            self.root.after(30 * 60 * 1000, check_chase)  # Reintentar en 30 minutos

        self.root.after(30 * 60 * 1000, check_chase)  # Primera ejecución en 30 minutos

    def start_mouse_chase(self):
        self.following = True
        self.speed = 5  # Restablecer velocidad inicial
        start_time = time.time()

        def chase():
            nonlocal start_time
            elapsed = time.time() - start_time

            # Aumentar velocidad cada 2 segundos
            if int(elapsed) % 2 == 0:
                self.speed += 1

            mouse_x, mouse_y = pyautogui.position()
            char_x, char_y = self.get_center()
            dx = (mouse_x - char_x) / 15 * self.speed / 5
            dy = (mouse_y - char_y) / 15 * self.speed / 5

            new_x = self.root.winfo_x() + dx
            new_y = self.root.winfo_y() + dy

            # Ajustar límites para que no se salga de la pantalla
            new_x = max(0, min(self.screen_width - 100, new_x))
            new_y = max(0, min(self.screen_height - 100, new_y))

            self.root.geometry(f"+{int(new_x)}+{int(new_y)}")

            # Verificar si capturó el mouse
            if abs(mouse_x - char_x) < 20 and abs(mouse_y - char_y) < 20:
                self.capture_mouse()
            else:
                self.root.after(30, chase)

        chase()

    def capture_mouse(self):
        print("¡Mouse capturado!")
        self.mouse_captured = True

        def move_with_mouse():
            if not self.mouse_captured:
                return

            # Movimiento continuo mientras el mouse está capturado
            self.angle += random.uniform(-0.1, 0.1)  # Cambiar ángulo
            dx = math.cos(self.angle) * self.speed
            dy = math.sin(self.angle) * self.speed

            new_x = self.root.winfo_x() + dx + random.randint(-20, 20)
            new_y = self.root.winfo_y() + dy + random.randint(-20, 20)

            # Ajustar límites para que no se salga de la pantalla
            new_x = max(0, min(self.screen_width - 100, new_x))
            new_y = max(0, min(self.screen_height - 100, new_y))

            # Actualizar posición del asistente y mover el mouse con él
            self.root.geometry(f"+{int(new_x)}+{int(new_y)}")
            pyautogui.moveTo(new_x + 50, new_y + 50, duration=0.1)  # Mantener el mouse centrado en el asistente

            self.root.after(50, move_with_mouse)

        def release_mouse():
            self.mouse_captured = False
            self.following = False
            self.speed = 5  # Restaurar velocidad
            self.move_character()
            print("Mouse liberado")

        move_with_mouse()
        self.root.after(11000, release_mouse)  # Soltar el mouse después de 11 segundos

    def get_center(self):
        window_x = self.root.winfo_x()
        window_y = self.root.winfo_y()
        return window_x + 50, window_y + 50  # Centro del personaje

    def show_menu(self, event):
        # Mostrar un menú con opciones
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Noticias", command=self.show_news_categories)
        menu.add_command(label="Clima", command=self.show_weather)
        menu.add_command(label="Jugar a las escondidas", command=self.play_hide_and_seek)
        menu.add_command(label="Cerrar", command=self.close_assistant)
        menu.post(event.x_root, event.y_root)

    def show_news_categories(self):
        # Mostrar categorías de noticias
        categories_window = tk.Toplevel(self.root)
        categories_window.title("Categorías de Noticias")
        categories_window.geometry("300x300")
        categories_window.configure(bg="lightgray")

        self.add_category_button(categories_window, "Noticias Internacionales", "international", "Imagenes/mundo.png")
        self.add_category_button(categories_window, "Noticias de Perú", "peru", "Imagenes/peru.png")
        self.add_category_button(categories_window, "Noticias de Fútbol", "sports", "Imagenes/futbol.png")

    def add_category_button(self, parent, text, category, image_path):
        try:
            img = Image.open(image_path)
            img = img.resize((300, 80))  # Ajustar tamaño de fondo
            photo = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"No se pudo cargar la imagen {image_path}: {e}")
            photo = None

        button = tk.Button(
            parent, text=text, font=("Arial", 14, "bold"), command=lambda: self.show_news_interface(category),
            compound="center", image=photo, bg="white"
        )
        button.image = photo  # Mantener referencia de la imagen
        button.pack(pady=10, padx=10, fill=tk.X)

    def show_news_interface(self, category):
        # Crear una nueva ventana para mostrar las noticias
        news_window = tk.Toplevel(self.root)
        news_window.title("Noticias")
        news_window.geometry("800x900")

        # Etiqueta de título
        title = tk.Label(news_window, text=f"Noticias de {category.capitalize()}", font=("Arial", 24, "bold"), bg="lightgray")
        title.pack(pady=20)

        # Marco de desplazamiento para noticias
        canvas = tk.Canvas(news_window, bg="lightgray", highlightthickness=0)
        scrollbar = tk.Scrollbar(news_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="lightgray")

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        loading_label = tk.Label(news_window, text="Cargando noticias...", font=("Arial", 14), bg="lightgray")
        loading_label.pack(pady=10)

        def fetch_and_display_news():
            loading_label.destroy()

            # Obtener noticias desde la API
            try:
                api_key = "pub_63621582321df3583172d78579eaf41a4319b"  # Clave de NewsAPI 
                if category == "peru":
                    url = f"https://newsdata.io/api/1/news?country=pe&language=es&apikey={api_key}"
                else:
                    category_map = {
                        "international": "world",
                        "sports": "sports",
                    }
                    language_map = {
                        "international": "es,en,pt,it",
                        "sports": "es,en",
                    }
                    selected_category = category_map.get(category, "world")
                    languages = language_map.get(category, "en")
                    url = f"https://newsdata.io/api/1/news?category={selected_category}&language={languages}&apikey={api_key}"

                response = requests.get(url)
                response.raise_for_status()  # Lanzar excepción si la respuesta HTTP contiene un error
                news = response.json()

                # Validar que existan resultados
                if not news.get('results'):
                    error_label = tk.Label(scrollable_frame, text="No se encontraron noticias.", bg="white", fg="red")
                    error_label.pack(pady=10)
                    return

                # Mostrar las primeras noticias con enlaces
                for article in news.get('results', []):
                    if 'title' in article and article['title']:
                        article_frame = tk.Frame(scrollable_frame, bg="white", relief=tk.RIDGE, borderwidth=2)
                        article_frame.pack(fill=tk.X, pady=10, padx=10)

                        # Mostrar imagen si está disponible
                        if 'image_url' in article and article['image_url']:
                            try:
                                img_data = requests.get(article['image_url']).content
                                img = Image.open(io.BytesIO(img_data))
                                img = img.resize((100, 100)) 
                                photo = ImageTk.PhotoImage(img)
                                img_label = tk.Label(article_frame, image=photo, bg="white")
                                img_label.image = photo  # Mantener referencia para evitar recolección de basura
                                img_label.pack(side=tk.LEFT, padx=10)
                            except Exception as e:
                                print(f"No se pudo cargar la imagen: {e}")

                        # Mostrar el título de la noticia
                        headline = tk.Label(
                            article_frame, text=article['title'], wraplength=600, justify=tk.LEFT, bg="white", font=("Arial", 14, "bold"), fg="blue", cursor="hand2"
                        )
                        headline.pack(anchor="w", padx=10, pady=5)

                        def open_article(url=article.get('link', '#')):
                            if url != "#":
                                webbrowser.open(url)

                        headline.bind("<Button-1>", lambda e, url=article.get('link', '#'): open_article(url))

                        # Mostrar la descripción si está disponible
                        if 'description' in article and article['description']:
                            description = tk.Label(
                                article_frame, text=article['description'], wraplength=600, justify=tk.LEFT, bg="white", font=("Arial", 12)
                            )
                            description.pack(anchor="w", padx=10, pady=5)
            except requests.RequestException as e:
                error_label = tk.Label(scrollable_frame, text=f"Error al obtener noticias: {e}", bg="white", fg="red")
                error_label.pack(pady=10)
            except Exception as e:
                error_label = tk.Label(scrollable_frame, text=f"Error inesperado: {e}", bg="white", fg="red")
                error_label.pack(pady=10)

        # Simulación de movimiento del asistente hacia las noticias
        def simulate_assistant_fetching():
            current_x = self.root.winfo_x()
            target_x = self.screen_width - 200
            step = 10 if current_x < target_x else -10

            def move():
                nonlocal current_x
                if (step > 0 and current_x < target_x) or (step < 0 and current_x > target_x):
                    current_x += step
                    self.root.geometry(f"+{current_x}+{self.root.winfo_y()}")
                    self.root.after(50, move)
                else:
                    fetch_and_display_news()

            move()

        simulate_assistant_fetching()

    def show_weather(self):
        # Mostrar clima basado en ubicación
        weather_window = tk.Toplevel(self.root)
        weather_window.title("Clima")
        weather_window.geometry("300x300")
        weather_window.configure(bg="lightblue")

        try:
            # Obtener ubicación basada en IP
            location_response = requests.get("https://ipinfo.io/json")
            location_data = location_response.json()
            city = location_data.get("city", "Desconocida")

            # Obtener clima usando una API de clima
            api_key = "3198f2f2c663133af1230c450de9e269"  # Clave de API
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=es&appid={api_key}"
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json()

            if weather_response.status_code == 200:
                temp = weather_data["main"]["temp"]
                description = weather_data["weather"][0]["description"].capitalize()
                label = tk.Label(weather_window, text=f"Clima en {city}:", font=("Arial", 16, "bold"), bg="lightblue")
                label.pack(pady=10)
                temp_label = tk.Label(weather_window, text=f"{temp}°C, {description}", font=("Arial", 14), bg="lightblue")
                temp_label.pack(pady=10)

            else:
                error_label = tk.Label(weather_window, text="No se pudo obtener el clima.", bg="lightblue", fg="red")
                error_label.pack(pady=10)
        except Exception as e:
            error_label = tk.Label(weather_window, text=f"Error al obtener datos: {e}", bg="lightblue", fg="red")
            error_label.pack(pady=10)

    def play_hide_and_seek(self):
        print("Jugar a las escondidas...")

        # Elegir un punto aleatorio donde se esconderá
        hide_x = random.randint(50, self.screen_width - 150)
        hide_y = random.randint(50, self.screen_height - 150)

        # Mostrar el mensaje de cuenta regresiva y moverse al escondite
        self.show_transparent_countdown(5)

        def hide():
            # Mover al escondite y mostrar "trozos de tierra"
            self.hidden = True
            self.root.geometry(f"+{hide_x}+{hide_y}")
            self.canvas.itemconfig(self.character, fill="white")  # Hacer al personaje invisible
            self.animate_dirt_effect(hide_x, hide_y)

        self.root.after(5000, hide)

    def animate_dirt_effect(self, x, y):
        # Crear una animación de bloques de tierra que aparezcan continuamente hasta ser encontrado
        dirt_window = tk.Toplevel(self.root)
        dirt_window.geometry(f"100x100+{x}+{y}")
        dirt_window.overrideredirect(1)
        dirt_window.attributes('-topmost', True)
        dirt_window.attributes('-transparentcolor', 'white')  # Fondo transparente
        dirt_canvas = tk.Canvas(dirt_window, width=100, height=100, bg="white", highlightthickness=0)
        dirt_canvas.pack()

        # Animar bloques de tierra apareciendo
        def create_block():
            block = dirt_canvas.create_rectangle(
                random.randint(0, 90), random.randint(0, 90), random.randint(10, 100), random.randint(10, 100),
                fill="brown", outline="black"
            )
            dirt_canvas.after(300, lambda: dirt_canvas.delete(block))  # Eliminar el bloque después de un tiempo
            if self.hidden:
                dirt_canvas.after(500, create_block)  # Continuar creando bloques si no ha sido encontrado

        def found():
            self.hidden = False
            self.canvas.itemconfig(self.character, fill="blue")  # Hacer al personaje visible
            dirt_window.destroy()  # Eliminar el canvas de tierra
            self.move_character()  # Reanudar el movimiento
            print("¡Me encontraste!")

        dirt_canvas.bind("<Button-1>", lambda e: found())
        create_block()

    def show_transparent_countdown(self, seconds):
        # Crear una ventana completamente transparente
        countdown_window = tk.Toplevel(self.root)
        countdown_window.overrideredirect(1)
        countdown_window.attributes('-topmost', True)
        countdown_window.attributes('-transparentcolor', 'black')
        countdown_window.geometry(f"{self.screen_width}x{self.screen_height}+0+0")

        # Agregar el texto como cuenta regresiva
        countdown_label = tk.Label(countdown_window, text="", font=("Arial", 63), fg="red", bg="black")
        countdown_label.pack(expand=True)

        def update_countdown(remaining):
            if remaining > 0:
                countdown_label.config(text=f"Espérame {remaining} segundos")
                self.root.after(1000, update_countdown, remaining - 1)
            else:
                countdown_window.destroy()

        update_countdown(seconds)

    def close_assistant(self):
        # Cerrar la aplicación
        print("Cerrando asistente...")
        self.root.destroy()

# Inicializar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = Assistant(root)
    root.mainloop()
