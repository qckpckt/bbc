#! /usr/local/bin/python

import signature as sig
from util import export_to_csv

def get_team(data, team):
    team_list = [person for person in data if person['department'] == team]
    return team_list


if __name__ == '__main__':
    team_name = input("Which Team would you like to change the signature for? \n EXACT NAME ONLY: ")
    data = sig.get_bamboo_directory()
    team_list = get_team(data, team_name)

    mobifyers = []
    for person in team_list:
        new_employee = sig.Mobifyer(person)
        mobifyers.append(new_employee.__dict__())

    export_to_csv(mobifyers, 'mycsv.csv')

    gam_cmd()

    # import pdb; pdb.set_trace()
