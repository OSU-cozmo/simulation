import logging

class worldState:
    objects = []

    def __init__(self):
        """Initializes an instance of the world state object."""

        logger = logging.getLogger('STATE')
        logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)


        formatter = logging.Formatter('%(name)s > %(levelname)2s >> %(message)s')


        ch.setFormatter(formatter)

        logger.addHandler(ch)
        self.log = logger

    def updateState(self, body):
        pass;

    def initState(self, body):
        self.log.info("Initializing state\n")

        for x in body['objects']:
            temp = worldObject(x)
            self.objects.append(x)

class worldObject:
    atts = []
    def __init__(self, info):
        for x in info:
            setattr(self, x, info[x])
            self.atts.append(x)

    def get(self, field):
        if field in self.atts:
            return getattr(self, field);
        else:
            return None
    def getAtts(self):
        return self.atts
