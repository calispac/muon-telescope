from vpython import *
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import read


def coordinates(arrow_length=800):

    pointer_x = arrow(pos=vector(0, 0, 0), axis=vector(arrow_length, 0, 0),
                    shaftwidth=1)
    pointer_y = arrow(pos=vector(0, 0, 0), axis=vector(0, arrow_length, 0),
                    shaftwidth=1)
    pointer_z = arrow(pos=vector(0, 0, 0), axis=vector(0, 0, arrow_length),
                    shaftwidth=1)

    return pointer_x, pointer_y, pointer_z


def layer(layer_position, bar_width=1, bar_height=1,
          bar_length=32*2, bar_spacing=1, n_bars=32, opacity=0.8):

    bars_x = []
    bars_y = []
    size = vector(bar_length, bar_height, bar_width)

    axis_x = vector(1, 0, 0)
    axis_y = vector(0, 0, 1)

    length = (bar_width + bar_spacing) * n_bars

    for bar_id in range(n_bars):

        pos = (bar_width + bar_spacing) * (bar_id + 1)

        pos_x = layer_position + vector(0, 0, pos)
        pos_y = layer_position + vector(pos - length / 2,
                                        bar_height, length / 2)

        bars_x.append(box(pos=pos_x, size=size, opacity=opacity, axis=axis_x))
        bars_y.append(box(pos=pos_y, size=size, opacity=opacity, axis=axis_y))

    return bars_x, bars_y


def detector(n_layers, layer_spacing, detector_base, bar_width, bar_height,
             bar_length, bar_spacing, n_bars):

    bars_x = []
    bars_y = []

    for i in range(n_layers):

        y = i * layer_spacing
        pos = detector_base + vector(0, y, - center_z)
        bar_x, bar_y = layer(pos, bar_width=bar_width, bar_height=bar_height,
              bar_length=bar_length, bar_spacing=bar_spacing, n_bars=n_bars)

        bars_x.append(bar_x)
        bars_y.append(bar_y)

    return bars_y, bars_x


if __name__ == '__main__':

    bar_width = 10
    bar_height = 7.5
    bar_length = 350
    bar_spacing = 0.1

    layer_spacing = 50

    n_bars = 32
    n_layers = 5

    center_y = (layer_spacing * n_layers) / 2
    center_z = ((bar_spacing + bar_width) * n_bars) / 2

    scene.waitfor("redraw")

    scene.fullscreen =True
    scene.visible = True
    scene.waitfor("draw_complete")
    # scene.stereo = 'redcyan'

    table_height = 30
    space_table_detector = 5
    detector_base = vector(0, table_height + space_table_detector, 0)

    bars_x, bars_y = detector(n_layers, layer_spacing, detector_base, bar_width,
                    bar_height, bar_length, bar_spacing, n_bars)
    coordinates()

    table_center = vector(0, 0, 0)

    # table = box(pos=table_center,
    #            size=vector(center_z*4, table_height, center_z*4),
    #            texture=textures.wood,
    #            )

    # cosmic_muon = sphere(make_trail=True, trail_type="points",
    #              interval=10, retain=50, color=color.red)

    for hits in read.event_stream('data/visualPythonIn.txt'):
        n_hits = 2

        #hits = [[np.random.randint(0, 32), np.random.randint(0, 32),
        #         np.random.randint(0, 5)] for i in range(n_hits)]

        hits = np.array(hits)

        scene.visible = False
        for x, y, z in hits:

            print(x, y, z)

            bars_x[z][x].color = color.green
            bars_y[z][y].color = color.green

        regressor = LinearRegression()

        scalled_hits = hits.copy()

        print(hits)
        # permutation = [0, 2, 1]
        # scalled_hits = scalled_hits[:, permutation]
        print(scalled_hits)

        scalled_hits[:, 0] = (scalled_hits[:, 0] - n_bars / 2) * (bar_width + bar_spacing)
        scalled_hits[:, 1] = (scalled_hits[:, 1] - n_bars / 2) * (bar_width + bar_spacing)
        scalled_hits[:, 2] = scalled_hits[:, 2] * (bar_height + layer_spacing) + table_height + space_table_detector
        print(scalled_hits)

        regressor.fit(scalled_hits[:, :1], scalled_hits[:, 2])

        a = regressor.predict(scalled_hits[:, :1])

        print(a)

        """
        bottom_point = np.argmin(a)
        top_point = np.argmax(a)

        scalled_hits[bottom_point] = scalled_hits[bottom_point]
        scalled_hits[top_point] = scalled_hits[top_point]

        scalled_hits = scalled_hits[[bottom_point, top_point]]
        """

        pos = [(scalled_hits[i, 0], a[i], scalled_hits[i, 1]) for i in range(len(scalled_hits))]

        # track = curve(pos=pos, color=color.red)

        scene.visible = True

        time.sleep(4)

        scene.visible = False
        # track.visible = False

        for x, y, z in hits:

            bars_x[z][x].color = color.white
            bars_y[z][y].color = color.white

        scene.visible = True

