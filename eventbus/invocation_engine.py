import logging
import pydoc
from typing import Union, Dict, Any

from .event_bus import EventBus, Event

logger = logging.getLogger(__name__)


class LocalInvocationEngine:
    def __init__(self, interfaces_dict: Dict[str, Dict[str, Union[str, dict]]], *, event_bus: EventBus):
        self.__interfaces_dict = interfaces_dict
        self.interfaces: Dict[str, Any] = {}
        self.__event_bus = event_bus
        self.load_classes()

    def load_classes(self):
        for interface_name, interface_details in self.__interfaces_dict.items():
            self.interfaces[interface_name] = self.__create_interface_instance(interface_details)

    def __create_interface_instance(self, interface_details: Dict[str, Any]):
        klass = pydoc.locate(interface_details['type'])  # import the class
        if klass is None:
            raise ValueError(f'cant load {interface_details["type"]}, no such class or function')
        klass_instance = klass(  # noqa
            **interface_details['kwargs'], event_bus=self.__event_bus
        )
        return klass_instance

    def invoke_method_from_event(self, event: Event):
        interface = self.interfaces[event.interface]
        try:
            invocation_method = getattr(interface, event.method)
            returned_data = invocation_method(**event.data_kwargs)
            return returned_data
        except Exception as e:
            logger.exception(f'and execution was raised for the method {event.method} in the class {interface} '
                             f'\n {e}')
