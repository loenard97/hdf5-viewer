import numpy as np
import pyqtgraph as pg


class DataImageView(pg.ImageView):

    def __init__(self, data):
        super().__init__()

        self.setImage(data)
        self.setColorMap(pg.colormap.get("inferno"))


class DataImageRGBView(pg.ImageView):

    def __init__(self, data):
        super().__init__()

        data = np.sum(data, axis=0)
        self.setImage(data)
        self.setColorMap(pg.colormap.get("inferno"))
