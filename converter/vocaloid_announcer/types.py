class SoundComponent(object):
    pass


class VSQRegion(SoundComponent):
    _region_name = ''

    def __init__(self, name):
        super(SoundComponent, self).__init__()
        self._region_name = name


class Pause(SoundComponent):
    _measures = 0

    def __init__(self, measures):
        super(SoundComponent, self).__init__()
        if type(measures) is str:
            measures = len(measures)
        self._measures = measures
