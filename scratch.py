"""Main code body"""
import requests
import json
from datetime import datetime
from copy import deepcopy
import io
import google.auth
from  google.cloud import bigquery
from  object_model import (
    fflOwner,
    fflPlayer,
    fflTeam
)

projectId="tenderknob-dynasty-ffl-829734"
dataset_id = "Tenderknob_Dynasty_FFL"
table_id = "teams_list"
credentials, project = google.auth.default(
        scopes=[
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/bigquery",
        ]
    )

bq_client = bigquery.Client(
        credentials=credentials, project=project
    )

ffl_dataset = bq_client.dataset(dataset_id,projectId)
table_partition_ref = bigquery.TableReference(ffl_dataset,f"{table_id}${datetime.today().strftime('%Y%m%d')}")
table_ref = bigquery.TableReference(ffl_dataset,table_id)
schema = list()
fields = {
    "Owner_Name":"STRING",
    "Team_Name":"STRING",
    "Division_Name":"STRING",
    "Division_ID":"STRING",
    "Team_Number":"STRING",
    "Load_Date":"DATE",
    "Player_Name":"STRING",
    "Player_Message":"STRING",
    "Player_Position":"STRING",
    "Player_Lineup_Position":"STRING",
    "Player_Salary":"INT64",
    "Injured":"Boolean",
    "Acquisition_Type":"STRING",
    "Acquisition_Date":"STRING"
}
for field,datatype in fields.items():
    schema.append(bigquery.SchemaField(field,datatype))

table = bigquery.Table(table_ref,schema)


bq_client.create_table(table)

# import json
# import requests

# swid = '{EEC210EE-DAC6-11D2-94E8-0060B067D8ED}'
# espn_s2 = 'AECzbf5PiFkW8NaM6ROQ3eDXVRzDbAXdCLeBxiF%2B6SniGFEEAwChH3EWQXG5vfzMo22bM2WA%2BCItF0FQBS5HJcMXZhPDIDUVZHTTW1cPqeE06cjTFA9ODzu%2F26c%2Bd597ks4Pp6N7fDdqAKHBdv4zefe1Fhw0q53NjlzwC9oXd1Y2nzntcIcuaULkUG68HuDGaHrjZNqrwghuftxdybqbDVNqa37%2BCe4FRtIy744l98r%2FJZun1yoS6jCzwY6CAUno97nIfEjJJ1pwKAEHQz87AQudAs7L%2B2JBR41RrUikW67heg%3D%3D'

# POSITION_MAP = {0: 'QB', 1: 'QB', 2: 'RB', 3: 'WR', 4: 'TE', 5: 'K', 6: 'TE', 7: 'OP', 8: 'DT', 9: 'DE', 10: 'LB', 11: 'DL',12: 'CB', 13: 'S', 14: 'DB', 15: 'DP', 16: 'D/ST',  17: 'K', 18: 'P',  19: 'HC',  20: 'BE',  21: 'IR',  22: '',  23: 'RB/WR/TE',  24: 'ER',  25: 'Rookie', 'QB': 0, 'RB': 2, 'WR': 4, 'TE': 6, 'D/ST': 16, 'K': 17, 'FLEX': 23}
# TEAM_NAMES = {1: 'Burlingame Bad Deals', 2: 'Fall City Hairy Backfield', 3: 'Bellevue LFGs', 4: 'Freeman Balls', 5: 'Half Chubb', 6: 'Stuck Up Hunts', 7: 'North Beach Mobsters', 8: 'Chicago Homers', 9: 'Crazy Rich Asian', 10: 'Oakland Hills Hacks'}
# TEAM_OWNERS = {1: 'Ben Shapiro', 2: 'Adam Grossman', 3: 'Jason LeeKeenan', 4: 'Brendan Buhmann', 5: 'Mike Blais', 6: 'Dave Karol', 7: 'Jordan Koene', 8: 'Nate Lyman', 9: 'Yi-Jau Ku', 10: 'Doug Bell'}

# request_params = [
#     'mRoster',
#     'mTeam',
#     'mSettings',
#     'mPendingTransactions',
#     'mMatchupScore',
#     'mScoreboard',
#     'mStatus'
# ]

# full_request = [("view",param) for param in request_params]
# api_url = "http://fantasy.espn.com/apis/v3/games/ffl/seasons/2023/segments/0/leagues/612662"

# response = requests.get(api_url,
#     cookies={'swid': swid,
#                 'espn_s2': espn_s2},
#     params=full_request, timeout=60
#     )

# new_file = open('mConsolidated.json','w',encoding='utf-8')
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
