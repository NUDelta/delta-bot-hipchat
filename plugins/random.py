from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
from random import randint


class RandomPlugin(WillPlugin):

    @respond_to("roll (?P<num1>\d*) (?P<num2>\d*)")
    def roll(self, message, num1, num2):
    	"""roll ___ ___: I can roll imaginary dice for you!"""
    	if (num2 > num1):
    		self.reply(message, "Your roll: " + str(randint(int(num1), int(num2))))
    	else:
    		self.reply(message, "Your roll: " + str(randint(int(num2), int(num1))))
    
    