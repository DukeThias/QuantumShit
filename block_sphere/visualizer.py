import matplotlib.pyplot as plt
import numpy as np

from matplotlib.backend_bases import MouseButton

t = np.arange(0.0, 1.0, 0.01)
s = np.sin(2 * np.pi * t)
fig, ax = plt.subplots()
ax.plot(t, s)


def on_click(event):
    if event.button is MouseButton.LEFT:
        print('linke Maustaste')
    elif event.button is MouseButton.RIGHT:
        print("rechte Maustaste")

plt.connect('button_press_event', on_click)

plt.show()
