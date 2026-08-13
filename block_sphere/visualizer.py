import matplotlib.pyplot as plt
import numpy as np

from matplotlib.backend_bases import MouseButton

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


u = np.linspace(0, 2 * np.pi, 50)
v = np.linspace(0, np.pi, 50)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones_like(u), np.cos(v))


def coords_from_angle(theta, phi):
    px = np.sin(theta) * np.cos(phi)
    py = np.sin(theta) * np.sin(phi)
    pz = np.cos(theta)
    return px, py, pz

test_theta = np.pi / 2
test_phi = np.pi * 3/4

test_coords = coords_from_angle(test_theta, test_phi)
ax.quiver(0, 0, 0, test_coords[0], test_coords[1], test_coords[2])

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
ax.text(0, 1, 0, "|+⟩", fontsize = 16)
ax.text(0, -1, 0, "|-⟩", fontsize = 16)
ax.text(1, 0, 0, "|i⟩", fontsize = 16)
ax.text(-1, 0, 0, "|-i⟩", fontsize = 16)

plt.show()
