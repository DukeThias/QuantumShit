# QuantumShit

Ein interaktiver Bloch-Kugel-Visualizer zum Rumspielen mit Qubit-Zuständen, gebaut mit [QuTiP](https://qutip.org/) und matplotlib.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Danach starten mit:

```bash
python3 block_sphere/visualizer.py
```

## Inhalt

- `block_sphere/visualizer.py` – Visualisierung der Bloch-Kugel, steuerbar per Tastatur (`k` neuer Vektor, `y` Matrix anwenden, `x` alles löschen) oder interaktiv im Terminal
