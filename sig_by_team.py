#! /usr/local/bin/python

import signature as sig
from util import export_to_csv

def get_team(data, team):
    team_list = [person for person in data if person['department'] == team]
    return team_list


if __name__ == '__main__':
    all_teams = ['Customer Success', 'Finance & Operations', 'Global Services',
                'Marketing', 'People', 'Product Engineering', 'Product Experience',
                'Sales', 'Strategy']

    while True:
        team_name = input("Which team would you like to change the signature for? \n To see a list of possible entries, type 'list': ")
        if team_name == 'list':
            for i in all_teams:
                print(i)
            continue
        if team_name not in all_teams and team_name != 'list':
            print("sorry, that's not a valid choice. Please try again. ")
        else:
            break
    sig_file = input('Enter the filepath for the signature file you wish to upload. ')
    data = sig.get_bamboo_directory()
    team_list = get_team(data, team_name)

    mobifyers = []
    for person in team_list:
        new_employee = sig.Mobifyer(person, sig_file)
        mobifyers.append(new_employee.__dict__())

    export_to_csv(mobifyers, 'mycsv.csv')

    sig.gam_cmd()

    # import pdb; pdb.set_trace()
