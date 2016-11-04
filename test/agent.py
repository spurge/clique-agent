# -*- coding: utf-8 -*-

import asyncio

from unittest import TestCase
from unittest.mock import patch

from clique_agent import Agent
from clique_connector import Connector


class TestAgent(TestCase):

    def setUp(self):
        self.agent = Agent()

    def tearDown(self):
        self.agent.virtz.conn.close()

    @patch('clique_agent.Agent.create_machine')
    @patch('clique_agent.Agent.confirm_machine')
    def test_start_create_stop(self, confirm_machine, create_machine):
        confirm_machine.return_value = True
        create_machine.return_value = dict(host='testhost',
                                           username='some_user')
        self.agent.start()

        connector = Connector('127.0.0.1')
        loop = asyncio.get_event_loop()
        machine = loop.run_until_complete(connector.create_machine(
            'testmachine', 'alpine', 1, 512, 10, 'pkey'))

        self.agent.stop()

        self.assertEqual(machine['host'], 'testhost')
        self.assertEqual(machine['username'], 'some_user')
        self.assertTrue(create_machine.called)
