# -*- coding: utf-8 -*-

from clique_connector import Connector
from threading import Event, Thread

from .virtz import Virtz


class Agent:

    def __init__(self):
        self.__connector = None
        self.__virtz = None

        self._start_thread = None
        self._start_disposable = None

    @property
    def connector(self):
        if self.__connector is None:
            self.__connector = Connector('127.0.0.1')

        return self.__connector

    @property
    def virtz(self):
        if self.__virtz is None:
            self.__virtz = Virtz()

        return self.__virtz

    def create_machine(self, name, image, cpu, mem, disc, pkey):
        machine = self.virtz.start(name, image=image, cpu=cpu,
                                   mem=mem, disc=disc)

        return machine

    def _start_listening(self):
        channel_close, \
            observable = self.connector.wait_for_machines(
                            self.create_machine)

        self._start_disposable = observable.subscribe(
            lambda cs: print(cs))

        while not self._start_disposable.is_disposed:
            pass

        channel_close()

    def start(self):
        self.stop()

        self._start_stop_event = Event()

        channel_close, \
            observable = self.connector.wait_for_machines(
                            self.create_machine)

        self._start_thread = Thread(target=self._start_listening)
        self._start_thread.start()

    def stop(self):
        if self._start_disposable is not None:
            self._start_disposable.dispose()

        if self._start_thread is not None:
            self._start_thread.join()
