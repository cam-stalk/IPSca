import os

class Logger:

    def __init__(self):
        self.files = []

    def logging(self, device, vendor, log):
        writepath = f'results/{device}/{vendor}.txt'
        mode = 'a' if os.path.exists(writepath) else 'w'

        if any([device == f.name for f in self.files]):
            for f in self.files:
                if f.name.split('/')[2] == (device + '.txt'):
                    f.write(log)
        else:
            f = open(writepath, mode)
            f.write(log + '\n')
            self.files.append(f)

    def close_all(self):
        # print('Closing files...')
        [f.close() for f in self.files]


