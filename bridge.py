class Device:
    def turn_on(self):
        pass
    
    def turn_off(self):
        pass

class TV(Device):
    def turn_on(self):
        print("TV is ON")
    
    def turn_off(self):
        print("TV is OFF")

class RemoteControl:
    def __init__(self, device: Device):
        self.device = device
    
    def press_power(self):
        print("Pressing power button...")
        self.device.turn_on() if isinstance(self.device, TV) else self.device.turn_off()

remote = RemoteControl(TV())
remote.press_power()