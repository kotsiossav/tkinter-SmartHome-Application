
#TASK 1/2#
class SmartDevice:
    def __init__(self):
        self._switched_on=False

    @property
    def switched_on(self):
        return self._switched_on
    
    @switched_on.setter
    def switched_on(self,power):
        self._switched_on=power
    
    def toggle_switch(self):
        self._switched_on= not self._switched_on

class SmartPlug(SmartDevice):

    def __init__(self,consumption_rate):
        super().__init__()
        if not isinstance(consumption_rate, (int, float)):
            raise TypeError("Consumption rate must be a number.")
        if not (0 <= consumption_rate <= 150):
            raise ValueError("Consumption rate must be between 0 and 150 watts.")
        self._consumption_rate = consumption_rate

    @property
    def consumption_rate(self):
        return self._consumption_rate
        
    
    @consumption_rate.setter
    def consumption_rate(self,rate):
        if not isinstance(rate, (int, float)):
            raise TypeError("Consumption rate must be a number.")
        elif not (0 <= rate <= 150):
            raise ValueError("Consumption rate must be between 0 and 150 watts.")
        else:
            self._consumption_rate = rate
        

    def __str__(self):
        if self._switched_on==True:
            output=f"SmartPlug is on with a consumption rate of {self.consumption_rate}"
        else:
            output=f"SmartPlug is off with a consumption rate of {self.consumption_rate}"
        return output
    
class SmartLight(SmartDevice):

    def __init__(self):
        super().__init__()
        self._brightness=50
    
    @property
    def brightness(self):
        return self._brightness
    
    @brightness.setter
    def brightness(self,new_bright):
        if not isinstance(new_bright, (int, float)):
            raise TypeError("Brightness must be a number.")
        if not (0 <= new_bright <= 100):
            raise ValueError("Brightness must be between 0 and 100.")
        else:
            self._brightness=new_bright

    def __str__(self):
        if self._switched_on==True:
            output=f"SmartLight is on with brightness of {self.brightness}"
        else:
            output=f"SmartLight is off with brightness of {self.brightness}"
        return output


class SmartTV(SmartDevice):

    def __init__(self):
        super().__init__()
        self._channel=1

    @property
    def channel(self):
        return self._channel
    
    @channel.setter
    def channel(self,new_chan):
        if not isinstance(new_chan, (int, float)):
            raise TypeError("Channel must be a number.")
        if not (1 <= new_chan <= 734):
            raise ValueError("Channel values must be between 1 and 734.")
        
        self._channel = new_chan

    def __str__(self):
        if self._switched_on==True:
            output=f"SmartTV is on and the channel is {self.channel}"
        else:
            output=f"SmartTV is off and the channel is {self.channel}"
        return output

# TASK 3#
class SmartHome:
    accepted_devices = [SmartPlug, SmartLight, SmartTV] 

    def __init__(self):
        self.devices=[]
        self.amount=0
        self.devices_on=0
        self.max_items=3

    def add_device(self, device):
        if self.amount >= self.max_items:
            raise ValueError("Maximum number of devices reached. Cannot add device.")
        elif not isinstance(device, tuple(self.accepted_devices)):
            raise TypeError("Invalid device type. Please add a valid Smart Device.")
        else:  
            self.devices.append(device)
            self.amount += 1

    def remove_device(self,index):
        if index>=0 and index<len(self.devices):
            del self.devices[index]
            self.amount-=1
        else:
            print(f"The index you inputted does not exist.Please try using between 0 and {len(self.devices)-1}.")

    def get_device(self,index):
        if index>=0 and index<len(self.devices):
            return self.devices[index]
        else:
            print(f"The index you inputted does not exist.Please try using between 0 and {len(self.devices)-1}.")

    def toggle_device(self,index):
        if index>=0 and index<len(self.devices):
            self.devices[index].toggle_switch()
    
    def update_option(self,index,value):
        device = self.get_device(index)
        try:
            if isinstance(device, SmartPlug) and 0 <= value <= 150:
                device.consumption_rate = value
            elif isinstance(device, SmartLight) and 0 <= value <= 100:
                device.brightness = value
            elif isinstance(device, SmartTV) and 1 <= value <= 734:
                device.channel = value
            else:
                raise ValueError("Invalid value for the selected device.")
        except TypeError:
            raise TypeError("Invalid input: Value must be a number.")
        


    def switch_all_on(self):
        for device in self.devices:
            if not device.switched_on: 
                device.toggle_switch()

    def switch_all_off(self):
        for device in self.devices:
            if device.switched_on: 
                device.toggle_switch()

    def get_num_devices(self):
        return self.amount

    def __str__(self):
        index=1
        output=f"SmartHome with {self.amount} device(s) \n"
        for device in self.devices:
            output+=f"{index}- {device} \n"
            index+=1
        return output


       

#TEST FUNCTION FOR TASK 1#
def test_smart_plug():
    plug=SmartPlug(45)
    print(plug)
    plug.toggle_switch()
    print(plug)
    plug.consumption_rate=75
    print(plug)
    plug.toggle_switch()
    print(plug)
    try:
        plug.consumption_rate=-10
        print(plug)
        plug.consumption_rate=200
        print(plug)
    except(ValueError,TypeError) as e:
        print(f"Error: {e}")

    print(plug)

    try:
        plug_2=SmartPlug(-5)
    except(ValueError,TypeError) as e:
        print(f"Error: {e}")
    try:
        plug_3=SmartPlug(-5)
    except(ValueError,TypeError) as e:
        print(f"Error: {e}")
   
    
#TEST FUNCTION FOR TASK 2#
def test_custom_device():
    light=SmartLight()
    tv=SmartTV()
    print(light)
    print(tv)
    light.toggle_switch()
    tv.toggle_switch()
    print(light)
    print(tv)
    light.brightness=80
    tv.channel=200
    print(light)
    print(tv)
    try:
        light.brightness="ertb"
    except(ValueError,TypeError) as e:
        print(f"Error:{e}")
    try:
        tv.channel=-5
    except(ValueError,TypeError) as e:
        print(f"Error:{e}")
    print(light)
    print(tv)


#TEST FUNCTION FOR TASK 3#
def test_smart_home():

    plug = SmartPlug(45)  
    light = SmartLight()  
    tv = SmartTV()        

    # Step 2: Initialize SmartHome and Add Devices
    home = SmartHome()
    home.add_device(plug)
    home.add_device(light)
    home.add_device(tv)
    print(home)

    # Step 3: Retrieve and Verify Devices
    print(home.get_device(0))
    print(home.get_device(1))
    print(home.get_device(2))
    

    # Step 4: Toggle Each Device Individually
    home.toggle_device(0)  
    home.toggle_device(1)  
    home.toggle_device(2)
    print("\n")  
    print(home)

    # Step 5: Switch All On, Then Off
    home.switch_all_on()
    home.switch_all_off()
    print(home)

    # Step 6: Verify max_items limit
    extra_device = SmartPlug(100)  # Extra device
    try:
        home.add_device(extra_device)  # Should be rejected
    except ValueError as e:
        print(f"Error: {e}")

    print(home)

    # Step 7: Update Option Attributes (Valid Updates)
    home.update_option(0, 75) 
    home.update_option(1, 80) 
    home.update_option(2, 300)  
    print(home)

    # Step 8: Attempt Invalid Updates
    try:
        home.update_option(0, 200)  
    except (ValueError,TypeError) as e:
        print(f"Error: {e}")
    try:
        home.update_option(2,-200)  
    except (ValueError,TypeError) as e:
        print(f"Error: {e}")
    try:
        home.update_option(2,"ever" ) 
    except (ValueError,TypeError) as e:
        print(f"Error: {e}")

    # Step 9: Remove Devices
    home.remove_device(0)  
    print("\n")
    print(home)
    # Step 10: Attempt Invalid Removals
    home.remove_device(-1)
    # Step 11: Final SmartHome State
    print(home)


test_smart_plug()

