from vpython import *
import numpy as np


def layer(layer_position, layer_angle=0, bar_width=1, bar_height=1,
          bar_length=32*2, bar_spacing=1, n_bars=32, c=color.white, opacity=0.5):

    bars = [None]*n_bars
    size = vector(bar_length, bar_height, bar_width)

    axis = vector(np.cos(layer_angle), 0., np.sin(layer_angle))

    for bar_id in range(len(bars)):

        pos = layer_position + vector(0, 0, (bar_width + bar_spacing) * bar_id)

        bars[bar_id] = box(pos=pos, size=size, color=c, opacity=opacity)

    bars_object = compound(bars)
    bars_object.axis = axis
    return bars


bar_width = 10
bar_height = 7.5
bar_length = 350
bar_spacing = 0.1

layer_spacing = 3 * bar_height


n_bars = 32
n_layers = 5

center_y = (layer_spacing * n_layers) / 2
center_z = ((bar_spacing + bar_width) * n_bars) / 2

scene.fullscreen =True
# scene.stereo = 'redcyan'

table_height = 30
detector_base = vector(0, table_height + 5, 0)

for i in range(n_layers):

    y = i * layer_spacing
    pos = detector_base + vector(0, y, - center_z)
    layer(pos, bar_width=bar_width, bar_height=bar_height,
          bar_length=bar_length, bar_spacing=bar_spacing, n_bars=n_bars)
    layer(pos + vector(0, bar_height, 0), layer_angle=np.pi/2,
          bar_width=bar_width, bar_height=bar_height,
          bar_length=bar_length, bar_spacing=bar_spacing, n_bars=n_bars,
          c=color.white
          )


pointer = arrow(pos=vector(0, 0, 0), axis=vector(800, 0, 0), shaftwidth=1)
pointer = arrow(pos=vector(0, 0, 0), axis=vector(0, 800, 0), shaftwidth=1)
pointer = arrow(pos=vector(0, 0, 0), axis=vector(0, 0, 800), shaftwidth=1)


table_center = vector(0, 0, 0)

table = box(pos=table_center,
            size=vector(center_z*4, table_height, center_z*4),
            texture=textures.wood,
            )

track = curve(vector(-1000, 1000, 0), vector(1000, -1000,0), color=color.red)


print(track.point(0), track.point(1))

cosmic_muon = sphere(make_trail=True, trail_type="points",
              interval=10, retain=50, color=color.red)

