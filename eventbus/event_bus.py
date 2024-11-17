from typing import Dict, Any, NamedTuple, Optional


class Event(NamedTuple):
    interface: str
    method: str
    data_kwargs: Dict[str, Any]


class EventBus:
    def __init__(self, config: dict):
        self.config = config
        from .invocation_engine import LocalInvocationEngine
        self.invocation_engine = LocalInvocationEngine(self.config['interfaces'], event_bus=self)

    def on_event(self, interface: str,
                 method: str,
                 kwargs: Optional[Dict[str, Any]] = None):
        if kwargs is None:
            kwargs = {}
        event = Event(interface, method, kwargs)
        return self.invocation_engine.invoke_method_from_event(event)

    def __call__(self, interface: str,
                 method: str,
                 kwargs: Optional[Dict[str, Any]] = None):
        return self.on_event(interface, method, kwargs)
