# -*- coding: utf-8 -*-

from unittest import TestCase

from virtz import Virtz


class TestVirtz(TestCase):

    def setUp(self):
        self.virtz = Virtz()
        self.machine = None

    def tearDown(self):
        if self.machine:
            self.machine.undefine()

        self.virtz.conn.close()

    def test_connection(self):
        self.assertIsNotNone(self.virtz.conn)

    def test_start(self):
        self.virtz.start('testmachine', 'alpine', 1, 512)
        self.machine = self.virtz.conn.lookupByName('testmachine')
        self.assertIsNotNone(self.machine)
