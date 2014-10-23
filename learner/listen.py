# from will.plugin import WillPlugin
# from will.decorators import hear

# class ListenPlugin(WillPlugin):

# 	def __init__(self):
# 		kb = self.load("knowledge", {})
# 		if (kb == {}):
# 			self.save("knowledge", kb)

# 	@hear("(?P<phrase>.*)")
# 	def learn(self, message, phrase, include_me=False):
# 		if ("kdbot" in phrase):
# 			return

# 		