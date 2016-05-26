#! python2.7

####################################
## Telavox public API Python demo ##
####################################

# Python script to pull down call history from Telavox using the official API
# http://www.telavox.com/sv/developer/documentation/calls/
# WARNING: not guaranteed to be 100% PEP 8-proof

# Copyright (C) 2016  Timesky AB

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#**** Built-in imports ****#
import os, sys
import json

#**** Basic check that 2 arguments are passed ****#
if len(sys.argv) != 3:
	print('Usage: python py_telavox_api_demo.py <extension> <password>')
	sys.exit()
	
#**** Functions ****#
## Install/prompt about module dependencies
def module_update():
	if sys.platform == "win32" or sys.platform == "win64":
		print('''Install/update necessary modules? (y/n)
(You probably want to answer yes if this is your first time running this script)''')
		update_prompt = raw_input()
		if update_prompt.lower() == 'y':
        # Install/update pip and modules
			os.system('py -m pip install -U pip')
			os.system('py -m pip install -U mechanize')
	elif sys.platform == "linux" or sys.platform == "linux2":
		print('''Make sure that you have the following python2 modules installed from your repositories:
- mechanize''')
	else:
		print('''Make sure that you have the following python2 modules installed:
- mechanize''')
	print('Press any key to continue.')
	raw_input()

## Loop through call types
def call_history_loop(call_type):
	total_duration = 0
	print('List of %s calls:' % (call_type))
	tvxapi_call_get = mech_wb.open(tvxapi_call_url)
	tvxapi_call_json = json.load(tvxapi_call_get)
	tvxapi_call_type_json = tvxapi_call_json[call_type]
	nb_calls = len(tvxapi_call_type_json)
	for i in range(nb_calls):
		print('Call %s %s on %s - lasted %d seconds' % (call_status[call_type],
														tvxapi_call_type_json[i]['number'].encode('utf-8'),
														tvxapi_call_type_json[i]['datetime'].encode('utf-8'),
														tvxapi_call_type_json[i]['duration']))
		total_duration += tvxapi_call_type_json[i]['duration']
	
	average_duration = total_duration / nb_calls
	# Print out average call duration for recorded calles, skipping missed ones
	if call_type != 'missed':
		print('Average %s call duration: %d seconds.' % (call_type, average_duration))

## Main function
def main_loop(target_url):
	# Authenticate #
	tvxapi_auth_get = mech_wb.open(target_url)
	tvxapi_auth_json = json.load(tvxapi_auth_get)

	# Check authentication success according to Telavox documentation
	if tvxapi_auth_json['message'] == 'OK':
		print('Login sucessful!')
		print('The latest 30 calls for %s are:' % (tvx_username))

	# List calls - incoming, outgoing, missed
		call_history_loop("incoming")
		call_history_loop("outgoing")
		call_history_loop("missed")

	else:
		print('Login failed with %s' % (tvxapi_auth_json['message']))

	print('Press any key to quit.')
	raw_input()


#**** pip imports ****#
## Run the module_update function first
module_update()
import mechanize

#**** Variables ****#
## Login info
### Username - extension
tvx_username = sys.argv[1]
### Note: passwords accept spaces, however the string is passed as an URL
### Parsing the string accordingly is advised
tvx_pw = sys.argv[2]

## Call status - dictionary to format stdout
call_status = { "incoming": "from", "missed": "missed from", "outgoing": "to"}

## Mechanize Web browser
mech_wb = mechanize.Browser()

## Telavox URLs
base_url = 'https://api.telavox.se/'
tvxapi_auth_url = base_url + 'auth/login?username=' + tvx_username + '&password=' + tvx_pw
tvxapi_call_url = base_url + 'calls'

#**** Getting started ****#
if __name__ == '__main__':
	try:
		main_loop(tvxapi_auth_url)
	except mechanize.HTTPError as err_msg:
		print('Server returned: %s' % err_msg)
	

