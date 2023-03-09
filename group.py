import datetime
import redis

rg = redis.Redis(db=1)
rm = redis.Redis(db=2)

class group:
    def __init__(self, g_name:str, creator, desc:str, created_at = datetime.datetime.now().replace(microsecond=0).isoformat(sep='-')):
        if rg.exists(g_name):
            raise ValueError('ERROR: The name has been used. You should choose a unique name')
        else:
            self.name = g_name
            self.owner = creator
            self.desc = desc
            self.created_at = created_at
            self.member_id = [creator.id]
    
    def to_dict(self):
        dict = {
                "creator" : self.owner.id,
                "desc" : self.desc,
                "created_at" : self.created_at,
                "members": {x:str(rm.get(x)) for x in self.member_id},
                "message": {}
        }
        return dict