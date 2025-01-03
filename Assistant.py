import tkinter as tk
import random
import time

class Assistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Asistente Personal")

        # Hacer la ventana flotante y sin bordes
        self.root.overrideredirect(1)  # Sin bordes
        self.root.attributes('-topmost', True)  # Siempre encima
        
        # Obtener dimensiones de la pantalla
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Configuración del canvas para cubrir toda la pantalla
        self.canvas = tk.Canvas(self.root, width=100, height=100, bg="white", highlightthickness=0)
        self.canvas.pack()

        # Crear personaje
        self.character = self.canvas.create_oval(10, 10, 90, 90, fill="blue", outline="black")

        # Variables de movimiento
        self.dx = random.choice([-2, 2])
        self.dy = random.choice([-2, 2])
        self.following = False

        # Evento para clic en el personaje
        self.canvas.tag_bind(self.character, "<Button-1>", self.show_menu)

        # Movimiento inicial
        self.move_character()

        # Detección del mouse
        self.root.bind("<Motion>", self.detect_mouse)

        # Permitir arrastrar la ventana
        self.root.bind("<B1-Motion>", self.drag_window)

    def drag_window(self, event):
        # Mover la ventana cuando se arrastra con el botón izquierdo del mouse
        x = self.root.winfo_pointerx() - 50  # Ajustar posición centrada
        y = self.root.winfo_pointery() - 50
        self.root.geometry(f"+{x}+{y}")

    def move_character(self):
        # Movimiento básico del personaje
        self.canvas.move(self.character, self.dx, self.dy)
        x1, y1, x2, y2 = self.canvas.coords(self.character)

        # Rebotar en los bordes de la pantalla
        if x1 + self.root.winfo_x() <= 0 or x2 + self.root.winfo_x() >= self.screen_width:
            self.dx = -self.dx
        if y1 + self.root.winfo_y() <= 0 or y2 + self.root.winfo_y() >= self.screen_height:
            self.dy = -self.dy

        # Actualizar movimiento
        if not self.following:
            self.root.after(50, self.move_character)

    def detect_mouse(self, event):
        if self.following:
            return

        mouse_x = self.root.winfo_pointerx()
        mouse_y = self.root.winfo_pointery()
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
            self.canvas.move(self.character, dx, dy)
            self.root.after(50, follow)

        follow()

    def get_center(self):
        x1, y1, x2, y2 = self.canvas.coords(self.character)
        abs_x = self.root.winfo_x() + (x1 + x2) / 2
        abs_y = self.root.winfo_y() + (y1 + y2) / 2
        return abs_x, abs_y

    def show_menu(self, event):
        # Mostrar un menú con opciones
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Noticias", command=self.show_news)
        menu.add_command(label="Jugar a las escondidas", command=self.play_hide_and_seek)
        menu.post(event.x_root, event.y_root)

    def show_news(self):
        # Placeholder para noticias
        print("Mostrar noticias...")

    def play_hide_and_seek(self):
        # Placeholder para el juego de las escondidas
        print("Jugar a las escondidas...")

# Inicializar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = Assistant(root)
    root.mainloop()
