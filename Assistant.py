import tkinter as tk
import random
import time
import pyautogui  
import requests  

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
        self.dx = random.choice([-5, 5])
        self.dy = random.choice([-5, 5])
        self.following = False

        # Evento para clic en el personaje
        self.canvas.tag_bind(self.character, "<Button-1>", self.show_menu)

        # Movimiento inicial
        self.move_character()

        # Detección del mouse
        self.root.bind("<Motion>", self.detect_mouse)

    def move_character(self):
        # Obtener posición actual de la ventana
        window_x = self.root.winfo_x()
        window_y = self.root.winfo_y()

        # Mover personaje dentro de la pantalla
        new_x = window_x + self.dx
        new_y = window_y + self.dy

        # Rebotar en los bordes de la pantalla
        if new_x <= 0 or new_x + 100 >= self.screen_width:
            self.dx = -self.dx
        if new_y <= 0 or new_y + 100 >= self.screen_height:
            self.dy = -self.dy

        # Actualizar posición de la ventana
        self.root.geometry(f"+{new_x}+{new_y}")

        # Continuar movimiento si no está siguiendo el mouse
        if not self.following:
            self.root.after(30, self.move_character)

    def detect_mouse(self, event):
        if self.following:
            return

        mouse_x, mouse_y = pyautogui.position()
        char_x, char_y = self.get_center()
        distance = ((mouse_x - char_x) ** 2 + (mouse_y - char_y) ** 2) ** 0.5

        if distance < 150:  # Si el mouse está cerca
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
            dx = (mouse_x - char_x) / 20
            dy = (mouse_y - char_y) / 20
            self.root.geometry(f"+{int(self.root.winfo_x() + dx)}+{int(self.root.winfo_y() + dy)}")
            self.root.after(30, follow)

        follow()

    def get_center(self):
        window_x = self.root.winfo_x()
        window_y = self.root.winfo_y()
        return window_x + 50, window_y + 50  # Centro del personaje

    def show_menu(self, event):
        # Mostrar un menú con opciones
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Noticias", command=self.show_news)
        menu.add_command(label="Jugar a las escondidas", command=self.play_hide_and_seek)
        menu.post(event.x_root, event.y_root)

    def show_news(self):
        try:
            # Obtener noticias desde una API
            api_key = ""  
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
            response = requests.get(url)
            news = response.json()

            # Mostrar las primeras noticias
            headlines = [article['title'] for article in news['articles'][:5]]
            news_text = "\n".join(headlines)
            print("Noticias recientes:\n", news_text)
        except Exception as e:
            print("Error al obtener noticias:", e)

    def play_hide_and_seek(self):
        # Animación de esconderse
        print("Jugar a las escondidas...")
        self.canvas.itemconfig(self.character, fill="white")  # Cambiar a invisible

        # Señal visual donde se esconde
        x1, y1, x2, y2 = self.canvas.coords(self.character)
        signal = self.canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, outline="red", width=2)

        def reappear():
            self.canvas.itemconfig(self.character, fill="blue")  # Volver a visible
            self.canvas.delete(signal)

        self.root.after(5000, reappear)  # Reaparecer después de 5 segundos

# Inicializar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = Assistant(root)
    root.mainloop()
