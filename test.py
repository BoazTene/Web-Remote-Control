from multiprocessing import Process
import time

class P(Process):
    def __init__(self):
        super(P, self).__init__()
    def run(self):
        print('hello')

if __name__ == '__main__':
    p = P()
    p.start()
    p.join()