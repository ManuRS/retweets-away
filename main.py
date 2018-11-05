import csv
import shutil, os
import argparse

############
# Variables
############
file     = 'tweets.csv'
file_all = 'tweets_all.csv'
file_new = 'tweets_clear.csv'

column_url = 0 # To create the url
column_dt  = 3 # Time of creation
column_tw  = 5 # Tweet text
column_rt  = 6 # Original user ID if is a rtweet

BLUE   = '\033[94m'
GREEN  = '\033[92m'
RED    = '\033[91m'
YELLOW = '\033[93m'
RESET  = '\033[0m'

line = '\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'

############
# Parser
############
ap = argparse.ArgumentParser()
ap.add_argument('-u', '--user', type=str, required=True,  help='nickname',   default='')
ap.add_argument('-d', '--date', type=str, required=False, help='yyyy-mm-dd', default='')

ap.add_argument('-rt', '--retweet',    action='store_true',  help='Turn rt tweets on',        default=False)
ap.add_argument('-og', '--originaltw', action='store_false', help='Turn original tweets off', default=True)

ap.add_argument('-i', '--include',  nargs='+', default=[], type=str, required=False, help='str1 str2 etc')
ap.add_argument('-ni','--ninclude', nargs='+', default=[], type=str, required=False, help='str1 str2 etc')

args = vars(ap.parse_args())
user = args["user"]
date = args["date"]
include = args["include"]
ninclude = args["ninclude"]
rt_on = args["retweet"]
org_on = args["originaltw"]

date_on=True if date!='' else False

############
# Backup
############
if os.path.exists(file):
    with open(file, 'rb') as forigen:
        with open(file_all, 'wb') as fdestino:
            shutil.copyfileobj(forigen, fdestino)

############
# Filters
############
def filters(row, date):
	# Date filter
	if (date in row[column_dt]) == False:
		return False

	# RT filter
	if row[column_rt]!='' and rt_on==False: 
		return False

	# Original tweet filter
	if row[column_rt]=='' and org_on==False:
		return False

	# Included and not included works better without url in the text
	tw_txt = clean_tweet(row[column_tw])

	# Included words filter
	aux=True
	if len(include)>0:
		aux=False
		for elem in include:
			if tw_txt.find(elem) != -1:
				aux=True
				break
	if aux==False:
		return False

	# Non included words filter
	if len(ninclude)>0:
		for elem in ninclude:
			if tw_txt.find(elem) != -1:
				return False
	return True

def clean_tweet(text):
	result=''
	for elem in text.split(' '):
		if ('http' not in elem) and ('://' not in elem):
			result+=elem+' '
	return result

############
# Main part
############
counter=-1
counter_org=0

# Opening the place to save the tweets
f       = open('salida.txt', 'w') # File to write in plain text
csvdest = open(file_new, 'w', newline='')
csvfile = open(file, newline='')
spamwriter = csv.writer(csvdest, delimiter=',', quoting=csv.QUOTE_ALL)
spamreader = csv.reader(csvfile, delimiter=',')

for row in spamreader:
	# First row is the column description
	if counter<0:
		txt='\nColumn description:\n'+str(row)
		print(YELLOW + txt + RESET + line)
		f.write(txt + line + '\n')

	# Tweet
	if filters(row, date)==True and counter>=0:
		counter_org+=1;
		spamwriter.writerow(row)

		txt = '\nhttps://twitter.com/'+user+'/statuses/'+str(row[column_url])
		print(row[column_tw] + BLUE + txt + RESET + line)
		f.write(row[column_tw] + txt + line + '\n') 

	# Count tweets
	counter+=1; 

############
# Final text
############
txt  = 'Reading from       = ' + file
txt += '\nBackup file route  = ' + file_all
txt += '\nNew file route     = ' + file_new + '\n'

print(GREEN + txt)
f.write(txt + '\n')

txt  = 'user           = ' + user
txt += '\nshow own tw  = ' + str(org_on)
txt += '\nshow rt tw   = ' + str(rt_on)
txt += '\ndate         = ' + date
txt += '\ninclude      = ' + str(include)
txt += '\nninclude     = ' + str(ninclude) + '\n'

print(RED + txt)
f.write(txt + '\n')

txt  = 'Total # of tweets (with RT)  = ' + str(counter)
txt += '\nFiltered tweets              = ' + str(counter_org)
txt += '\nFiltered tweets %            = {0:.2f}%\n'.format(counter_org*100/counter)

print(GREEN + txt)
f.write(txt + '\n')

txt  = 'Created to delete re-tweets from a csv twitter archive'
txt += '\nNow you can also filter by date or words'
url  = '\nhttps://github.com/manurs/retweets-away\n'

print(RESET + txt + BLUE + url + RESET)
f.write(txt + url)

############
# Close
############
f.close()
csvdest.close()
csvfile.close()
