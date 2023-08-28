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
    player_position:str
    lineup_position:str
    last_week_score:int
    current_week_score:int
    acquisition_unix:int
    acquistion_date:str = None
    
    def __post_init__(self):
        self.acquistion_date = datetime.utcfromtimestamp(self.acquisition_unix).strftime('%m-%d-%y')
    
    def get_position_label(self):
        POSITION_MAP = {0: 'QB', 1: 'QB', 2: 'RB', 3: 'WR', 4: 'TE', 5: 'K', 6: 'TE', 7: 'OP', 8: 'DT', 9: 'DE', 10: 'LB', 11: 'DL',12: 'CB', 13: 'S', 14: 'DB', 15: 'DP', 16: 'D/ST',  17: 'K', 18: 'P',  19: 'HC',  20: 'BE',  21: 'IR',  22: '',  23: 'RB/WR/TE',  24: 'ER',  25: 'Rookie', 'QB': 0, 'RB': 2, 'WR': 4, 'TE': 6, 'D/ST': 16, 'K': 17, 'FLEX': 23}
        return POSITION_MAP[self.player_position]
    

@dataclass(slots=True)
class fflTeam():
    team_name:str
    team_number:str
    owner:fflOwner
    players:list(fflPlayer) = list()
    
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