class EuropeanPlug:
    def connect_to_eu_socket(self):
        return "Connected to EU socket"

class USPlug:
    def connect_to_us_socket(self):
        return "Connected to US socket"

class Adapter:
    def __init__(self, plug: EuropeanPlug):
        self.plug = plug
    
    def connect_to_us_socket(self):
        return self.plug.connect_to_eu_socket() + " via adapter"

adapter = Adapter(EuropeanPlug())
print(adapter.connect_to_us_socket())