import win32gui, win32con, win32api
import random, time, math, msvcrt
from multiprocessing import Process, Manager
import threading
import winsound

DUR = 20
TOTAL_PARTES = 18

def minimizar_ventanas():
    
    def enum_handler(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    
    win32gui.EnumWindows(enum_handler, None)

if __name__ == "__main__":
    minimizar_ventanas()

def reproducir_musica(parte):
    nombre = f"{parte}.wav"  
    def play_sound():
        try:
            winsound.PlaySound(nombre, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except:
            pass
    threading.Thread(target=play_sound, daemon=True).start()

def mouse_temblor(w, h, pos):
    x_mouse, y_mouse = pos
    while True:
        x_mouse += random.randint(-50, 50)
        y_mouse += random.randint(-50, 50)
        x_mouse = max(0, min(w-1, x_mouse))
        y_mouse = max(0, min(h-1, y_mouse))
        pos[0] = x_mouse
        pos[1] = y_mouse
        win32api.SetCursorPos((x_mouse, y_mouse))
        time.sleep(0.02)

def iconos_en_pantalla(pos):
    dc = win32gui.GetDC(0)
    iconos = [
        win32gui.LoadIcon(0, win32con.IDI_ERROR),
        win32gui.LoadIcon(0, win32con.IDI_WARNING),
        win32gui.LoadIcon(0, win32con.IDI_INFORMATION)
    ]
    while True:
        x_mouse, y_mouse = pos
        for _ in range(5):
            icono = random.choice(iconos)
            x = x_mouse + random.randint(-50, 50)
            y = y_mouse + random.randint(-50, 50)
            win32gui.DrawIcon(dc, x, y, icono)
        time.sleep(0.05)

def dispersar_pixeles_proceso(w, h):
    dc = win32gui.GetDC(0)
    mem_dc = win32gui.CreateCompatibleDC(dc)
    bmp = win32gui.CreateCompatibleBitmap(dc, w, h)
    win32gui.SelectObject(mem_dc, bmp)
    while True:
        win32gui.BitBlt(mem_dc, 0, 0, w, h, dc, 0, 0, win32con.SRCCOPY)
        for _ in range(5000):
            bx = random.randint(0, w - 10)
            by = random.randint(0, h - 10)
            dx = bx + random.randint(-50, 50)
            dy = by + random.randint(-50, 50)
            dx = max(0, min(w - 10, dx))
            dy = max(0, min(h - 10, dy))
            win32gui.BitBlt(mem_dc, dx, dy, 10, 10, mem_dc, bx, by, win32con.SRCCOPY)
        win32gui.BitBlt(dc, 0, 0, w, h, mem_dc, 0, 0, win32con.SRCCOPY)
        time.sleep(0.1)

def tunel(dc, w, h, cx, cy, f):
    size = int(100 + f % 200)
    for i in range(0, w, size):
        for j in range(0, h, size):
            dx = int((i - cx) * 0.9 + cx)
            dy = int((j - cy) * 0.9 + cy)
            win32gui.BitBlt(dc, dx, dy, size, size, dc, i, j, win32con.SRCCOPY)

def lineas(dc, w, h):
    pen = win32gui.CreatePen(0, 2, win32api.RGB(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
    win32gui.SelectObject(dc, pen)
    win32gui.MoveToEx(dc, random.randint(0,w), random.randint(0,h))
    win32gui.LineTo(dc, random.randint(0,w), random.randint(0,h))
    win32gui.DeleteObject(pen)

def distorsion(dc, w, h, f):
    for y in range(0,h,20):
        off = int(math.sin(f/5 + y/30) * 20)
        win32gui.BitBlt(dc, off, y, w, 20, dc, 0, y, win32con.SRCCOPY)

def remolino(dc, w, h, cx, cy, f):
    ang = (f % 360) * math.pi / 180
    for y in range(0, h, 30):
        for x in range(0, w, 30):
            dx = int(cx + (x - cx) * math.cos(ang) - (y - cy) * math.sin(ang))
            dy = int(cy + (x - cx) * math.sin(ang) + (y - cy) * math.cos(ang))
            win32gui.BitBlt(dc, dx, dy, 30, 30, dc, x, y, win32con.SRCCOPY)

def caos_pixeles(dc, w, h):
    for _ in range(1000):
        tam = random.randint(2, 20)
        sx = random.randint(0, w - tam)
        sy = random.randint(0, h - tam)
        dx = sx + random.randint(-40, 40)
        dy = sy + random.randint(-40, 40)
        dx = max(0, min(w - tam, dx))
        dy = max(0, min(h - tam, dy))
        win32gui.BitBlt(dc, dx, dy, tam, tam, dc, sx, sy, win32con.SRCCOPY)

def mover_derecha(dc, w, h, vel=2):
    win32gui.BitBlt(dc, vel, 0, w - vel, h, dc, 0, 0, win32con.SRCCOPY)

def estirar(dc, w, h, f):
    for y in range(0, h, 10):
        fact = 1 + 0.5 * math.sin(f / 5 + y / 50)
        ancho2 = int(w * fact)
        dx = int((w - ancho2) / 2)
        win32gui.StretchBlt(dc, dx, y, ancho2, 10, dc, 0, y, w, 10, win32con.SRCCOPY)

def arcoiris(dc, w, h, f):
    r = int((math.sin(f/10)+1)*127)
    g = int((math.sin(f/13+2)+1)*127)
    b = int((math.sin(f/17+4)+1)*127)
    brush = win32gui.CreateSolidBrush(win32api.RGB(r, g, b))
    old = win32gui.SelectObject(dc, brush)
    win32gui.PatBlt(dc, 0, 0, w, h, win32con.PATINVERT)
    win32gui.SelectObject(dc, old)
    win32gui.DeleteObject(brush)

def arcoiris_explosivo(dc, w, h, f):
    arcoiris(dc, w, h, f)
    for _ in range(10):
        s = random.randint(50, 200)
        x = random.randint(0, w - s)
        y = random.randint(0, h - s)
        brush = win32gui.CreateSolidBrush(win32api.RGB(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        old = win32gui.SelectObject(dc, brush)
        win32gui.PatBlt(dc, x, y, s, s, win32con.PATINVERT)
        win32gui.SelectObject(dc, old)
        win32gui.DeleteObject(brush)

def figuras(dc, w, h):
    for _ in range(5):
        pen = win32gui.CreatePen(0, 3, win32api.RGB(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        brush = win32gui.CreateSolidBrush(win32api.RGB(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        win32gui.SelectObject(dc, pen)
        win32gui.SelectObject(dc, brush)
        puntos = [(random.randint(0, w), random.randint(0, h)) for _ in range(random.randint(5, 10))]
        win32gui.Polygon(dc, puntos)
        win32gui.DeleteObject(pen)
        win32gui.DeleteObject(brush)

def neon(dc, w, h, f):
    r = int((math.sin(f/5)+1)*127+128)
    g = int((math.sin(f/7)+1)*127+128)
    b = int((math.sin(f/9)+1)*127+128)
    brush = win32gui.CreateSolidBrush(win32api.RGB(r, g, b))
    old = win32gui.SelectObject(dc, brush)
    win32gui.PatBlt(dc, 0, 0, w, h, win32con.PATINVERT)
    win32gui.SelectObject(dc, old)
    win32gui.DeleteObject(brush)
    win32gui.BitBlt(dc, random.randint(-5, 5), random.randint(-5, 5), w, h, dc, 0, 0, win32con.SRCCOPY)

def saturado(dc, w, h, f):
    r = min(255, int(abs(math.sin(f/4))*300))
    g = min(255, int(abs(math.sin(f/5))*300))
    b = min(255, int(abs(math.sin(f/6))*300))
    brush = win32gui.CreateSolidBrush(win32api.RGB(r, g, b))
    old = win32gui.SelectObject(dc, brush)
    win32gui.PatBlt(dc, 0, 0, w, h, win32con.PATINVERT)
    win32gui.SelectObject(dc, old)
    win32gui.DeleteObject(brush)

def epileptico(dc, w, h):
    color = win32api.RGB(random.randint(200,255), random.randint(200,255), random.randint(200,255))
    brush = win32gui.CreateSolidBrush(color)
    old = win32gui.SelectObject(dc, brush)
    win32gui.PatBlt(dc, 0, 0, w, h, win32con.PATINVERT)
    win32gui.SelectObject(dc, old)
    win32gui.DeleteObject(brush)

def baja_calidad(dc, w, h):
    for _ in range(500):
        x = random.randint(0, w - 10)
        y = random.randint(0, h - 10)
        win32gui.BitBlt(dc, x, y, 10, 10, dc, x, y, win32con.DSTINVERT)

def parte_18(dc, w, h, f):
    saturado(dc, w, h, f)
    angle = int((f % 360))
    text = f"Windows version {random.choice(['XP','7','10','11'])}"
    win32gui.DrawText(dc, text, -1, (w//2-100,h//2,w,h), win32con.DT_CENTER)
    win32gui.BitBlt(dc, int(math.sin(f/10)*10), int(math.cos(f/10)*10), w, h, dc, 0, 0, win32con.SRCCOPY)

def ejecutar_parte(parte, dc, w, h, cx, cy, f):
    if parte == 1: tunel(dc, w, h, cx, cy, f)
    elif parte == 2: lineas(dc, w, h)
    elif parte == 3: distorsion(dc, w, h, f)
    elif parte == 4: remolino(dc, w, h, cx, cy, f)
    elif parte == 5: caos_pixeles(dc, w, h)
    elif parte == 6: mover_derecha(dc, w, h, vel=4)
    elif parte == 7: estirar(dc, w, h, f)
    elif parte == 8: arcoiris(dc, w, h, f)
    elif parte == 9: arcoiris_explosivo(dc, w, h, f)
    elif parte == 10: figuras(dc, w, h)
    elif parte == 11: neon(dc, w, h, f)
    elif parte == 12: figuras(dc, w, h); saturado(dc, w, h, f)
    elif parte == 13: mover_derecha(dc, w, h, vel=2); epileptico(dc, w, h)
    elif parte == 14: epileptico(dc, w, h); figuras(dc, w, h); win32gui.BitBlt(dc, random.randint(-10,10), random.randint(-10,10), w, h, dc, 0, 0, win32con.SRCCOPY)
    elif parte == 15: baja_calidad(dc, w, h)
    elif parte == 16: saturado(dc, w, h, f); win32gui.BitBlt(dc, random.randint(-5,5), random.randint(-5,5), w, h, dc, 0, 0, win32con.SRCCOPY)
    elif parte == 17: pass
    elif parte == 18: parte_18(dc, w, h, f)

if __name__ == "__main__":
    w = win32api.GetSystemMetrics(0)
    h = win32api.GetSystemMetrics(1)
    cx, cy = w//2, h//2
    dc = win32gui.GetDC(0)

    manager = Manager()
    mouse_pos = manager.list([cx, cy])

    mouse_proc = Process(target=mouse_temblor, args=(w,h,mouse_pos))
    iconos_proc = Process(target=iconos_en_pantalla, args=(dc, mouse_pos))
    mouse_proc.start()
    iconos_proc.start()

    parte_anterior = 0
    pixel_proc = None
    start_time = time.time()
    frame = 0

    while True:
        if msvcrt.kbhit() and ord(msvcrt.getch())==27: break
        elapsed = time.time() - start_time
        parte = int(elapsed // DUR) + 1
        frame += 1
        if parte > TOTAL_PARTES: parte = TOTAL_PARTES
        if parte != parte_anterior:
            reproducir_musica(parte)
            parte_anterior = parte
            if parte == 17:
                if pixel_proc is None or not pixel_proc.is_alive():
                    pixel_proc = Process(target=dispersar_pixeles_proceso, args=(w,h))
                    pixel_proc.start()
        ejecutar_parte(parte, dc, w, h, cx, cy, frame)
        time.sleep(0.01)

    mouse_proc.terminate()
    iconos_proc.terminate()
    if pixel_proc: pixel_proc.terminate()
