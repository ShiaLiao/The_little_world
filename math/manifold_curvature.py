import numpy as np

class OpenBall:
    def __init__(self, center, radius):
        self.center = np.array(center)
        self.radius = radius

    def contains(self, point):
        return np.linalg.norm(np.array(point) - self.center) < self.radius

class OpenSet:
    def __init__(self):
        self.open_balls = []

    def add_open_ball(self, open_ball):
        self.open_balls.append(open_ball)

    def contains(self, point):
        return any(ball.contains(point) for ball in self.open_balls)

class Chart:
    def __init__(self, subset, phi):
        self.subset = subset
        self.phi = phi

    def is_one_to_one_on_subset(self):
        #待实现
        pass

class Atlas:
    def __init__(self):
        self.charts = []

    def add_chart(self, chart):
        self.charts.append(chart)

    def covers(self, manifold):
        points_covered = set()
        for chart in self.charts:
            points_covered.update(chart.subset)
        return points_covered == manifold.set

class Manifold:
    def __init__(self, set, atlas):
        self.set = set
        self.atlas = atlas

    def is_maximal_atlas(self, atlas):
        #待实现
        pass
