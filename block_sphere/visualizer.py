import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import numpy as np
import sys
import os
import qutip as qt
from matplotlib.backend_bases import MouseButton
from matplotlib.animation import FuncAnimation
import threading

matplotlib.rcParams['toolbar'] = 'None'

ket_0 = qt.Qobj([1, 0])
ket_1 = qt.Qobj([0, 1])

list = []

class vector:
    def __init__(self, x, y, z, a, b, c, color=None):
        self.x = x
        self.y = y
        self.z = z
        self.a = a
        self.b = b
        self.c = c
        self.color = color if color is not None else np.random.rand(3)

    def plot(self, color=None):
        c = color if color is not None else self.color
        ax.quiver(self.x, self.y, self.z, self.a, self.b, self.c, color=c)

def update(list_of_vectors, rotationsachse = None):
    ax.cla()
    if not rotationsachse is None:
        v = vector_from_state(rotationsachse)

        ax.plot([-10*v.a, 10*v.a], [-10*v.b, 10*v.b], [-10*v.c, 10*v.c], color='r', linewidth=2.0)
    for i in list_of_vectors:
        i.plot()

    draw_axis()
    plt.draw()

def on_press(event):
    sys.stdout.flush()
    if event.key == 'y':
        apply_matrix(matrix)

    elif event.key == 'x':
        global list
        list = []
        update(list)
    elif event.key == 'k':
        for i in range(1): list.append(vector_from_state(((np.random.randint(-100, 100)+(np.random.randint(-100, 100)*1j))*ket_0 + (np.random.randint(-100, 100)+(np.random.randint(-100, 100)*1j))*ket_1).unit()))
        update(list)

def apply_matrix(matrix):
    eigenwerte, eigenzustaende = matrix.eigenstates()
    rotationsachse = eigenzustaende[0]
    
    global anim
    starts = [np.array([v.a, v.b, v.c]).flatten() for v in list]
    ends = []
    for v in list:
        vector_neu = vector_from_state(matrix * state_from_vector(v))
        ends.append(np.array([vector_neu.a, vector_neu.b, vector_neu.c]).flatten())

    fps = 30

    gesamt_winkel = np.angle(eigenwerte[1]) - np.angle(eigenwerte[0])
    def frame_update(frame):
        t = frame / (fps - 1)

        achsen_state = vector_from_state(rotationsachse)
        achsen_vec = np.array([achsen_state.a, achsen_state.b, achsen_state.c])
        current = [vector(0, 0, 0, *rotiere(s, achsen_vec, t * gesamt_winkel), color=orig.color) for s, orig in zip(starts, list)]
        achse = rotationsachse if frame < fps - 1 else None
        update(current, achse)
        return ()
    anim = FuncAnimation(
        fig, frame_update, frames=fps,
        interval=1000/30, blit=False, repeat=False
    )
    fig.canvas.draw_idle()

    for i, v in enumerate(list):
        list[i] = vector_from_state(matrix * state_from_vector(v))
        list[i].color = v.color


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

def rotiere(v, achse, theta):
    achse = achse / np.linalg.norm(achse)
    return (v * np.cos(theta)
            + np.cross(achse, v) * np.sin(theta)
            + achse * np.dot(achse, v) * (1 - np.cos(theta)))


def draw_axis():
    #alle axen einstellungen
    ax.plot_wireframe(x, y, z, color='0', alpha=0.3, linewidth=0.2)
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
    ax.plot([-lim, lim], [0, 0], [0, 0], color='k', lw=1)
    ax.plot([0, 0], [-lim, lim], [0, 0], color='k', lw=1)
    ax.plot([0, 0], [0, 0], [-lim, lim], color='k', lw=1)

    ax.set_axis_off() 

    ax.text(0, 0, 1, "|0⟩", fontsize = 16)
    ax.text(0, 0, -1, "|1⟩", fontsize = 16)
    ax.text(0, 1, 0, "|i⟩", fontsize = 16)
    ax.text(0, -1, 0, "|-i⟩", fontsize = 16)
    ax.text(1, 0, 0, "|+⟩", fontsize = 16)
    ax.text(-1, 0, 0, "|-⟩", fontsize = 16)


fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
u = np.linspace(0, 2 * np.pi, 50)
v = np.linspace(0, np.pi, 50)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones_like(u), np.cos(v))

fig.canvas.mpl_connect('key_press_event', on_press)

matrix = qt.Qobj([[1/np.sqrt(2), 1/np.sqrt(2)], [1/np.sqrt(2), -1/np.sqrt(2)]])

update(list)


def input_loop():
    while True:
        global list
        global matrix
        text = input("0 = neuer Vektor, 1 = Neue Matrix, 2 = Vektoren löschen, q = Beenden: ")
        if text == "q":
            os._exit(0)
        try:
            if text == "0":
                text = input("Neuer Vektor (a+bj): ")
                alpha, beta = text.split(" ")
                list.append(vector_from_state((complex(alpha)*ket_0 + complex(beta)*ket_1).unit()))
                update(list)

            elif text == "1":
                text = input("Neue Matrix (a+bj a+bj a+bj a+bj): ")
                werte = text.split(" ")
                for i in range(len(werte)):
                    werte[i] = eval(werte[i])
                matrix = qt.Qobj([[werte[0], werte[1]], [werte[2], werte[3]]])

            elif text == "2":
                list = []
                update(list)
        except ValueError:
            print("Ungültig.")

threading.Thread(target=input_loop, daemon=True).start()
manager = plt.get_current_fig_manager()
plt.show()
