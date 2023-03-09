import datetime
import uuid

class message:
    def __init__(self,sender, text:str, g_name:str, time = datetime.datetime.now().replace(microsecond=0).isoformat(sep='-')):
        self.id = str(uuid.uuid1())
        self.sender = sender
        self.time = time
        self.text = text
        self.group = g_name

    def to_keyval(self):
        """
        This Method returns the key as the first parameter and the value(message text) as the second one
        """
        return  f"{self.group}-{self.sender.name}-{self.time}", self.text