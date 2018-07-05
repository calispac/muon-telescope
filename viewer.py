from vpython import *
import numpy as np
from sklearn.linear_model import LinearRegression
import read


def compute_theta(direction):

    vertical_axis = vector(0, 1, 0)
    direction = direction.norm()

    theta = vertical_axis.dot(direction)
    theta = np.arccos(theta)

    if theta > np.pi / 2:

        theta = theta - np.pi

    theta = np.rad2deg(theta)

    return theta


def compute_phi(direction):

    phi = np.arctan(direction.z/direction.x)
    phi = np.rad2deg(phi)

    return phi


def fit_track(hits, track_length):


    epsilon = 5
    track_length += epsilon

    x = hits[:, 0]
    y = hits[:, 1]
    z = hits[:, 2]

    data = np.concatenate((x[:, np.newaxis],
                           y[:, np.newaxis],
                           z[:, np.newaxis]),
                          axis=1)

    # Calculate the mean of the points, i.e. the 'center' of the cloud
    datamean = data.mean(axis=0)

    # Do an SVD on the mean-centered data.
    uu, dd, vv = np.linalg.svd(data - datamean)

    # Now vv[0] contains the first principal component, i.e. the direction
    # vector of the 'best fit' line in the least squares sense.

    # Now generate some points along this best fit line, for plotting.

    # I use -7, 7 since the spread of the data is roughly 14
    # and we want it to have mean 0 (like the points we did
    # the svd on). Also, it's a straight line, so we only need 2 points.
    linepts = vv[0] * np.mgrid[-1:2:1][:, np.newaxis] * track_length / 2

    # shift by the mean to get the line in the right place
    linepts += datamean

    return linepts


def coordinates(arrow_length=800):

    pointer_x = arrow(pos=vector(0, 0, 0), axis=vector(arrow_length, 0, 0),
                    shaftwidth=1)
    pointer_y = arrow(pos=vector(0, 0, 0), axis=vector(0, arrow_length, 0),
                    shaftwidth=1)
    pointer_z = arrow(pos=vector(0, 0, 0), axis=vector(0, 0, arrow_length),
                    shaftwidth=1)

    return pointer_x, pointer_y, pointer_z


def layer(layer_position, bar_width=1, bar_height=1,
          bar_length=32*2, bar_spacing=1, n_bars=32, opacity=0.3):

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


def draw_spheres(radius, n_spheres, color=color.blue):

    spheres = []

    for i in range(n_spheres):

        temp = sphere(pos=vector(0, 0, 0), color=color, radius=radius)
        temp.visible = False
        spheres.append(temp)

    return spheres


def detector(n_layers, layer_spacing, detector_base, bar_width, bar_height,
             bar_length, bar_spacing, n_bars, opacity):

    bars_x = []
    bars_y = []

    for i in range(n_layers):

        y = i * layer_spacing
        pos = detector_base + vector(0, y, - center_z)
        bar_x, bar_y = layer(pos, bar_width=bar_width, bar_height=bar_height,
              bar_length=bar_length, bar_spacing=bar_spacing, n_bars=n_bars,
                             opacity=opacity)

        bars_x.append(bar_x)
        bars_y.append(bar_y)

    return bars_y, bars_x


def compute_rate(time, count):

    rate = np.average(time, weights=count)
    rate = 1 / rate

    return rate


def compute_exponential_pdf(x, rate, amplitude):

    temp = rate * np.exp(- rate * x)

    return temp * amplitude


if __name__ == '__main__':

    bar_width = 10
    bar_height = 7.5
    bar_length = 350
    bar_spacing = 0.1
    layer_spacing = 50
    n_bars = 32
    n_layers = 5
    opacity = 0.3

    TRACK_VISIBLE = True
    PAUSED = True
    FRAME_RATE = 1

    filename = 'data/real_data_7.txt'

    center_y = (layer_spacing * n_layers) / 2
    center_z = ((bar_spacing + bar_width) * n_bars) / 2

    def keyboard_input(event):

        global TRACK_VISIBLE
        global PAUSED
        global FRAME_RATE

        if event.key == 'delete':

            TRACK_VISIBLE = False if TRACK_VISIBLE else True

        elif event.key == 'down':

            FRAME_RATE = FRAME_RATE * 1.25

        elif event.key == 'up':

            FRAME_RATE = FRAME_RATE * 0.75
            FRAME_RATE = max(0, FRAME_RATE)

        elif len(event.key):

            PAUSED = False if PAUSED else True

    scene = canvas(width=1000,
                   height=800, align='left')

    scene.waitfor("redraw")
    # scene.waitfor('click keydown')

    scene.fullscreen =True
    scene.visible = True
    scene.waitfor("draw_complete")
    scene.autocenter = False

    detector_base = vector(0, 0, 0)

    detector_height = (2*bar_height) * n_layers + \
                      (bar_spacing + layer_spacing) * (n_layers - 1)
    scene.center = vector(0, detector_base.y + detector_height/2, 0)
    # scene.stereo = 'redcyan'

    track_length = ((bar_width + bar_spacing) * n_bars)**2
    track_length = ((2*bar_height + bar_spacing + layer_spacing) * n_layers)**2
    track_length = np.sqrt(track_length)

    bars_x, bars_y = detector(n_layers, layer_spacing, detector_base,
                              bar_width, bar_height, bar_length, bar_spacing,
                              n_bars, opacity)
    # coordinates()

    table_center = vector(0, 0, 0)

    cosmic_muon = sphere(pos=vector(0, 0, 0), radius=10, color=color.purple)
    cosmic_muon.visible = False

    text_hits = label(pos=vector(0, 0, 0), text='', xoffset=10, yoffset=20)
    text_hits.visible = TRACK_VISIBLE

    green = vector(163/255, 235/255, 12/255)

    scene.bind('keydown', keyboard_input)

    bins = np.linspace(0, np.pi/2, num=20)
    bins = np.rad2deg(bins)
    histogram_theta = np.zeros(len(bins) - 1)

    histogram_1 = graph(xtitle='angle au zenith [deg]',
                        ytitle='compte', align='right')

    bars_theta = gvbars(delta=bins[1]-bins[0], color=color.blue,
                        graph=histogram_1)

    histogram_2 = graph(xtitle='intervalle de temps [secondes]',
                        ytitle='compte', align='right')

    bins_time = np.linspace(0, 5, num=100)
    bins_time_diff = bins_time[1] - bins_time[0]
    count_time = np.zeros(len(bins_time) - 1)
    bars_time = gvbars(delta=bins_time_diff, color=color.blue,
                       graph=histogram_2)
    fit_curve = gcurve(color=color.red, graph=histogram_2)

    spheres = draw_spheres(radius=8, n_spheres=n_layers, color=color.blue)

    n_events = 0

    while True:

        for event_id, hits in enumerate(read.event_stream(filename=filename)):

            n_events += 1

            new_time = hits[1]
            hits = np.array(hits[0])
            hits[:, 0] = hits[:, 0] + 8
            hits[:, 1] = hits[:, 1] - 8
            hits[:, 2] = hits[:, 2] + 1

            phrase = 'Coordonnées : \n'

            if event_id == 0:

                previous_time = new_time
                continue

            scene.visible = False
            for x, y, z in hits:

                bars_x[z][x].color = green
                bars_y[z][y].color = green
                bars_x[z][x].opactiy = 0.8
                bars_y[z][y].opacity = 0.8
                phrase += '({}, {}, {}),\n'.format(x, y, z)

            phrase = phrase[:-2]
            text_hits.text = phrase

            regressor = LinearRegression()

            scalled_hits = hits.copy()

            scalled_hits[:, 0] = (scalled_hits[:, 0] - n_bars / 2 + 1) * (bar_width + bar_spacing)
            scalled_hits[:, 1] = (scalled_hits[:, 1] - n_bars / 2 + 1) * (bar_width + bar_spacing)
            scalled_hits[:, 2] = scalled_hits[:, 2] * layer_spacing + bar_height / 2

            for hit, scalled_hit in zip(hits, scalled_hits):

                pos = vector(scalled_hit[0], scalled_hit[2], scalled_hit[1])
                z = hit[2]
                spheres[z].pos = pos
                spheres[z].visible = True

            a = fit_track(scalled_hits, track_length)

            pos = [vector(a[i, 0], a[i, 2], a[i, 1]) for i in range(len(a))]

            highest_point = np.argmax(a[:, 2])
            track = curve(pos=pos, color=color.red)
            text_hits.pos = pos[highest_point]

            vector_track = pos[1] - pos[0]

            theta = compute_theta(vector_track)
            histogram_theta += np.histogram(theta, bins)[0]
            data = np.stack((bins[:-1], histogram_theta), axis=-1)
            bars_theta.data = data
            bars_theta.label = 'Total : {}'.format(n_events)

            time_diff = new_time - previous_time
            previous_time = new_time
            count_time += np.histogram(time_diff, bins_time)[0]
            data = np.stack((bins_time[:-1], count_time), axis=-1)
            bars_time.data = data
            bars_time.label = 'Total : {}'.format(n_events)

            x_fit = bins_time[:-1] + bins_time_diff / 2
            rate = compute_rate(x_fit, count_time)
            y_fit = compute_exponential_pdf(x_fit, rate, n_events)

            data = np.stack((x_fit, y_fit), axis=-1)
            fit_curve.data = data

            fit_curve.label = 'Taux : {:02f} [Hz]'.format(1. / rate)
            # fit_curve.legend = 'Rate'
            # label(display=fit_curve.display, pos=(3, 2), text="P")
            # histogram_2.title =

            track.visible = TRACK_VISIBLE
            text_hits.visible = TRACK_VISIBLE
            scene.visible = True

            while PAUSED:
                track.visible = TRACK_VISIBLE
                text_hits.visible = TRACK_VISIBLE
                time.sleep(time_diff)

            time.sleep(FRAME_RATE)

            text_hits.visible = False
            scene.visible = False
            track.visible = False

            for x, y, z in hits:

                bars_x[z][x].color = color.white
                bars_y[z][y].color = color.white
                bars_x[z][x].opactiy = opacity
                bars_y[z][y].opacity = opacity
                spheres[z].visible = False

            scene.visible = True
