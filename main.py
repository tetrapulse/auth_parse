import functions as f

# parse_line returns the tuple (username, ip) and so can be put into 
# a database or dictionary. I will start with dictionarys
failed_attemts = {}
failed_username = {}
filename = '/var/log/auth.log' # or /var/log/secure for RHEL based systems
with open(filename) as file_object:
	for line in file_object:
		result = f.parse_line(line)
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

print("IP addresses:")
for ip in failed_attemts.keys():
	print("%s\t%s" % (ip, failed_attemts[ip]))		

top_ip = max(failed_attemts, key=failed_attemts.get)
print("Worst offender:\t\t %s" % top_ip)
print("Attempted connections:\t %s" % failed_attemts[top_ip])
print("Usernames attempted:")
printed_names = []
for value in failed_username[top_ip]:
	if value not in printed_names:
		print(value)
		printed_names.append(value)
