from gpiozero import Button
class Non_Standard_Button:
    def __init__(self, button_dict):
        self.address = button_dict['address']
        self.pin = button_dict['pin']
        self.type = button_dict['button_type']
        self.status = 'off' 

    def cycle(self):
        '''this runs when a real hard button is pressed. It overrides the voltage'''
        if self.status == 'on':
            self.status = 'off'
        else:
            self.status = 'on'



    