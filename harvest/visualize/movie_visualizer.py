from harvest.visualize.plot_visualizer import PlotVisualizer

class MovieVisualizer(PlotVisualizer):

    def visualize(self, **kwargs):
        self.do_animation(vid=True)