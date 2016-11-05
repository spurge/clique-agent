# -*- coding: utf-8 -*-

import yaml

from . import Virtz


class Capacity:
    """Used for checking capacity stored as an yaml file.
    Example of capacity yaml:
        # Maximum amount of resources
        capacity:
            machines: 0 # Unlimited
            cpu: 16
            mem: 8192 # MB
            disc: 128 # GB
        images:
            alpine: "/var/images/alpine-3.4.4-x86_64.iso"
    """

    def __init__(self, filename):
        self._capacity = None
        self._images = None
        self.__virtz = None

        self.load(filename)

    @property
    def virtz(self):
        if self.__virtz is None:
            self.__virtz = Virtz()

        return self.__virtz

    def load(self, filename):
        with open(filename, 'r') as f:
            config = yaml.load(f.read())

        self.set_capacity(**config['capacity'])
        self.set_images(**config['images'])

    def set_capacity(self, machines, cpu, mem, disc):
        self._capacity = dict(machines=int(machines),
                              cpu=int(cpu),
                              mem=int(mem),
                              disc=int(disc))

    def set_images(self, **images):
        self._images = images

    def capable(self, cpu, mem, disc):
        stats = self.virtz.stats()

        pass
