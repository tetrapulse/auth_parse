#!/usr/bin/python3
import re
import argparse

# --- Begin argument parsing ---
parser = argparse.ArgumentParser(description='Tool to analize ssh attempts '
	'and show top offenders.')

parser.add_argument('--log-file', '-l', default='/var/log/auth.log',
	help='Authentication log file. Default is: /var/log/authlog')

args = parser.parse_args()

filename = args.log_file # argparse removes leading dashes and converts
						 # internal dashes to underscores
# --- End arguement parsing ---

def parse_line(line):
	# Searches provided line for failed logins and returns the 
	# username and password if a match is found. 
	# Else it returns nothing.
	
	# search for invalid user attempts
	search_pattern1 = 'Invalid\suser\s(\w+)\sfrom\s(\d+\.\d+\.\d+\.\d+)'
	# search for failed login for valid username
	search_pattern2 = 'Disconnected\sfrom\sauthenticating\suser\s(\w+)\s(\d+\.\d+\.\d+\.\d+)'
	result1 = re.search(search_pattern1, line)
	result2 = re.search(search_pattern2, line)
	# assuming only one line parsed at a time so only one of the results
	# will be valid.
	if result1:
		username = result1.group(1)
		ip = result1.group(2)
		return (username, ip)
	elif result2:
		username = result2.group(1)
		ip = result2.group(2)
		return (username, ip)
	else:
		# line did not contain a failed login and ip so will not return
		# anything
		pass


# parse_line returns the tuple (username, ip) and so can be put into 
# a database or dictionary. I will start with dictionarys
failed_attemts = {}
failed_username = {}
try:
	with open(filename) as file_object:
		for line in file_object:
			result = parse_line(line)
			# First assumes that an entry already exists for the current IP.
			# Should that not be the case it will correct it by creating it new.
			# Should both of those fail it will print a message letting the user know
			if result:
				try:
					failed_attemts[result[1]] += 1
				except:
					failed_attemts[result[1]] = 1			
				
				try:
					failed_username[result[1]].append(result[0])
				except:
					failed_username[result[1]] = [result[0]]
except FileNotFoundError as err:
	print("The log file: " + args.log_file + " could not be found.")
	print(err)
	exit(2)
except PermissionError as err:
	print("You do not have permission to read this file, are you root?")
	print(err)
	exit(13)

# If no items are added to the dictionarys the program will display a 
# message and exit.
if not failed_attemts and not failed_username:
	print(f'No ssh login attempts found in {filename}')
	print('Exiting...')
	exit(0)

# Reporting to console begins here
print("IP addresses and number of attempts:")
for ip in failed_attemts.keys():
	print("\t%s\t%s" % (ip, failed_attemts[ip]))		

top_ip = max(failed_attemts, key=failed_attemts.get)
print("Worst offender:\t\t %s" % top_ip)
print("Attempted connections:\t %s" % failed_attemts[top_ip])
print("Usernames attempted:")
printed_names = []
for value in failed_username[top_ip]:
	if value not in printed_names:
		print('\t' +value)
		printed_names.append(value)
