# -*- coding: utf-8 -*-

import libvirt

from xml.etree import ElementTree


class Virtz:

    def __init__(self):
        self.conn = libvirt.open('qemu:///system')

    def start(self, name, image, cpu, mem):
        xml = ElementTree.parse('templates/domain.xml')
        root = xml.getroot()

        name_el = root.find('name')
        name_el.text = name

        self.conn.defineXML(ElementTree.tostring(
                                root,
                                encoding='utf8',
                                method='xml').decode('utf-8'))
