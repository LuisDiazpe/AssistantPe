import tkinter as tk
import random
import time

class Assistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Asistente Personal")
        self.root.geometry("800x600")
        
        # Configuración del canvas
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack()
        
        # Crear personaje
        self.character = self.canvas.create_oval(50, 50, 100, 100, fill="blue", outline="black")
        
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

    def move_character(self):
        # Movimiento básico del personaje
        self.canvas.move(self.character, self.dx, self.dy)
        x1, y1, x2, y2 = self.canvas.coords(self.character)
        
        # Rebotar en los bordes
        if x1 <= 0 or x2 >= 800:
            self.dx = -self.dx
        if y1 <= 0 or y2 >= 600:
            self.dy = -self.dy
        
        # Actualizar movimiento
        if not self.following:
            self.root.after(50, self.move_character)

    def detect_mouse(self, event):
        if self.following:
            return
        
        mouse_x, mouse_y = event.x, event.y
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
        return (x1 + x2) / 2, (y1 + y2) / 2

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
