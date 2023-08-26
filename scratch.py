from dataclasses import dataclass

@dataclass(slots=True)
class fflTeam():
    team_name:str
    team_number:str
    players:list()=None
    owner:str=None
    new_att:str=None
    
    def __post_init__(self):
        self.players = list()
        self.owner = None
        
    def set_new_att(self,new_att):
        self.new_att = new_att

variable = fflTeam('abces','dfsdf')
variable.set_new_att('fdsfd')

print(variable.new_att)
# import json
# import requests

# swid = '{EEC210EE-DAC6-11D2-94E8-0060B067D8ED}'
# espn_s2 = 'AECzbf5PiFkW8NaM6ROQ3eDXVRzDbAXdCLeBxiF%2B6SniGFEEAwChH3EWQXG5vfzMo22bM2WA%2BCItF0FQBS5HJcMXZhPDIDUVZHTTW1cPqeE06cjTFA9ODzu%2F26c%2Bd597ks4Pp6N7fDdqAKHBdv4zefe1Fhw0q53NjlzwC9oXd1Y2nzntcIcuaULkUG68HuDGaHrjZNqrwghuftxdybqbDVNqa37%2BCe4FRtIy744l98r%2FJZun1yoS6jCzwY6CAUno97nIfEjJJ1pwKAEHQz87AQudAs7L%2B2JBR41RrUikW67heg%3D%3D'

# POSITION_MAP = {0: 'QB', 1: 'QB', 2: 'RB', 3: 'WR', 4: 'TE', 5: 'K', 6: 'TE', 7: 'OP', 8: 'DT', 9: 'DE', 10: 'LB', 11: 'DL',12: 'CB', 13: 'S', 14: 'DB', 15: 'DP', 16: 'D/ST',  17: 'K', 18: 'P',  19: 'HC',  20: 'BE',  21: 'IR',  22: '',  23: 'RB/WR/TE',  24: 'ER',  25: 'Rookie', 'QB': 0, 'RB': 2, 'WR': 4, 'TE': 6, 'D/ST': 16, 'K': 17, 'FLEX': 23}
# TEAM_NAMES = {1: 'Burlingame Bad Deals', 2: 'Fall City Hairy Backfield', 3: 'Bellevue LFGs', 4: 'Freeman Balls', 5: 'Half Chubb', 6: 'Stuck Up Hunts', 7: 'North Beach Mobsters', 8: 'Chicago Homers', 9: 'Crazy Rich Asian', 10: 'Oakland Hills Hacks'}
# TEAM_OWNERS = {1: 'Ben Shapiro', 2: 'Adam Grossman', 3: 'Jason LeeKeenan', 4: 'Brendan Buhmann', 5: 'Mike Blais', 6: 'Dave Karol', 7: 'Jordan Koene', 8: 'Nate Lyman', 9: 'Yi-Jau Ku', 10: 'Doug Bell'}

# request_params = [
#     'mRoster',
#     'mTeam'
# ]

# full_request = [("view",param) for param in request_params]
# api_url = "http://fantasy.espn.com/apis/v3/games/ffl/seasons/2023/segments/0/leagues/612662"

# response = requests.get(api_url,
#     cookies={'swid': swid,
#                 'espn_s2': espn_s2},
#     params=full_request, timeout=60
#     )

# new_file = open('tmp/mTeamRoster.json','w',encoding='utf-8')
# new_file.write(json.dumps(json.loads(response.text), indent=2))
# new_file.close()

# for param in request_params:

#     response = requests.get(api_url,
#         cookies={'swid': swid,
#                     'espn_s2': espn_s2},
#         params={'view': param}, timeout=60
#         )

#     new_file = open(f'tmp/{param}.json','w',encoding='utf-8')
#     new_file.write(json.dumps(json.loads(response.text), indent=2))
#     new_file.close()
