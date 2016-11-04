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
    def test_start_create_stop(self, create_machine):
        self.agent.start()

        connector = Connector('127.0.0.1')
        loop = asyncio.get_event_loop()
        machine = loop.run_until_complete(connector.create_machine(
            'testmachine', 'alpine', 1, 512, 10, 'pkey'))

        self.agent.stop()

        print(machine)
        print(create_machine.called)
