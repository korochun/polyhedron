import tkinter as tk
from common.r3 import R3

# Размер окна
SIZE = 900
# Коэффициент гомотетии
SCALE = 1.5


def x(p):
    """ преобразование x-координаты """
    return SIZE / 2 + SCALE * p.x


def y(p):
    """" преобразование y-координаты """
    return SIZE / 2 - SCALE * p.y


class TkDrawer(tk.Tk):
    """ Графический интерфейс """

    # Конструктор
    def __init__(self):
        self.lines = []

        super().__init__()
        self.title("Изображение проекции полиэдра")
        self.geometry(f"{SIZE+5}x{SIZE+5}")

        self.bind('<Control-c>', quit)

        self.canvas = tk.Canvas(width=SIZE, height=SIZE)
        self.canvas.pack(padx=5, pady=5)
        self.canvas.create_rectangle(0, 0, SIZE, SIZE, fill="white")

        self.update()
        self.resizable(False, False)

    # Стирание существующей картинки
    def clean(self):
        for line in self.lines:
            self.canvas.delete(line[0])
        self.update()

    close = tk.Tk.quit

    # Рисование линии
    def draw_line(self, p, q):
        self.lines.append([
            self.canvas.create_line(x(p), y(p), x(q), y(q),
                                    fill="black", width=3),
            p, q,
        ])


if __name__ == "__main__":
    import time
    from r3 import R3
    tk = TkDrawer()
    tk.clean()
    tk.draw_line(R3(0.0, 0.0, 0.0), R3(100.0, 100.0, 0.0))
    tk.draw_line(R3(0.0, 0.0, 0.0), R3(0.0, 100.0, 0.0))
    time.sleep(5)
