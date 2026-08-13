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

print(x)
print(y)
print(z)
ax.plot_wireframe(x, y, z, color='0', alpha=1, linewidth=0.2)
ax.set_box_aspect([1,1,1])
plt.show()
