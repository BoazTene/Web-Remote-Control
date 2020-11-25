import threading


class Data:
    def __init__(self):
        self.data = []


def test(data):
    while True:
        print(data.data)


if __name__ == "__main__":
    data = Data()
    threading.Thread(target=test, args=(data,)).start()

    index = 0
    while True:
        data.data.append(index)
        index += 1