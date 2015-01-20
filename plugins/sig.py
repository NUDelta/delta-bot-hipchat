from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

sigs = [ ["KevinChen"],
["YongsungKim2", "StephenChan", "nicole", "ShanaAzria", "HaoqiZhang"],
["JoshHibschman", "BenRothman", "AlexHollenbeck", "PhilipHouse", "HaoqiZhang"],
["CoreyGrief", "KevinChen", "KalinaSilverman", "HaoqiZhang"],
["FrankAvino", "ScottCambo", "LeeshaMaliakal", "ChristinaKim", "HaoqiZhang"] ]

members = ["YongsungKim2", "StephenChan", "nicole", "ShanaAzria", "HaoqiZhang",
"JoshHibschman", "BenRothman", "AlexHollenbeck", "PhilipHouse",
"CoreyGrief", "KevinChen", "KalinaSilverman",
"FrankAvino", "ScottCambo", "LeeshaMaliakal", "ChristinaKim"]

class SIGPlugin(WillPlugin):

    @hear("@sig(?P<signum>\d) (?P<text>.*)")
    def message_sig(self, message, signum, text):
        """@sig__ ____: I can message everyone in each Special Interest Group for you!""" 
        for i in sigs[int(signum)]:
            print self.available_rooms
            self.say("@{0} From @{1}: {2}".format(i, message.sender.nick, text), message=message)


