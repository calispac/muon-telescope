

def event_stream(filename):

    with open(filename) as file:

        for line in file.readlines():

            event = []
            hit = []

            for i, string in enumerate(line.split()):

                hit.append(int(string))

                if i % 3 == 2 and i != 0:
                    hit = tuple(hit)
                    event.append(hit)
                    hit = []

            yield event


if __name__ == '__main__':

    for event in event_stream('data/visualPythonIn.txt'):

        print(event)
