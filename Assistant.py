import tkinter as tk
import random
import time
import pyautogui  
import requests  # Para obtener noticias desde una API
from threading import Timer  # Para manejar intervalos de tiempo

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
        self.dx = random.uniform(-5, 5)
        self.dy = random.uniform(-5, 5)
        self.following = False

        # Evento para clic en el personaje
        self.canvas.tag_bind(self.character, "<Button-1>", self.show_menu)

        # Movimiento inicial
        self.move_character()

        # Detección del mouse
        self.root.bind("<Motion>", self.detect_mouse)

        # Configurar probabilidad de capturar el mouse cada 30 minutos
        self.schedule_mouse_capture()

    def move_character(self):
        # Obtener posición actual de la ventana
        window_x = self.root.winfo_x()
        window_y = self.root.winfo_y()

        # Simular pausas aleatorias
        if random.random() < 0.01:  # Pausa breve ocasional
            self.root.after(500, self.move_character)
            return

        # Mover personaje dentro de la pantalla
        new_x = window_x + self.dx
        new_y = window_y + self.dy

        # Rebotar en los bordes de la pantalla
        if new_x <= 0 or new_x + 100 >= self.screen_width:
            self.dx = -self.dx + random.uniform(-1, 1)  # Cambio aleatorio de dirección
        if new_y <= 0 or new_y + 100 >= self.screen_height:
            self.dy = -self.dy + random.uniform(-1, 1)

        # Actualizar posición de la ventana
        self.root.geometry(f"+{int(new_x)}+{int(new_y)}")

        # Continuar movimiento si no está siguiendo el mouse
        if not self.following:
            self.root.after(30, self.move_character)

    def detect_mouse(self, event):
        if self.following:
            return

        mouse_x, mouse_y = pyautogui.position()
        char_x, char_y = self.get_center()
        distance = ((mouse_x - char_x) ** 2 + (mouse_y - char_y) ** 2) ** 0.5

        if distance < 200:  # Si el mouse está cerca
            self.follow_mouse(mouse_x, mouse_y)

    def follow_mouse(self, mouse_x, mouse_y):
        self.following = True
        start_time = time.time()

        def follow():
            nonlocal start_time
            elapsed = time.time() - start_time

            if elapsed > 10:  # Perseguir por 10 segundos
                self.following = False
                self.move_character()
                return

            char_x, char_y = self.get_center()
            dx = (mouse_x - char_x) / 15 + random.uniform(-1, 1)
            dy = (mouse_y - char_y) / 15 + random.uniform(-1, 1)

            new_x = self.root.winfo_x() + dx
            new_y = self.root.winfo_y() + dy

            self.root.geometry(f"+{int(new_x)}+{int(new_y)}")
            self.root.after(30, follow)

        follow()

    def get_center(self):
        window_x = self.root.winfo_x()
        window_y = self.root.winfo_y()
        return window_x + 50, window_y + 50  # Centro del personaje

    def show_menu(self, event):
        # Mostrar un menú con opciones
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Noticias", command=self.show_news_interface)
        menu.add_command(label="Jugar a las escondidas", command=self.play_hide_and_seek)
        menu.add_command(label="Cerrar", command=self.close_assistant)
        menu.post(event.x_root, event.y_root)

    def show_news_interface(self):
        # Crear una nueva ventana para mostrar las noticias
        news_window = tk.Toplevel(self.root)
        news_window.title("Noticias")
        news_window.geometry("400x600")

        # Marco para las noticias
        frame = tk.Frame(news_window, bg="white")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Etiqueta de título
        title = tk.Label(frame, text="Últimas Noticias", font=("Arial", 16), bg="white")
        title.pack(pady=10)

        # Obtener noticias desde la API
        try:
            api_key = "6c8be6de99d6477e872492194efd7d14"  
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
            response = requests.get(url)
            news = response.json()

            # Mostrar las primeras noticias
            for article in news['articles'][:10]:
                headline = tk.Label(frame, text=f"- {article['title']}", wraplength=350, justify=tk.LEFT, bg="white")
                headline.pack(anchor="w", pady=5)
        except Exception as e:
            error_label = tk.Label(frame, text=f"Error al obtener noticias: {e}", bg="white", fg="red")
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
            self.root.geometry(f"+{hide_x}+{hide_y}")
            self.canvas.itemconfig(self.character, fill="white")  # Hacer al personaje invisible
            self.show_dirt_pieces(hide_x, hide_y)

        self.root.after(5000, hide)

    def show_dirt_pieces(self, x, y):
        # Crear trozos de tierra para indicar el escondite
        dirt_window = tk.Toplevel(self.root)
        dirt_window.geometry(f"100x50+{x}+{y}")
        dirt_window.overrideredirect(1)
        dirt_window.attributes('-topmost', True)

        dirt_label = tk.Label(dirt_window, text="Trozos de tierra", font=("Arial", 12), bg="brown", fg="white")
        dirt_label.pack(expand=True)

        # Permitir que el usuario haga clic para revelar al personaje
        def found():
            self.canvas.itemconfig(self.character, fill="blue")  # Hacer al personaje visible
            dirt_window.destroy()
            print("¡Me encontraste!")

        dirt_window.bind("<Button-1>", lambda e: found())

    def show_transparent_countdown(self, seconds):
        # Crear una ventana completamente transparente
        countdown_window = tk.Toplevel(self.root)
        countdown_window.overrideredirect(1)
        countdown_window.attributes('-topmost', True)
        countdown_window.attributes('-transparentcolor', 'black')
        countdown_window.geometry(f"{self.screen_width}x{self.screen_height}+0+0")

        # Agregar el texto como cuenta regresiva
        countdown_label = tk.Label(countdown_window, text="", font=("Arial", 48), fg="red", bg="black")
        countdown_label.pack(expand=True)

        def update_countdown(remaining):
            if remaining > 0:
                countdown_label.config(text=f"Espérame {remaining} segundos")
                self.root.after(1000, update_countdown, remaining - 1)
            else:
                countdown_window.destroy()

        update_countdown(seconds)

    def schedule_mouse_capture(self):
        # Programar el intento de capturar el mouse cada 30 minutos
        def attempt_capture():
            if random.random() < 0.5:  # 50% de probabilidad
                self.capture_mouse()
            self.root.after(30 * 60 * 1000, attempt_capture)  # Reprogramar

        attempt_capture()

    def capture_mouse(self):
        print("¡Capturando el mouse por 10 segundos!")
        start_time = time.time()

        def move_mouse_randomly():
            elapsed = time.time() - start_time
            if elapsed > 10:  # Liberar el mouse después de 10 segundos
                print("Mouse liberado.")
                return

            # Mover el mouse a una posición aleatoria cercana
            current_x, current_y = pyautogui.position()
            new_x = current_x + random.randint(-100, 100)
            new_y = current_y + random.randint(-100, 100)

            # Asegurarse de que esté dentro de la pantalla
            new_x = max(0, min(self.screen_width, new_x))
            new_y = max(0, min(self.screen_height, new_y))

            pyautogui.moveTo(new_x, new_y, duration=0.1)
            self.root.after(100, move_mouse_randomly)

        move_mouse_randomly()

    def close_assistant(self):
        # Cerrar la aplicación
        print("Cerrando asistente...")
        self.root.destroy()

# Inicializar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = Assistant(root)
    root.mainloop()
