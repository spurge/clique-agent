# -*- coding: utf-8 -*-

import libvirt

from os import listdir, path
from xml.etree import ElementTree

from template import get_domain


class Virtz:

    def __init__(self):
        self.network_dir = './networks'
        self.libvirt_host = 'qemu:///system'

        self.connect()
        self.networks()

    def connect(self):
        self.conn = libvirt.open(self.libvirt_host)

    def networks(self):
        for filename in listdir(self.network_dir):
            xml = ElementTree.parse(path.join(self.network_dir,
                                              filename))
            name = xml.getroot().find('name').text

            try:
                network = self.conn.networkLookupByName(name)

                if network is not None:
                    network.destroy()
                    network.undefine()
            except:
                pass

            self.conn.networkDefineXML(
                ElementTree.tostring(xml.getroot(),
                                     encoding='utf8',
                                     method='xml').decode('utf-8')
            )

            network = self.conn.networkLookupByName(name)
            network.create()

    def get(self, name):
        try:
            machine = self.conn.lookupByName(name)
        except:
            machine = None

        return machine

    def create(self, name, **kwargs):
        machine = self.get(name)

        if machine is not None and machine.isActive():
            return machine

        self.remove(name)

        self.conn.defineXML(get_domain(name, **kwargs))

        return self.get(name)

    def remove(self, name):
        machine = self.get(name)

        if machine is not None:
            machine.undefine()

    def start(self, name, **kwargs):
        machine = self.create(name, **kwargs)

        if not machine.isActive():
            machine.create()

        return machine

    def stop(self, name):
        machine = self.get(name)

        if machine is not None and machine.isActive():
            machine.destroy()
