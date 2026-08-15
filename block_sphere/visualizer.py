import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import numpy as np
import sys
import os
import colorsys
import qutip as qt
from matplotlib.backend_bases import MouseButton
from matplotlib.animation import FuncAnimation
import threading



#visuelle Einstellungen
matplotlib.rcParams['toolbar'] = 'None'
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['figure.dpi'] = 150
matplotlib.rcParams['lines.antialiased'] = True
matplotlib.rcParams['patch.antialiased'] = True

#Farben definieren
BG_COLOR = '#0b0e14'
SPHERE_COLOR = '#6366f1'
GRID_COLOR = '#4b5568'
AXIS_COLOR = '#8b93a7'
LABEL_COLOR = '#e6e9f0'
TITLE_COLOR = '#818cf8'
ROT_AXIS_COLOR = '#f472b6'

#Definiere Standardbasen |0⟩ und |1⟩
ket_0 = qt.Qobj([1, 0])
ket_1 = qt.Qobj([0, 1])

#speichert alle Vektoren, die angezeigt werden
vector_list = []


#Klasse Vektor speichert Daten für anzuzeigende Vektoren
class vector:
    def __init__(self, x, y, z, a, b, c, color=None):
        self.x = x
        self.y = y
        self.z = z
        self.a = a
        self.b = b
        self.c = c
        self.color = color if color is not None else colorsys.hsv_to_rgb(np.random.rand(), 0.65, 0.98)

    def plot(self, color=None):
        c = color if color is not None else self.color
        ax.quiver(self.x, self.y, self.z, self.a, self.b, self.c,
                  color=c, linewidth=2.6, arrow_length_ratio=0.14,
                  antialiased=True, capstyle='round')


#malt einmal alle Vektoren in list_of_vectors in die Bloch-Kugel
def update(list_of_vectors, rotationsachse = None):
    ax.cla()
    if not rotationsachse is None:
        v = vector_from_state(rotationsachse)

        ax.plot([-1.1*v.a, 1.1*v.a], [-1.1*v.b, 1.1*v.b], [-1.1*v.c, 1.1*v.c],
                color=ROT_AXIS_COLOR, linewidth=1.8, linestyle='--', alpha=0.85)
    for i in list_of_vectors:
        i.plot()

    draw_axis()
    plt.draw()


#User Input
#x: löscht alle Vektoren
#y: wendet momentane Matrix auf alle Vektoren an
#k: spawnt einen zufälligen Vektoren

def on_press(event):
    sys.stdout.flush()
    if event.key == 'y':
        apply_matrix(matrix)

    elif event.key == 'x':
        global vector_list
        vector_list = []
        update(vector_list)
    elif event.key == 'k':
        for i in range(1): vector_list.append(vector_from_state(((np.random.randint(-100, 100)+(np.random.randint(-100, 100)*1j))*ket_0 + (np.random.randint(-100, 100)+(np.random.randint(-100, 100)*1j))*ket_1).unit()))
        update(vector_list)


#wendet die Matrix matrix auf alle Vektoren in vector_list an und animiert ihre Rotation auf der Sphäre

def apply_matrix(matrix):
    eigenwerte, eigenzustaende = matrix.eigenstates()
    rotationsachse = eigenzustaende[0]
    
    global anim
    starts = [np.array([v.a, v.b, v.c]).flatten() for v in vector_list]
    ends = []
    for v in vector_list:
        vector_neu = vector_from_state(matrix * state_from_vector(v))
        ends.append(np.array([vector_neu.a, vector_neu.b, vector_neu.c]).flatten())

    fps = 30

    gesamt_winkel = np.angle(eigenwerte[1]) - np.angle(eigenwerte[0])
    def frame_update(frame):
        t = frame / (fps - 1)

        achsen_state = vector_from_state(rotationsachse)
        achsen_vec = np.array([achsen_state.a, achsen_state.b, achsen_state.c])
        current = [vector(0, 0, 0, *rotiere(s, achsen_vec, t * gesamt_winkel), color=orig.color) for s, orig in zip(starts, vector_list)]
        achse = rotationsachse if frame < fps - 1 else None
        update(current, achse)
        return ()
    anim = FuncAnimation(
        fig, frame_update, frames=fps,
        interval=1000/30, blit=False, repeat=False
    )
    fig.canvas.draw_idle()

    for i, v in enumerate(vector_list):
        vector_list[i] = vector_from_state(matrix * state_from_vector(v))
        vector_list[i].color = v.color

#Namen dieser Funktionen sind selbsterklärend (benötigt für Rest des Programms)
def angles_from_state(alpha, beta):
    theta = 2*np.arccos(np.abs(alpha))
    phi = (np.arctan2(beta.imag, beta.real)-np.arctan2(alpha.imag, alpha.real))

    return theta, phi

def state_from_vector(vector):
    x, y, z = vector.a.item(), vector.b.item(), vector.c.item()
    theta = np.arccos(z)
    phi = np.arctan2(y, x)
    alpha = complex(np.cos(theta/2))
    beta = complex(np.exp(1j*phi) * np.sin(theta/2))
    return alpha * ket_0 + beta * ket_1

def vector_from_angle(theta, phi):
    px = np.sin(theta) * np.cos(phi)
    py = np.sin(theta) * np.sin(phi)
    pz = np.cos(theta)
    return vector(0, 0, 0, px, py, pz)

def vector_from_state(state):
    alpha = state.full()[0].item()
    beta = state.full()[1].item()
    theta, phi = angles_from_state(alpha, beta)
    return vector_from_angle(theta, phi)

#rechnet für die Animation der Vektoren ihren Weg auf der Bloch-Kugel aus mithilfe von Start- und Endpunkt und der Rotationsachse
def rotiere(v, achse, theta):
    achse = achse / np.linalg.norm(achse)
    return (v * np.cos(theta)
            + np.cross(achse, v) * np.sin(theta)
            + achse * np.dot(achse, v) * (1 - np.cos(theta)))

#Malt den Hintergrund und die Achsen 
def draw_axis():
    #alle axen einstellungen
    ax.plot_surface(x, y, z, color=SPHERE_COLOR, alpha=0.10, linewidth=0,
                     shade=True, antialiased=True, zorder=0)
    ax.plot_wireframe(x, y, z, color=GRID_COLOR, alpha=0.35, linewidth=0.3, antialiased=True)
    ax.set_box_aspect([1,1,1])

    ax.grid(False)

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('none')
    ax.yaxis.pane.set_edgecolor('none')
    ax.zaxis.pane.set_edgecolor('none')

    lim = 1.2
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)

    # Äquator und Meridiane als dezente Referenzkreise
    ring = np.linspace(0, 2 * np.pi, 150)
    ax.plot(np.cos(ring), np.sin(ring), 0, color=GRID_COLOR, lw=1.0, alpha=0.65, antialiased=True)
    ax.plot(np.cos(ring), np.zeros_like(ring), np.sin(ring), color=GRID_COLOR, lw=1.0, alpha=0.65, antialiased=True)
    ax.plot(np.zeros_like(ring), np.cos(ring), np.sin(ring), color=GRID_COLOR, lw=1.0, alpha=0.65, antialiased=True)

    ax.plot([-lim, lim], [0, 0], [0, 0], color=AXIS_COLOR, lw=1.1, alpha=0.6, antialiased=True)
    ax.plot([0, 0], [-lim, lim], [0, 0], color=AXIS_COLOR, lw=1.1, alpha=0.6, antialiased=True)
    ax.plot([0, 0], [0, 0], [-lim, lim], color=AXIS_COLOR, lw=1.1, alpha=0.6, antialiased=True)

    ax.set_axis_off()

    label_kwargs = dict(fontsize=15, fontweight='bold', color=LABEL_COLOR, ha='center', va='center')
    ax.text(0, 0, 1.15, "|0⟩", **label_kwargs)
    ax.text(0, 0, -1.15, "|1⟩", **label_kwargs)
    ax.text(0, 1.15, 0, "|i⟩", **label_kwargs)
    ax.text(0, -1.15, 0, "|-i⟩", **label_kwargs)
    ax.text(1.15, 0, 0, "|+⟩", **label_kwargs)
    ax.text(-1.15, 0, 0, "|-⟩", **label_kwargs)

#Erstellt fig für die Bloch-Kugel und zeichne alles
fig = plt.figure(figsize=(7, 7), dpi=150, facecolor=BG_COLOR)
fig.canvas.manager.set_window_title('Bloch-Kugel')
ax = fig.add_axes([0, 0, 1, 0.94], projection='3d')
ax.set_facecolor(BG_COLOR)
ax.view_init(elev=20, azim=35)
fig.suptitle('Bloch-Kugel', fontsize=13, fontweight='bold', color=TITLE_COLOR, y=0.98)
u = np.linspace(0, 2 * np.pi, 90)
v = np.linspace(0, np.pi, 90)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones_like(u), np.cos(v))

#startet den listener für Tastendrücke
fig.canvas.mpl_connect('key_press_event', on_press)

#Hermit'sche Matrix als Standard (kann verändert werden)
matrix = qt.Qobj([[1/np.sqrt(2), 1/np.sqrt(2)], [1/np.sqrt(2), -1/np.sqrt(2)]])

#malt einmal alle Vektoren 
update(vector_list)

#parallel zu Tastendrücken kann im Terminal interaktiv das Programm gesteuert werden (selbsterklärend)
def input_loop():
    while True:
        global vector_list
        global matrix
        text = input("0 = neuer Vektor, 1 = Neue Matrix, 2 = Vektoren löschen, q = Beenden: ")
        if text == "q":
            os._exit(0)
        try:
            if text == "0":
                text = input("Neuer Vektor (a+bj): ")
                alpha, beta = text.split(" ")
                vector_list.append(vector_from_state((complex(alpha)*ket_0 + complex(beta)*ket_1).unit()))
                update(list)

            elif text == "1":
                text = input("Neue Matrix (a+bj a+bj a+bj a+bj): ")
                werte = text.split(" ")
                for i in range(len(werte)):
                    werte[i] = eval(werte[i])
                matrix = qt.Qobj([[werte[0], werte[1]], [werte[2], werte[3]]])

            elif text == "2":
                vector_list = []
                update(list)
        except ValueError:
            print("Ungültig.")

#paralleler Thread für Terminaleingabe
threading.Thread(target=input_loop, daemon=True).start()
manager = plt.get_current_fig_manager()

#malt alles und startet loops
plt.show()



#Geschrieben von DukeThias mit mathematischer Hilfe von Wurmloch08
