import sys
import time

import matplotlib.cm
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets

points_count = 10 ** 4

class DynamicScatterPlot(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        # self.graphics_layout_widget = pg.GraphicsLayoutWidget()
        self.graphics_layout_widget = pg.PlotWidget()
        # self.plot_widget = self.graphics_layout_widget.addPlot()
        self.plot_widget = self.graphics_layout_widget
        self.scatter_plot_item = None
        self.data = np.random.rand(points_count, 2)
        self.intensity_channels = [np.random.rand(points_count) for _ in range(points_count)]

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.slider.setRange(0, 100)
        self.slider.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.slider.setFocus()
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(lambda x: self.scatter_plot(x))

        layout.addWidget(self.graphics_layout_widget)
        layout.addWidget(self.slider)

        self.slider.setValue(30)

    def get_brushes(self, intensities):
        a = min(intensities)
        b = max(intensities)
        colormap = matplotlib.cm.viridis
        positions = np.linspace(a, b, len(colormap.colors), endpoint=True)
        q_colormap = pg.ColorMap(pos=positions, color=colormap.colors)
        color_for_points = q_colormap.map(intensities)
        brushes = [QtGui.QBrush(QtGui.QColor(*color_for_points[i, :].tolist())) for i in
                   range(color_for_points.shape[0])]
        return brushes

    def scatter_plot(self, channel):
        start = time.time()
        brushes = self.get_brushes(self.intensity_channels[channel])
        print(f'creating brushes: {time.time() - start}')
        if self.scatter_plot_item is None:
            start = time.time()
            # from pyqtgraph.opengl import GLScatterPlotItem
            # import numpy as np
            # self.scatter_plot_item = GLScatterPlotItem(pos=np.random.random((10000, 3)),
            #                                            color=np.random.random((10000, 4)))

            self.scatter_plot_item = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None))
            self.scatter_plot_item.clear()
            self.scatter_plot_item.setData(pos=self.data, brush=brushes)
            # self.scatter_plot_item.setData(pos=self.data, brush='b')
            self.plot_widget.clear()
            self.plot_widget.addItem(self.scatter_plot_item)
            print(f'first rendering: {time.time() - start}')
        else:
            start = time.time()
            # brushes = [QtGui.QBrush(QtGui.QColor(255, 255, 255, 255)) for _ in range(len(brushes))]
            self.scatter_plot_item.setBrush(brushes)
            # brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 255))
            # self.scatter_plot_item.setBrush(brush)
            self.plot_widget.repaint()
            print(f'updating colors: {time.time() - start}')


if __name__ == '__main__':
    print(f'PyQtGraph version: {pg.__version__}')
    print(f'Qt Python binding: {pg.Qt.VERSION_INFO}')
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        app = pg.mkQApp()
        viewer = DynamicScatterPlot()
        viewer.setWindowTitle('Dynamic Scatter Plot')
        viewer.show()
        QtGui.QApplication.instance().exec_()
        sys.exit(app.exec_())
