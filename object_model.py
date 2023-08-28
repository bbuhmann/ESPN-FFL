'''Objects used during process'''
from dataclasses import dataclass

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
    

@dataclass(slots=True)
class fflTeam():
    team_name:str
    team_number:str
    players:list(fflPlayer) = list()
    owner:fflOwner = None
    
    def assign_owner(
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