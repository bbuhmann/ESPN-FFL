'''Objects used during process'''
from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True)
class fflOwner():
    id:str
    first_name:str
    last_name:str
    full_name:str = ""
    
    def __post_init__(self):
        self.full_name = f"{self.first_name} {self.last_name}"
    
@dataclass(slots=True)   
class fflPlayer():
    name:str
    id:str
    message:str
    player_position_id:str
    lineup_position_id:str
    salary:int
    injured:bool
    acquisition_unix:int
    acquisition_type:str
    acquistion_date:str = None
    player_position:str = None
    lineup_position:str = None
    
    def __post_init__(self):
        POSITION_MAP = {0: 'QB', 1: 'QB', 2: 'RB', 3: 'WR', 4: 'TE', 5: 'K', 6: 'TE', 7: 'OP', 8: 'DT', 9: 'DE', 10: 'LB', 11: 'DL',12: 'CB', 13: 'S', 14: 'DB', 15: 'DP', 16: 'D/ST',  17: 'K', 18: 'P',  19: 'HC',  20: 'BE',  21: 'IR',  22: '',  23: 'RB/WR/TE',  24: 'ER',  25: 'Rookie', 'QB': 0, 'RB': 2, 'WR': 4, 'TE': 6, 'D/ST': 16, 'K': 17, 'FLEX': 23}
        self.player_position = POSITION_MAP[self.player_position_id]
        self.lineup_position = POSITION_MAP[self.lineup_position_id]
        self.acquistion_date = datetime.utcfromtimestamp(self.acquisition_unix).strftime('%m-%d-%y')
        
    

@dataclass(slots=True)
class fflTeam():
    team_name:str
    team_number:str
    division_id:int
    owner:fflOwner
    division_name:str = None
    players:list(fflPlayer) = list()
    
    def __post_init__(self):
        self.division_name = "Greater Santa Clara Area" if self.division_id==1 else "Norther Lights"
    
    def update_owner(
        self,
        owner
    ):
        """Assigns an owner to the team

        Args:
            owner (_type_): Team Owner object
        """
        self.owner = owner
        
    def add_player(
        self,
        player:fflPlayer
    ):
        self.players.append(player)