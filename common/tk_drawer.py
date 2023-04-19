from math import pi
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
        self.mouse_start = None

        super().__init__()
        self.title("Изображение проекции полиэдра")
        self.geometry(f"{SIZE+5}x{SIZE+5}")

        self.bind('<Control-c>', quit)
        self.bind('<ButtonPress-1>', self._mouse_press)
        self.bind('<B1-Motion>', self._mouse_move)
        self.bind('<ButtonRelease-1>', self._mouse_release)

        self.canvas = tk.Canvas(width=SIZE, height=SIZE)
        self.canvas.pack(padx=5, pady=5)
        self.canvas.create_rectangle(0, 0, SIZE, SIZE, fill="white")

        self.update()
        self.resizable(False, False)

    def _mouse_press(self, e):
        self.mouse_start = R3(e.x, e.y, 0) * (1.5 / SIZE) - R3(1, 1, 0)
        self.last = R3(0, 0, 0)

    def _mouse_move(self, e):
        if self.mouse_start:
            new = R3(e.x, e.y, 0) * (1.5 / SIZE) - R3(1, 1, 0) - self.mouse_start
            for line in self.lines:
                line[1] = line[1].ry(new.x - self.last.x).rz(pi / 2).ry(new.y - self.last.y).rz(-pi / 2)
                line[2] = line[2].ry(new.x - self.last.x).rz(pi / 2).ry(new.y - self.last.y).rz(-pi / 2)
                self.canvas.coords(line[0], x(line[1]), y(line[1]), x(line[2]), y(line[2]))
            self.last = new

    def _mouse_release(self, e):
        self.mouse_start = None

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
