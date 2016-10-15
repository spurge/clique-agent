# -*- coding: utf-8 -*-

import libvirt

from xml.etree import ElementTree


class Virtz:

    def __init__(self):
        self.conn = libvirt.open('qemu:///system')

    def get(self, name):
        try:
            machine = self.conn.lookupByName(name)
        except:
            machine = None

        return machine

    def create(self, name, image, cpu, mem):
        self.remove(name)

        xml = ElementTree.parse('templates/domain.xml')
        root = xml.getroot()

        name_el = root.find('name')
        name_el.text = name

        self.conn.defineXML(
            ElementTree.tostring(root,
                                 encoding='utf8',
                                 method='xml').decode('utf-8')
        )

        return self.get(name)

    def remove(self, name):
        machine = self.get(name)

        if machine is not None:
            machine.undefine()

    def start(self, name, **kwargs):
        machine = self.create(name, **kwargs)
        machine.create()

        return machine

    def stop(self, name):
        machine = self.get(name)

        if machine is not None:
            machine.destroy()
