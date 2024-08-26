"""Main launching point"""
import io
from fetcher import (
    populate_objects,
    create_json,
    load_teams_to_bq
)

def main(request):
    
    tenderknob_teams = populate_objects()
    teams_csv = list()
    for team in tenderknob_teams.values():
        teams_csv.extend(create_json(team))
    load_job = load_teams_to_bq(io.StringIO("\n".join(teams_csv)),"tenderknob-dynasty-ffl-829734","Tenderknob_Dynasty_FFL","teams_list")
    if load_job:
        return "Success", 200


if __name__ == '__main__':
    main({})