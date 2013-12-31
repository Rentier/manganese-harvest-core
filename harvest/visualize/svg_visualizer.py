import numpy as np
import svgwrite

from harvest.visualize.visualizer import Visualizer

class SvgVisualizer(Visualizer):

    def normalize(self, points):
        pass

    def visualize(self, **kwargs):
        for z in zip(self.positions_x[-1], self.positions_y[-1]):
            print z
        return
        filename = kwargs.get('filename', 'harvest.svg')
        lines = np.empty([self.n, self.t])
        
        svg_document = svgwrite.Drawing(filename=filename, size=("800px", "800px"))

        for points in zip(self.positions_x.T, self.positions_y.T):
            path = np.array(points).T
            svg_document.add( svgwrite.shapes.Polyline(points=path,
                                                       stroke_width = "1",
                                                       stroke = "black"))

        svg_document.add(svg_document.text("Hello World",
                                           insert = (210, 110)))
        
        svg_document.save()
        
                