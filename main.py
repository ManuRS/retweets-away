import csv
import shutil, os
import argparse

file='tweets.csv'
file_all='tweets_all.csv'
file_new='tweets_clear.csv'

# To create the url
column_url=0
# Time of creation
column_dt=3
# Tweet text
column_tw=5
# Original user ID if is a rtweet
column_rt=6

user='nick'

ap = argparse.ArgumentParser()
ap.add_argument('-d', '--date', type=str, required=False, help='yyyy-mm-dd', default='')
ap.add_argument('-i', '--include', nargs='+', default=[], type=str, required=False, help='[str1,str2,etc]')
ap.add_argument('-ni', '--ninclude', nargs='+', default=[], type=str, required=False, help='[str1,str2,etc]')

args = vars(ap.parse_args())
date = args["date"]
include = args["include"]
ninclude = args["ninclude"]

if date!='':
	date_on = True
else:
	date_on = False

print('\033[92mThis script deletes a row if the selected column of that row has content')
print('Created to delete the re-tweets from an official twitter archive csv\n')

print('Reading from       =', file)
print('Backup file route  =', file_all)
print('New file route     =', file_new)
print('Columns & user     = set in the code\033[0m\n')

if os.path.exists(file):
    with open(file, 'rb') as forigen:
        with open(file_all, 'wb') as fdestino:
            shutil.copyfileobj(forigen, fdestino)

counter=-1
counter_org=0

f = open('salida.txt', 'w') 
with open(file_new, 'w', newline='') as csvdest:
	spamwriter = csv.writer(csvdest, delimiter=',', quoting=csv.QUOTE_ALL)

	with open(file, newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',') #quotechar='"'

		for row in spamreader:
			if counter>=0:
				
				if date in row[column_dt]: # Case with no date works because '' in any_str is True
					if row[column_rt]=='': 
						
						# Included words
						filter_a_pass=False
						if len(include)>0:
							for elem in include:
								if row[column_tw].find(elem)!=-1:
									filter_a_pass=True
									break
						else:
							filter_a_pass=True
							
						# Non included words
						filter_b_pass=True
						if len(ninclude)>0:
							for elem in ninclude:
								if row[column_tw].find(elem)==-1:
									filter_b_pass=False
									break
						# Filters
						if filter_a_pass and filter_b_pass:
							#if (row[column_tw].find(include)!=-1) and (row[column_tw].find(ninclude)==-1):
							# Original tweet
							counter_org+=1;
							spamwriter.writerow(row)

							print(row[column_tw])
							f.write(row[column_tw]) 

							print('\033[94mhttps://twitter.com/'+user+'/statuses/'+str(row[column_url])+'\033[0m')
							f.write('\nhttps://twitter.com/'+user+'/statuses/'+str(row[column_url])) 

							print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
							f.write('\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n') 
				counter+=1; # total counter

			else: # Only 1st time
				print('\033[93mColumn description:\n'+str(row)+'\033[0m')
				print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
				f.write('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n')
				counter+=1;

print('\033[92mTotal number of tweets (with rt)    = ', counter)
print('Original (and filtered) tweets      = ', counter_org)
print('Original (and filtered) tweets %    =  {0:.2f}%\033[0m'.format(counter_org*100/counter))
