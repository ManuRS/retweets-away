import csv
import shutil, os
import argparse

file='tweets.csv'
file_all='tweets_all.csv'
file_new='tweets_clear.csv'
column_link=0
column_dt=3
column_tw=5
column_rt=6
user='nick'

ap = argparse.ArgumentParser()
ap.add_argument('-d', '--date', type=str, required=False, help='yyyy-mm-dd', default='')
args = vars(ap.parse_args())
date = args["date"]
if args!='':
	date_on = True
else:
	date_on = False

print('\033[92mThis script deletes a row if the selected column of that row has content')
print('Created to delete the re-tweets from an official twitter archive csv\n')

print('Reading from       =', file)
print('Backup file route  =', file_all)
print('New file route     =', file_new)
print('Columns & user     = set in the code')
print('Date on            =', date_on) 
print('Date               =', date,'\033[0m\n')

if os.path.exists(file):
    with open(file, 'rb') as forigen:
        with open(file_all, 'wb') as fdestino:
            shutil.copyfileobj(forigen, fdestino)

counter=-1;
counter_org=0;

f = open('salida.txt', 'w') 
with open(file_new, 'w', newline='') as csvdest:
	spamwriter = csv.writer(csvdest, delimiter=',', quoting=csv.QUOTE_ALL)
	with open(file, newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',') #quotechar='"'
		for row in spamreader:
			if counter>=0:
				if date_on==True and date in row[column_dt]:
					if row[column_rt]=='': # Original tweet
						counter_org+=1;
						spamwriter.writerow(row)

						print(row[column_tw])
						f.write(row[column_tw]) 

						print('\033[94mhttps://twitter.com/'+user+'/statuses/'+str(row[column_link])+'\033[0m')
						f.write('\nhttps://twitter.com/'+user+'/statuses/'+str(row[column_link])) 

						print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
						f.write('\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n') 
					counter+=1;
			else:	
				print('\033[93mColumn description:\n',row,'\033[0m')
				print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
				f.write('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n')
				counter+=1;

print('\033[92mTotal tweets       = ', counter)
print('Original tweets    = ', counter_org)
print('% Original tweets  = ', counter_org*100/counter, '\033[0m')


		