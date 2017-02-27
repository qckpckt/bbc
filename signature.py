#! /usr/local/bin/python

import json
import os
import subprocess
import re
import sys
from util import export_to_csv

import requests


BAMBOO_TOKEN = os.getenv('BAMBOO_API_KEY')
BAMBOO_API = 'https://api.bamboohr.com/api/gateway.php/mobify/v1/employees/directory'
USE_CELL_API = 'https://api.bamboohr.com/api/gateway.php/mobify/v1/employees/{employee_id}?fields=customIncludemobilephoneonemailsignature?'
DEFAULT_HEADERS = {'Accept': 'application/json'}
HQ_PHONE = '1.604.343.4696'
UK_PHONE = '+44 (0) 1189 000 715'
TEST_USER = 'amyers'
RE_GAM_EMAIL = re.compile('<(.*)>')


def get_bamboo_directory():
    """
    Returns a list of dictionaries with the following schema:

    {
        'workPhoneExtension': '',
        'photoUploaded': boolean,
        'nickname': ,
        'firstName': '',
        'division': '',
        'mobilePhone': '',
        'location': '',
        'displayName': '',
        'canUploadPhoto': 1,
        'workPhone': '',
        'gender': '',
        'workEmail': '',
        'lastName': '',
        'jobTitle': '',
        'department': '',
        'photoUrl': '',
        'skypeUsername': None,
        'twitterFeed': None,
        'linkedIn': None,
        'id': ''
    }
    """
    auth = requests.auth.HTTPBasicAuth(BAMBOO_TOKEN, 'x')
    resp = requests.get(BAMBOO_API, auth=auth, headers = DEFAULT_HEADERS)
    directory = resp.json()
    return directory['employees']


def should_use_cell(employee_id):
    url = USE_CELL_API.format(employee_id=employee_id)
    auth = requests.auth.HTTPBasicAuth(BAMBOO_TOKEN, 'x')
    resp = requests.get(url, auth=auth, headers = DEFAULT_HEADERS)
    reply = resp.json()
    if reply['customIncludemobilephoneonemailsignature?'] is None:
        return False
    return True


def make_NA_phone_number(phone):
    clean_phone = ''.join([c for c in phone if c.isdigit()])
    #removing leading country code
    if len(clean_phone) == 11:
        clean_phone = clean_phone[1:]
    assert(len(clean_phone) == 10)
    area_code = clean_phone[:3]
    first_digits = clean_phone[3:6]
    last_digits = clean_phone[6:]
    return '1.{}.{}.{}'.format(area_code, first_digits, last_digits)


def make_UK_phone_number(phone):
    # 07123456789, +44 (0) 07123456789
    clean_phone = ''.join([c for c in phone if c.isdigit()])
    # removing leading country code
    if len(clean_phone) > 10:
        clean_phone = clean_phone[-10:]
    assert(len(clean_phone) == 10)
    part_1 = clean_phone[:4]
    part_2 = clean_phone[4:7]
    part_3 = clean_phone[7:]
    return '+44 (0) {} {} {}'.format(part_1, part_2, part_3)


def make_phone_number(phone, location):
    default_phone = UK_PHONE if location == 'UK' else HQ_PHONE
    f_phone_parse = make_UK_phone_number if location == 'UK' else make_NA_phone_number
    try:
        p = f_phone_parse(phone)
    except AssertionError as e:
        p = default_phone
    return p


def is_valid_mobile(user_information):
    if user_information['mobilePhone']:
        test = make_phone_number(user_information['mobilePhone'],
                                 user_information['location'])
        return test not in [HQ_PHONE, UK_PHONE]
    return False


def gen_twitter(twitterFeed):
    if twitterFeed == '' or twitterFeed is None:
        twitterFeed = 'mobify'
    if twitterFeed.startswith('@'):
        twitterFeed = twitterFeed[1:]
    base = '<a href="https://twitter.com/{twitter_name}" style="text-decoration:underline!important;color:#000000!important;">@{twitter_name}</a>'
    return base.format(twitter_name=twitterFeed)


def make_contact_line(user_information):
    contact_line_parts = ['<a href="http://www.mobify.com/&amp;utm_medium=Email&amp;utm_campaign=email-signature" style="text-decoration:underline; color: #000000 !important;">mobify.com</a>',]
    location = user_information['location']

    phone = HQ_PHONE

    if user_information['location'] == 'UK':
        phone = UK_PHONE

    if user_information['workPhone']:
        clean_phone = make_phone_number(user_information['workPhone'],location)
        phone = 'D {}'.format(clean_phone)
    ext = user_information['workPhoneExtension']

    if ext and ext.isdigit():
        phone += ' ext.{workPhoneExtension}'.format(**user_information)

    contact_line_parts.append(phone)

    if user_information['mobilePhone'] and is_valid_mobile(user_information) and should_use_cell(user_information['id']):
        clean_mobile_phone = make_phone_number(user_information['mobilePhone'],
                                               location)
        contact_line_parts.append('M {}'.format(clean_mobile_phone))

    contact_line_parts.append(gen_twitter(user_information['twitterFeed']))

    return ' | '.join(contact_line_parts)


def merge_signature(user_information, template):
    user_information['contact_line'] = make_contact_line(user_information)
    return template.format(**user_information)


def save_temp_signature(user_name, signature):
    # Returns generated filename
    fname = '/tmp/{}.html'.format(user_name)
    with open(fname, 'wb') as f:
        #must remove new lines or extra breaks are inserted
        f.write(signature.replace('\n', '').encode('utf-8'))
    return fname


def gam_cmd():
    command = ['python', 'lib/GAM-3.71/src/gam.py', 'csv', 'mycsv.csv',
              'gam', 'user', '~name', 'signature', 'file', '~sendas']
    ret = subprocess.run(command)
    print(ret)
    if ret.returncode != 0:
        print('failed to upload signatures!')


def get_sendas(employee):
    # returns text file with sendas info for each employee
    command = ['python', 'lib/GAM-3.71/src/gam.py', 'user',
               employee,'show', 'sendas']
    ret = subprocess.run(command)
    output = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0].decode()
    return output

def find_sendas_email(sendas):
    # searches through output of get_sendas and finds the line containing
    # the default sendas email address, then extracts the email from the line
    # using regex
    for line in sendas.split('\n'):
        if 'SendAs Address:' in line:
            sendas_email = RE_GAM_EMAIL.search(line).groups(1)[0]
        if 'Default: True' in line:
            return sendas_email

class Mobifyer:

    def __init__(self, directory_record, signature_template):
        with open (signature_template) as f:
            template = f.read()
        self.name = get_user_name(directory_record)
        print('username is {}'.format(self.name))
        self.sendas = get_sendas(self.name)
        self.sendas_email = find_sendas_email(self.sendas)
        print('sendas address is {}'.format(self.sendas_email))
        self.signature = merge_signature(directory_record, template)
        self.sig_file = save_temp_signature(self.name, self.signature)
        print('signature filepath is {}'.format(self.sig_file))

    def __dict__(self):
        return {
            'name': self.sendas_email,
            'sendas': self.sig_file
        }

def get_user_name(employee):
    # employee here is the parsed employee record from bamboo.
    email = employee['workEmail']
    return email.split('@')[0]

if __name__ == '__main__':
    directory = get_bamboo_directory()
    mobifyers = []
    for employee in directory:
        new_employee = Mobifyer(employee, 'template1.html')
        mobifyers.append(new_employee.__dict__())

    export_to_csv(mobifyers, 'mycsv.csv')

    gam_cmd()
