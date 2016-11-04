# -*- coding: utf-8 -*-

from unittest import TestCase
from xml.etree import ElementTree

from clique_agent.template import get_domain


class TestTemplate(TestCase):

    def test_get_domain(self):
        xml = ElementTree.fromstring(get_domain('testmachine',
                                                'alpine',
                                                2,
                                                1024))

        self.assertEqual(xml.find('name').text, 'testmachine')
        self.assertEqual(
            xml.find('devices/disk[@device="cdrom"]/source').get('file'),
            '/var/images/alpine.iso'
        )
        self.assertEqual(xml.find('vcpu').text, '2')
        self.assertEqual(xml.find('memory').text, '1024')
