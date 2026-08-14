import matplotlib.pyplot as plt
import numpy as np
import sys
import qutip as qt
from matplotlib.widgets import TextBox
from matplotlib.backend_bases import MouseButton
from matplotlib.animation import FuncAnimation

ket_0 = qt.Qobj([1, 0])
ket_1 = qt.Qobj([0, 1])

list = []

class vector:
    def __init__(self, x, y, z, a, b, c):
        self.x = x
        self.y = y
        self.z = z
        self.a = a
        self.b = b
        self.c = c
    def plot(self):
        ax.quiver(self.x, self.y, self.z, self.a, self.b, self.c)

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
    print('press', event.key)
    sys.stdout.flush()
    if event.key == 'y':
        apply_matrix(matrix)

    elif event.key == 'x':
        list = []
        update(list)

def submit_alpha(text):
    try:
        alpha = complex(text.split(" ")[0])
        beta = complex(text.split(" ")[1])
        list.append(vector_from_state((alpha*ket_0 + beta*ket_1).unit()))
        update(list)
    except ValueError:
        print("Ungültiger Wert.")

def apply_matrix(matrix):

    rotationsachse = matrix.eigenstates()[1][0]
    
    global anim
    starts = [np.array([v.a, v.b, v.c]).flatten() for v in list]
    ends = []
    for v in list:
        vector_neu = vector_from_state(matrix * state_from_vector(v))
        ends.append(np.array([vector_neu.a, vector_neu.b, vector_neu.c]).flatten())

    fps = 30

    def frame_update(frame):
        t = frame / (fps - 1)
        current = [vector(0, 0, 0, *slerp(s, e, t)) for s, e in zip(starts, ends)]
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

def slerp(v1, v2, t):
    dot = np.clip(np.dot(v1, v2), -1.0, 1.0)
    omega = np.arccos(dot)
    if omega < 1e-6:
        return v1  # Vektoren praktisch identisch
    sin_omega = np.sin(omega)
    return (np.sin((1 - t) * omega) / sin_omega) * v1 + (np.sin(t * omega) / sin_omega) * v2
 

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
ax = fig.add_subplot(111, projection='3d')

u = np.linspace(0, 2 * np.pi, 50)
v = np.linspace(0, np.pi, 50)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones_like(u), np.cos(v))

fig.canvas.mpl_connect('key_press_event', on_press)
ax_alpha = plt.axes([0.15, 0.05, 0.3, 0.06])
alpha_beta_box = TextBox(ax_alpha, "2 komplexe Zahlen (bsp: 2+3j) ")
alpha_beta_box.on_submit(submit_alpha)

def updateframe(frame):
    # for each frame, update the data stored on each artist.
    x = t[:frame]
    y = z[:frame]
    # update the scatter plot:
    data = np.stack([x, y]).T
    scat.set_offsets(data)
    # update the line plot:
    line2.set_xdata(t[:frame])
    line2.set_ydata(z2[:frame])
    return (scat, line2)


test_theta = np.pi / 2
test_phi = np.pi * 3/4

for i in range(3): list.append(vector_from_state(((np.random.randint(-100, 100)+(np.random.randint(-100, 100)*1j))*ket_0 + (np.random.randint(-100, 100)+(np.random.randint(-100, 100)*1j))*ket_1).unit()))
list.append(vector_from_state((1*ket_0 + 0*ket_1).unit()))
print(len(list))
matrix = qt.Qobj([[1, 0], [0, -1]])

update(list)



plt.show()
