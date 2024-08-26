"""Main code body"""
import requests
import json
import os
from datetime import datetime
from copy import deepcopy
import google.auth
from google.cloud import secretmanager_v1
from  google.cloud import bigquery
from  object_model import (
    fflOwner,
    fflPlayer,
    fflTeam
)
    
def populate_objects() -> dict:
    """Populate objects into dict

    Returns:
        dict: dict of ffl Team Objects
    """
    
    secret_val = get_secret("projects/575591763219/secrets/FFL_League_Credentials/versions/latest")
    swid=secret_val["SWID"]
    espn_s2 = secret_val["ESPN_S2"]
    season="2024"
    api_url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leagues/612662"
    
    # espn_s2 = os.getenv("ESPN_S2")
    # swid = os.getenv("SWID")
    
    request_params = [
        'mRoster',
        'mTeam',
        'mSettings',
        'mPendingTransactions',
        'mMatchupScore',
        'mScoreboard',
        'mStatus'
    ]

    full_request = [("view",param) for param in request_params]
    response = requests.get(api_url,
        cookies={'swid': swid,
                    'espn_s2': espn_s2},
        params=full_request, timeout=60
        )

    data = json.loads(response.text)
    response_teams = data['teams']
    response_members = data['members']
    response_draft_details = data['draftDetail']
    draft_status = response_draft_details['drafted']
    ffl_teams = {}
    ffl_owners = {}
    for member in response_members:
        ffl_owners[member["id"]]=fflOwner(member["id"],member["firstName"],member["lastName"])
    for team in response_teams:
        curr_team = ffl_teams[team["id"]] = fflTeam(team["name"],team["id"],team["divisionId"],ffl_owners[team["primaryOwner"]])
        for player in team["roster"]["entries"]:
            player_details = player['playerPoolEntry']['player']
            curr_team.add_player(
                fflPlayer(
                    player_details['fullName'],
                    player_details["id"],
                    player_details["seasonOutlook"] if "seasonOutlook" in player_details else "",
                    player_details["defaultPositionId"],
                    player["lineupSlotId"],
                    max(player['playerPoolEntry']["keeperValue"] if not draft_status else player['playerPoolEntry']["keeperValueFuture"],1),
                    player_details["injured"],
                    player["acquisitionDate"],
                    player["acquisitionType"],
                    player_details["proTeamId"]
                ))
    return ffl_teams

def get_secret(secret_name:str) -> dict:
    """_summary_

    Args:
        secret_name (str): Full Resource name of secret, including version

    Returns:
        dict: value of secret, loaded to dict
    """

    client = secretmanager_v1.SecretManagerServiceClient()

    # Initialize request argument(s)
    request = secretmanager_v1.AccessSecretVersionRequest(
        name=secret_name,
    )

    # Make the request
    response = client.access_secret_version(request=request).payload.data.decode('utf-8')

    # Handle the response
    try:
        return json.loads(response)
    except:
        print("Error loading secret")
        return {}

def create_json(team:fflTeam) -> str:
    """Creates csv data from teams dict

    Args:
        teams (dict): dict of FFL Teams objects
        
    Retunrs:
        str: new-line delimited csv to upload to BQ
    """
    base_list = {
        "Owner_Name":team.owner.full_name,
        "Team_Name":team.team_name,
        "Division_Name":team.division_name,
        "Division_ID":team.division_id,
        "Team_Number":team.team_number,
        "Load_Date":datetime.today().strftime('%Y-%m-%d')
    }
    team_data = list()
    for player in team.players:
        temp_base = deepcopy(base_list)
        player_data = {
            "Player_Name":player.name,
            "Player_Message":player.message,
            "Player_Position":player.player_position,
            "Player_Lineup_Position":player.lineup_position,
            "Player_Salary":player.salary,
            "Injured":player.injured,
            "Acquisition_Type":player.acquisition_type,
            "Acquisition_Date":player.acquisition_date,
            "Pro_Team_ID":player.pro_team_id
        }
        team_data.append(json.dumps(temp_base|player_data))
    return team_data
    
def load_teams_to_bq(
    csvdata:str,
    project_id:str,
    dataset_id:str,
    table_id:str
) -> str:
    """Uploads data to bigquery table

    Args:
        csvdata (str): Parsed Data from Fantasy league
        projectId (str): Google Cloud Project ID
        datasetId (str): Bigquery dataset
        tableId (str): BigQuery table ID

    Returns:
        str: Status of upload
    """
    
    credentials, project = google.auth.default(
            scopes=[
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/bigquery",
            ]
        )

    bq_client = bigquery.Client(
            credentials=credentials, project=project_id
        )
    
    ffl_dataset = bq_client.dataset(dataset_id,project_id)
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
        "Acquisition_Date":"STRING",
        "Pro_Team_ID":"INT64"
    }
    for field,datatype in fields.items():
        schema.append(bigquery.SchemaField(field,datatype))
    table = bigquery.Table(table_ref,schema)
    table.time_partitioning = bigquery.TimePartitioning(    
        type_=bigquery.TimePartitioningType.DAY,
        field="Load_Date"
    )
    
    
    try:
        bq_client.create_table(table)
    except:
        bq_client.update_table(table,["schema"])
        print("already exists")
    load_job_config = bigquery.LoadJobConfig()
    
    load_job_config.schema = schema
    load_job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
    load_job_config.create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED
    load_job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    load_job = bq_client.load_table_from_file(csvdata,table_partition_ref,job_config = load_job_config)

    load_job_status = load_job.result()
    return load_job_status.done()
    

