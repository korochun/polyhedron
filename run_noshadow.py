#!/usr/bin/env -S python3 -B
from sys import argv
from time import time
from common.tk_drawer import TkDrawer
from noshadow.polyedr import Polyedr


tk = TkDrawer()
try:
    for name in argv[1:]:
        print("=============================================================")
        print(f"Начало работы с полиэдром '{name}'")
        start_time = time()
        Polyedr(f"data/{name}.geom").draw(tk)
        delta_time = time() - start_time
        print(f"Изображение полиэдра '{name}' заняло {delta_time} сек.")
        input("Hit 'Return' to continue -> ")
except(EOFError, KeyboardInterrupt):
    print("\nStop")
    tk.close()
