# -*- coding: utf-8 -*-

from xml.etree import ElementTree

def get_domain(name, image, cpu, mem):
    xml = ElementTree.parse('clique_agent/templates/domain.xml')
    root = xml.getroot()

    name_el = root.find('name')
    name_el.text = name

    image_el = root.find('devices/disk[@device="cdrom"]/source')
    image_el.set('file', '/var/images/%s.iso' % image)

    cpu_el = root.find('vcpu')
    cpu_el.text = str(cpu)

    mem_el = root.find('memory')
    mem_el.text = str(mem)

    return ElementTree.tostring(root,
                                encoding='utf8',
                                method='xml').decode('utf-8')
