# EventBus
A simple pythonic single threaded IOC (inversion of control) library

# Usage example

csv_data.py
```python

# an example of an accessor class
class CsvAccessor:
    def __init__(self, path: str):
        self.path = path
    
    def read_data(self, arg1: int, arg2: int):
        ...
```

__main__.py
```python
from eventbus import EventBus

# initializing the evenBus (IOC)
if __name__ == '__main__':
    # the keys are the names of the interface  
    # the values are the import path of the classes 
    eb = EventBus({'data_interface': 'csv_data.CsvAccessor'})

    # invoking the method
    eb.on_event(interface='data_interface', method='read_data', kwargs={
        'arg1':1, 'arg2':2
    })
    
    # can also invoke via the class directly
    eb(interface='data_interface', method='read_data', kwargs={
        'arg1':1, 'arg2':2
    })
```

# TODO

- add support for interfaces
- add support for secret extraction