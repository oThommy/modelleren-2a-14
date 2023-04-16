from pathlib import Path


ROOT_DIR = Path(__file__).parent.resolve()
DATA_DIR = (ROOT_DIR / '..' / 'data').resolve()
OUT_DIR = (ROOT_DIR / '..' / 'out').resolve()
ALPHA = 0.05
POLYNOMIAL_DEGREE = 8

# Colours for plotting using matplotlib.pyplot
TURQUOISE = (31 / 255, 119 / 255, 180 / 255)
TRUE_PLOT_COLOR = TURQUOISE
PREDICTED_PLOT_COLOR = 'red'