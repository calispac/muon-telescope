

def event_stream(filename):

    with open(filename) as file:

        for line in file.readlines():

            event = []
            hit = []
            time = 0

            for i, string in enumerate(line.split()):

                if i == 0:

                    time = float(string)

                else:

                    hit.append(int(string))

                    if i % 3 == 0 and i != 0:

                        hit = tuple(hit)
                        event.append(hit)
                        hit = []

            yield event, time


if __name__ == '__main__':

    for event in event_stream('data/visualPythonIn.txt'):

        print(event)
