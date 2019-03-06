import re

def parse_line(line):
	# Searches provided line for failed logins and returns the 
	# username and password if a match is found. 
	# Else it returns nothing.
	
	# search for invalid user attempts
	search_pattern1 = 'Invalid\suser\s(\w+)\sfrom\s([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'
	# search for failed login for valid username
	search_pattern2 = 'Disconnected\sfrom\sauthenticating\suser\s(\w+)\s([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'
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
