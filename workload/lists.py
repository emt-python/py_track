import time


class SimpleListManipulationrange:

    version = 2.0
    operations = 5 * (6 + 6 + 6)
    rounds = 130000

    def test(self):

        l = []
        append = l.append

        for i in range(self.rounds):

            append(2)
            append(3)
            append(4)
            append(2)
            append(3)
            append(4)

            l[0] = 3
            l[1] = 4
            l[2] = 5
            l[3] = 3
            l[4] = 4
            l[5] = 5

            x = l[0]
            x = l[1]
            x = l[2]
            x = l[3]
            x = l[4]
            x = l[5]

            append(2)
            append(3)
            append(4)
            append(2)
            append(3)
            append(4)

            l[0] = 3
            l[1] = 4
            l[2] = 5
            l[3] = 3
            l[4] = 4
            l[5] = 5

            x = l[0]
            x = l[1]
            x = l[2]
            x = l[3]
            x = l[4]
            x = l[5]

            append(2)
            append(3)
            append(4)
            append(2)
            append(3)
            append(4)

            l[0] = 3
            l[1] = 4
            l[2] = 5
            l[3] = 3
            l[4] = 4
            l[5] = 5

            x = l[0]
            x = l[1]
            x = l[2]
            x = l[3]
            x = l[4]
            x = l[5]

            append(2)
            append(3)
            append(4)
            append(2)
            append(3)
            append(4)

            l[0] = 3
            l[1] = 4
            l[2] = 5
            l[3] = 3
            l[4] = 4
            l[5] = 5

            x = l[0]
            x = l[1]
            x = l[2]
            x = l[3]
            x = l[4]
            x = l[5]

            append(2)
            append(3)
            append(4)
            append(2)
            append(3)
            append(4)

            l[0] = 3
            l[1] = 4
            l[2] = 5
            l[3] = 3
            l[4] = 4
            l[5] = 5

            x = l[0]
            x = l[1]
            x = l[2]
            x = l[3]
            x = l[4]
            x = l[5]

            if len(l) > 10000:
                # cut down the size
                del l[:]

    def calibrate(self):

        l = []
        append = l.append

        for i in range(self.rounds):
            pass


class ListSlicingrange:

    version = 2.0
    operations = 25*(3+1+2+1)
    rounds = 800

    def test(self):

        n = range(1000)
        r = range(25)

        for i in range(self.rounds):

            l = n[:]

            for j in r:

                m = l[50:]
                m = l[:25]
                m = l[50:55]
                m = l[:-1]
                m = l[1:]

    def calibrate(self):

        n = range(1000)
        r = range(25)

        for i in range(self.rounds):
            for j in r:
                pass


class SmallListsrange:

    version = 2.0
    operations = 5*(1 + 6 + 6 + 3 + 1)
    rounds = 80000

    def test(self):

        for i in range(self.rounds):

            l = []

            append = l.append
            append(2)
            append(3)
            append(4)
            append(2)
            append(3)
            append(4)

            l[0] = 3
            l[1] = 4
            l[2] = 5
            l[3] = 3
            l[4] = 4
            l[5] = 5

            l[:3] = [1, 2, 3]
            m = l[:-1]
            m = l[1:]

            l[-1:] = [4, 5, 6]

            l = []

            append = l.append
            append(2)
            append(3)
            append(4)
            append(2)
            append(3)
            append(4)

            l[0] = 3
            l[1] = 4
            l[2] = 5
            l[3] = 3
            l[4] = 4
            l[5] = 5

            l[:3] = [1, 2, 3]
            m = l[:-1]
            m = l[1:]

            l[-1:] = [4, 5, 6]

            l = []

            append = l.append
            append(2)
            append(3)
            append(4)
            append(2)
            append(3)
            append(4)

            l[0] = 3
            l[1] = 4
            l[2] = 5
            l[3] = 3
            l[4] = 4
            l[5] = 5

            l[:3] = [1, 2, 3]
            m = l[:-1]
            m = l[1:]

            l[-1:] = [4, 5, 6]

            l = []

            append = l.append
            append(2)
            append(3)
            append(4)
            append(2)
            append(3)
            append(4)

            l[0] = 3
            l[1] = 4
            l[2] = 5
            l[3] = 3
            l[4] = 4
            l[5] = 5

            l[:3] = [1, 2, 3]
            m = l[:-1]
            m = l[1:]

            l[-1:] = [4, 5, 6]

            l = []

            append = l.append
            append(2)
            append(3)
            append(4)
            append(2)
            append(3)
            append(4)

            l[0] = 3
            l[1] = 4
            l[2] = 5
            l[3] = 3
            l[4] = 4
            l[5] = 5

            l[:3] = [1, 2, 3]
            m = l[:-1]
            m = l[1:]

            l[-1:] = [4, 5, 6]

    def calibrate(self):

        for i in range(self.rounds):
            pass


class SimpleListComprehensionsrange:

    version = 2.0
    operations = 6
    rounds = 20000

    def test(self):

        n = range(1000)

        for i in range(self.rounds):
            l = [x for x in n]
            l = [x for x in n if x]
            l = [x for x in n if not x]

            l = [x for x in n]
            l = [x for x in n if x]
            l = [x for x in n if not x]

    def calibrate(self):

        n = range(1000)

        for i in range(self.rounds):
            pass


class NestedListComprehensionsrange:

    version = 2.0
    operations = 6
    rounds = 20000

    def test(self):

        m = range(10)
        n = range(1000)

        for i in range(self.rounds):
            l = [x for x in n for y in m]
            l = [y for x in n for y in m]

            l = [x for x in n for y in m if y]
            l = [y for x in n for y in m if x]

            l = [x for x in n for y in m if not y]
            l = [y for x in n for y in m if not x]

    def calibrate(self):

        m = range(10)
        n = range(1000)

        for i in range(self.rounds):
            pass


if __name__ == "__main__":
    start_time = time.time()
    ins1 = SimpleListManipulationrange()
    ins1.test()
    ins1.calibrate()
    ins2 = ListSlicingrange()
    ins2.test()
    ins2.calibrate()
    ins3 = SmallListsrange()
    ins3.test()
    ins3.calibrate()
    ins4 = SimpleListComprehensionsrange()
    ins4.test()
    ins4.calibrate()
    ins5 = NestedListComprehensionsrange()
    ins5.test()
    ins5.calibrate()
    elapsed_time = time.time() - start_time
    print(f"Compute time: {elapsed_time:.2f} seconds")
