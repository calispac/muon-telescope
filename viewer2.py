from vpython import *
import numpy as np
import pandas as pd


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

        pos = (bar_width + bar_spacing) * bar_id

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

    return bars_x, bars_y


if __name__ == '__main__':

    bar_width = 10
    bar_height = 7.5
    bar_length = 350
    bar_spacing = 0.1

    layer_spacing = 3 * bar_height

    n_bars = 32
    n_layers = 5

    center_y = (layer_spacing * n_layers) / 2
    center_z = ((bar_spacing + bar_width) * n_bars) / 2

    scene.waitfor("redraw")

    scene.fullscreen =True
    scene.visible = False
    scene.waitfor("draw_complete")
    # scene.stereo = 'redcyan'

    table_height = 30
    detector_base = vector(0, table_height + 5, 0)

    bars_x, bars_y = detector(n_layers, layer_spacing, detector_base, bar_width,
                    bar_height, bar_length, bar_spacing, n_bars)
    coordinates()

    table_center = vector(0, 0, 0)

    table = box(pos=table_center,
                size=vector(center_z*4, table_height, center_z*4),
                texture=textures.wood,
                )

    track = curve(vector(0, 800, 0), vector(0, -800, 0), color=color.red)

    # cosmic_muon = sphere(make_trail=True, trail_type="points",
    #              interval=10, retain=50, color=color.red)

    hits = [(0, 0, 0), (4, 12, 2), (31, 12, 4)]

    for x, y, z in hits:

        bars_x[z][x].color = color.green
        bars_y[z][y].color = color.green

    scene.visible = True
