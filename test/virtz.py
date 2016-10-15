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

    def test_create(self):
        machine = self.virtz.create('testmachine',
                                    image='alpine',
                                    cpu=1,
                                    mem=512)
        self.assertIsNotNone(machine)

        self.machine = self.virtz.conn.lookupByName('testmachine')
        self.assertEqual(self.machine.UUIDString(),
                         machine.UUIDString())

        # Shall be able to create it twice
        self.machine = self.virtz.create('testmachine',
                                         image='alpine',
                                         cpu=1,
                                         mem=512)
        self.assertIsNotNone(self.machine)
        self.assertNotEqual(self.machine.UUIDString(),
                            machine.UUIDString())

    def test_remove(self):
        self.virtz.remove('testmachine')

        try:
            self.virtz.conn.lookupByName('testmachine')
            self.assertFail()
        except:
            pass

    def test_start(self):
        machine = self.virtz.start('testmachine',
                                   image='alpine',
                                   cpu=1,
                                   mem=512)
        self.assertIsNotNone(self.machine.UUIDString(), machine.UUIDString())

    def test_stop(self):
        self.virtz.stop('testmachine')
