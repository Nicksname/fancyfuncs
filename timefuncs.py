import numpy as np
from time import clock

__all__= ['timer']

class timer:
    def __init__(self):
        ''' Class to time calculation '''
        self.timedict = {}
        self._events = []

    def __call__(self, *events):
        ''' Create new timemarks for ``events``
        Parameters
        ----------
        *events : comma seperated strings
            events to create a new timemark for. Names can be used for indexing
            when first timing for ``event`` has stopped.
        '''

        now = clock()
        # dictionaries are called by reference
        timedict = self.timedict

        for event in events:
            if event not in timedict.keys():
                timedict[event] = np.array(now)
                self._events.append(event)
                print('running {}'.format(event))
            else:
                timedict[event] = np.append(timedict[event], now)

                time = now - timedict[event][-2]
                print('{} time: {:.2f}s'.format(event, time))

                if len(timedict[event]) > 2:
                    tottime = now - timedict[event][0]
                    print('total {} time: {:.2f}s'.format(event, tottime))

    @property
    def events(self):
        return self._events

    def __getitem__(self, event):
        timedict = self.timedict
        try:
            times = timedict[event][1:] - timedict[event][:-1]
        except IndexError:
            raise UserWarning('Timing not stopped.')

        return times

    def __len__(self):
        return len(self.timedict)
