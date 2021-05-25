class Panel():

    thing = 50

    def __init__(self):

        global thing

        thing += 10

        print(thing)


class Diary():

    def __init__(self, thing):

        panel = Panel()


two = Diary(10)
