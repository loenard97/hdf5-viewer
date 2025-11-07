import pyqtgraph as pg


class ArrayPlotWidget(pg.PlotWidget):

    def __init__(self, data):
        super().__init__()

        if data.ndim == 2 and min(data.shape) == 1:
            data = data.ravel()
        self.plot(data, pen="black")
