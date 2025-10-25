from backend import SmartHome, SmartPlug, SmartLight, SmartTV
from tkinter import Tk, Frame, Button, Label, StringVar,Entry,IntVar,Toplevel
import csv
import os


class SmartHomeApp():
    
     
    def __init__(self,home,win_type):
        self.home=home
        self.win = win_type
        self.win.title("Smart Home App")
        self.win.geometry("450x200")
        self.main_frame = Frame(self.win)
        self.main_frame.pack(padx=5, pady=5)
        
        self.home_widgets = []
        self.new_value = StringVar()
        self.value_error_message = StringVar()
        self.value_error_message.set("")
        self.amount_error_message = StringVar()
        self.amount_error_message.set("")
        
    def create_widgets(self):
        self.delete_all_widgets()
        all_on=Button(self.main_frame,text="Turn all on",command=self.turn_all_on)
        all_on.grid(column=0,row=0,padx=30,pady=5)

        all_off=Button(self.main_frame,text="Turn all off",command=self.turn_all_off)
        all_off.grid(column=1,row=0,padx=30,pady=5)
        
        amount=self.home.get_num_devices()

        for i in range(amount):
            device = self.home.get_device(i)
            if type(device)==SmartLight:
                toggle_text = f"Light: {'on' if device.switched_on==True else 'off'} ,"
                level_text = f"Brightness: {device.brightness}"
            elif type(device)==SmartTV:
                toggle_text = f"TV: {'on' if device.switched_on==True else 'off'} ,"
                level_text = f"Channel: {device.channel}"
            elif type(device)==SmartPlug:
                toggle_text = f"Plug: {'on' if device.switched_on==True else 'off'} ,"
                level_text = f"Consumption: {device.consumption_rate}"
        

            toggle_label = Label(self.main_frame, text=toggle_text)
            toggle_label.grid(row=i+1, column=0, padx=2, pady=2)
            self.home_widgets.append(toggle_label)


            level_label = Label(self.main_frame, text=level_text)
            level_label.grid(row=i+1, column=1, padx=2, pady=2)
            self.home_widgets.append(level_label)

            toggle_button = Button(self.main_frame, text="Toggle",command=lambda index=i: self.toggle_device(index))
            toggle_button.grid(row=i+1, column=2, padx=2, pady=5)
            self.home_widgets.append(toggle_button) 

            edit_button = Button(self.main_frame, text="Edit",command=lambda index=i: self.edit_device(index))
            edit_button.grid(row=i+1, column=3, padx=2, pady=2)
            self.home_widgets.append(edit_button)

            del_button = Button(self.main_frame, text="Delete",command=lambda index=i: self.delete_device(index))
            del_button.grid(row=i+1, column=4, padx=2, pady=2)
            self.home_widgets.append(del_button)

        add_button = Button(self.main_frame, text="Add",command=self.add_device)
        add_button.grid(row=amount+1, column=0, padx=5, pady=2)
        self.home_widgets.append(add_button)

        amount_error_label = Label(self.main_frame, textvariable=self.amount_error_message)
        amount_error_label.grid(row=amount+1, column=1, columnspan=5, pady=5)
        self.home_widgets.append(amount_error_label)

    def turn_all_on(self):
        self.home.switch_all_on()
        self.create_widgets()
        

    def turn_all_off(self):
        self.home.switch_all_off()
        self.create_widgets()

    def toggle_device(self,index):
        self.home.toggle_device(index)
        self.create_widgets()

    def delete_device(self,index):
        self.home.remove_device(index)
        self.amount_error_message.set("")
        self.create_widgets()     

    def delete_all_widgets(self):#used in create widgets so changes are reflected in the GUI
        for widget in self.home_widgets:
            widget.destroy()
        self.home_widgets = []

    def edit_device(self, index):
        device = self.home.get_device(index)
        edit_win = Toplevel(self.win)
        edit_win.title("Edit Device")
        edit_win.geometry("300x150")

    #Label text depends on the device being edited
        if isinstance(device, SmartLight):
            label = Label(edit_win, text="Brightness:")
            self.new_value.set(device.brightness)
            
    
        elif isinstance(device, SmartPlug):
            label = Label(edit_win, text="Consumption Rate:")
            self.new_value.set(device.consumption_rate)
            
    
        elif isinstance(device, SmartTV):
            label = Label(edit_win, text="Channel:")
            self.new_value.set(device.channel)
        
        label.grid(row=0, column=0, padx=5, pady=5)
            
        value_entry = Entry(edit_win, textvariable=self.new_value)
        value_entry.grid(row=0, column=1, padx=5, pady=5)

        save_button = Button(edit_win, text="Save",command=lambda:self.update_device(index, edit_win))
        save_button.grid(row=1, column=0, columnspan=2, pady=10)

        value_error_label = Label(edit_win, textvariable=self.value_error_message)
        value_error_label.grid(row=2, column=0, columnspan=2, pady=5)
        
        

    def update_device(self, index, edit_win):
        try:
            value = int(self.new_value.get())
            self.update_option_in_app(index,value)
            if self.value_error_message.get() == "":
                edit_win.destroy()
                self.create_widgets()
        except (ValueError,TypeError):
            self.value_error_message.set("Please enter a valid number and not text.")


    def add_device(self):
        new_win = Toplevel(self.win)
        new_win.title("Add Device")
        new_win.geometry("300x150")

        label=Label(new_win,text="Choose a device to add:")
        label.grid(row=0,column=0,padx=5,pady=5)

        plug_button=Button(new_win,text="Smart Plug",command=lambda: self.add_new_device(new_win,SmartPlug))
        plug_button.grid(row=1,column=0,padx=5,pady=5)

        light_button=Button(new_win,text="Smart Light",command=lambda: self.add_new_device(new_win,SmartLight))
        light_button.grid(row=2,column=0,padx=5,pady=5)

        tv_button=Button(new_win,text="Smart TV",command=lambda: self.add_new_device(new_win,SmartTV))
        tv_button.grid(row=3,column=0,padx=5,pady=5)

    def add_new_device(self,new_win,DeviceClass):
        if DeviceClass == SmartPlug:
            device = SmartPlug(45)  # Default consumption rate
        elif DeviceClass == SmartLight:
            device = SmartLight()
        elif DeviceClass == SmartTV:
            device = SmartTV()
        
        self.add_device_in_app(device)
        self.create_widgets()
        new_win.destroy()

    def update_option_in_app(self, index, value):
        try:
            device = self.home.get_device(index)  # Retrieve device safely
            if isinstance(device, SmartPlug) and 0 <= value <= 150:
                device.consumption_rate = value
            elif isinstance(device, SmartLight) and 0 <= value <= 100:
                device.brightness = value
            elif isinstance(device, SmartTV) and 1 <= value <= 734:
                device.channel = int(value)  # Ensure integer for channel
            else:
                raise ValueError("Invalid value for the selected device.")
            self.value_error_message.set("")  # Clear error if successful
        except TypeError:
            self.value_error_message.set("Please enter a numeric value.")
        except ValueError as e:
            self.value_error_message.set(str(e))
    
    def add_device_in_app(self, device):
        try:
            self.home.add_device(device)
            self.amount_error_message.set("")  # Clear error if successful
        except ValueError as e:
            self.amount_error_message.set(str(e))  # Show error message
            
    def run(self):
       self.create_widgets()
       self.win.mainloop()


class SmartHomesApp(SmartHome):
    def __init__(self):
        self.homes = []
        self.load_data()
        self.win = Tk()
        self.win.title("Smart Homes App")
        self.win.geometry("450x300")
        self.main_frame = Frame(self.win)
        self.main_frame.pack(padx=5, pady=5)
        self.home_widgets = []
        

    def save_data(self):
        #Saves all homes and their devices to a CSV file.
        file = open("smarthomes.csv", mode="w", newline="")  # Open file for writing
        writer = csv.writer(file)

        for home in self.homes:
            writer.writerow(["HOME"])  # Mark the start of a new home
            for device in home.devices:
                if isinstance(device, SmartPlug):
                    writer.writerow(["SmartPlug", device.consumption_rate, device.switched_on])
                elif isinstance(device, SmartLight):
                    writer.writerow(["SmartLight", device.brightness, device.switched_on])
                elif isinstance(device, SmartTV):
                    writer.writerow(["SmartTV", device.channel, device.switched_on])

        file.close()  # Close file manually

    def load_data(self):
        if os.path.exists("smarthomes.csv"):
            file = open("smarthomes.csv", mode="r")  # Open file for reading
            reader = csv.reader(file)
            for row in reader:
                if row[0] == "HOME":
                    home = SmartHome()
                    self.homes.append(home)
                elif home:
                    device_type, value, switched_on = row[0], int(row[1]), row[2]
                    if device_type == "SmartPlug":
                        device = SmartPlug(value)
                    elif device_type == "SmartLight":
                        device = SmartLight()
                        device.brightness = value
                    elif device_type == "SmartTV":
                        device = SmartTV()
                        device.channel = value
                    if switched_on=="True":
                        device.switched_on=True
                    else:
                        device.switched_on=False
                    
                    
                    home.add_device(device)

            file.close()
        
        

    def add_home(self):
        home = SmartHome()
        self.homes.append(home)
        self.save_data()  # Save immediately
        self.create_widgets()
        
        

    def delete_home(self,index):
        del self.homes[index]
        self.save_data()
        self.create_widgets()
        
        self.save_data()  # Save immediately

    def create_widgets(self):
        self.delete_all_widgets()
        for i in range (len(self.homes)):
            devices_on=0
            home_button = Button(self.main_frame, text=f"Home {i+1}", command=lambda index=i: self.open_home(index))
            home_button.grid(row=i, column=0, padx=5, pady=5)
            self.home_widgets.append(home_button)

            del_button = Button(self.main_frame, text="Delete", command=lambda index=i: self.delete_home(index))
            del_button.grid(row=i, column=1, padx=5, pady=5)
            self.home_widgets.append(del_button)

            info_label = Label(self.main_frame, text=f"Devices: {len(self.homes[i].devices)}")
            info_label.grid(row=i, column=2, padx=5, pady=5)
            self.home_widgets.append(info_label)

            for device in self.homes[i].devices:
                if device.switched_on==True:
                    devices_on+=1

            on_or_off=Label(self.main_frame,text=f"Devices switched on: {devices_on}")
            on_or_off.grid(row=i,column=3,padx=5,pady=5)
            self.home_widgets.append(on_or_off)

        add_button = Button(self.main_frame, text="Add Home", command=self.add_home)
        add_button.grid(row=len(self.homes), column=0, padx=5, pady=5)
        self.home_widgets.append(add_button)


    def delete_all_widgets(self):
        for widget in self.home_widgets:
            widget.destroy()
        self.home_widgets = []

    def open_home(self, index):
        home = self.homes[index]
        app = SmartHomeApp(home,Toplevel())  # Open SmartHomeApp
        app.win.protocol("WM_DELETE_WINDOW",lambda a=app:self.close_win(a))
        app.run()
        self.save_data()
        
    #used to save the changes made in homes as soon as the window closes   
    def close_win(self,app):
        self.save_data()
        self.create_widgets()
        app.win.destroy()
        

    def run(self):
        self.create_widgets()
        self.win.protocol("WM_DELETE_WINDOW", self.on_close)
        self.win.mainloop()

    def on_close(self):
        #Save data before closing the app.
        self.save_data()
        self.win.destroy()
    
    

#TEST FUNCTION FOR TASK 5#
def test_smart_home_system():
    home=SmartHome()
    home.add_device(SmartPlug(45))
    home.add_device(SmartLight())
    home.add_device(SmartTV())
    app=SmartHomeApp(home,Tk())
    print(home)
    app.run()
    print(home)


#TEST FUNCTION FOR CHALLENGE TASK#
def test_smart_homes_system():
    homes = SmartHomesApp()
    homes.run()

test_smart_homes_system()

