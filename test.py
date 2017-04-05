#! /usr/local/bin/python

import signature as sig
from util import export_to_csv

def first(iterator, condition=None):
    # lambda function used above in finding specific users
    condition = (condition or (lambda x: True))
    return next ((x for x in iterator if condition(x)))

def get_employee(data):
    while True:
        empl_id = input('Enter the Bamboo ID of the employee you want to set the signature for. ')
        try:
            employee = first(data, condition = lambda x: x['id'] == empl_id)
        except StopIteration as s:
            print('No employee exists for that ID. Please try again. ')
        return employee

def should_set_sig():
    answers = ['yes', 'no']
    while True:
        user_in = input('Do you wish to upload this signature file? Answer "yes" or "no": ')
        if user_in not in answers:
            print('Sorry, input not recognised. Answer "yes" or "no": ')
        if user_in == 'yes':
            sig.gam_cmd()
        else:
            break

if __name__ == '__main__':
    sig_file = input('Enter the filepath for the signature file you wish to upload. ')
    data = sig.get_bamboo_directory()
    employee = get_employee(data)
    sig_list = []
    set_signature = sig.Mobifyer(employee, sig_file)
    sig_list.append(set_signature.__dict__())

    export_to_csv(sig_list, 'mycsv.csv')

    should_set_sig()
