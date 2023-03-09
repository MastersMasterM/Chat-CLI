from group import group
from message import message
import redis
import json

rg = redis.Redis(db=1)
rm = redis.Redis(db=2)
rmes = redis.Redis(db=3)

class member:
    def __init__ (self, name:str, username:str):
        self.id = username #Username Should Be Unique
        self.name = name
        self.group = {}
    
    def create_group(self,g_name,desc):
        g = group(g_name,self,desc)
        if rg.set(g.name, json.dumps(g.to_dict())):
            self.group[g_name] = self.id
            self.to_redis()
            print(f"{g_name} Created")
    
    def join_group(self,g_name):
        if rg.exists(g_name):
            gr = json.loads(rg.get(g_name))
            gr["members"][self.id] = self.name
            rg.delete(g_name)
            if rg.set(g_name,json.dumps(gr)):
                self.group[g_name] = self.id
                self.to_redis()
                print(f"You added to {g_name}")
        else:
            print("Such a group doesn't exist")

    def send(self,t_message:str,s_group):
        m = message(self,t_message,s_group)
        key, val = m.to_keyval()
        rmes.set(key,val)
        gr = json.loads(rg.get(s_group))
        gr["message"][m.id] = {
            "sender" : m.sender.id,
            "sent_at" : m.time,
            "text" : m.text
            }
        rg.delete(s_group)
        rg.set(s_group,json.dumps(gr))


    def to_redis(self):
        dic = {
            "name" : self.name,
            "groups" : self.group
        }
        if rm.set(str(self.id),json.dumps(dic)):
            print(f"{self.name} added to the app")
        else:
            print("Cannot connect to the DB")

    def leave_group(self,s_group):
        del self.group[s_group]
        gr = json.loads(rg.get(s_group))
        del gr["members"][self.id]
        if rg.set(s_group,json.dumps(gr)):
            print(f"{self.name} left {s_group}")