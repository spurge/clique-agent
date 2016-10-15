# -*- coding: utf-8 -*-

from unittest import TestCase

from virtz import Virtz


class TestVirtz(TestCase):

    def setUp(self):
        self.virtz = Virtz()
        self.machine = None

    def tearDown(self):
        try:
            self.machine.destroy()
            self.machine.undefine()
        except:
            pass

        self.virtz.conn.close()

    def test_connection(self):
        self.assertIsNotNone(self.virtz.conn)

    def test_create_and_remove(self):
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

        self.virtz.remove('testmachine')

        try:
            self.virtz.conn.lookupByName('testmachine')
            self.assertFail()
        except:
            pass

    def test_start_and_stop(self):
        self.machine = self.virtz.start('testmachine',
                                   image='alpine',
                                   cpu=1,
                                   mem=512)
        self.assertEqual(self.machine.isActive(), True)

        self.virtz.stop('testmachine')
        self.assertEqual(self.machine.isActive(), False)

    def test_double_start(self):
        self.machine = self.virtz.start('testmachine',
                                   image='alpine',
                                   cpu=1,
                                   mem=512)
        self.assertEqual(self.machine.isActive(), True)

        machine = self.virtz.start('testmachine',
                                   image='alpine',
                                   cpu=1,
                                   mem=512)
        self.assertEqual(machine.isActive(), True)

        self.assertEqual(self.machine.UUIDString(),
                         machine.UUIDString())
