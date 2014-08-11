#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author - Max Cheswick 


import os, csv, glob, sys, hashlib, time
import MySQLdb as mdb
from collections import defaultdict
import itertools as it
con = mdb.connect( host="localhost",
	                   user = "root",
	                   passwd="",
	                   db="novitas")
cur = con.cursor()
con.commit()	                   
myDic={}
new_files={}	 

                 
def createTable():
	
	with con:
		cur.execute("DROP TABLE IF EXISTS names")
		cur.execute("CREATE TABLE names (old_names VARCHAR(25),\
		             new_names VARCHAR(25))")
	Query = """LOAD DATA LOCAL INFILE 'example.csv' INTO TABLE names \
	        FIELDS TERMINATED BY ',' ENCLOSED BY '"' \
	        LINES TERMINATED BY '\r\n' """
	cur.execute(Query)

	
def accessTable():
	with con: 
		cur = con.cursor(mdb.cursors.DictCursor)	
		cur.execute("SELECT * FROM names")
		rows = cur.fetchall()
		for row in rows:
			myDic[row["old_names"]]=row["new_names"]
	for filename in os.listdir(path):
		title, ext = os.path.splitext(os.path.basename(filename))
		if title in myDic:
			try:
				os.rename(os.path.join(path, filename), os.path.join(path, myDic[title])+ ext)
				
			except:
				print 'File ' +	filename + ' could not be renamed to ' + myDic[title]+ '!'
		    		
	return os.listdir(path)			
		
def outputHash(x):
	hash_list=[]
	for y in x:
		hasher = hashlib.md5()
		with open(os.path.join(path, y), 'rb') as afile:
			buf = afile.read()
			hasher.update(buf)
			hash_list.append((hasher.hexdigest()))
	return hash_list
	
			
def create_hash_dic(hash_list, file):
	#print hash_list
	#print file
	hash_dic = dict(zip(file, hash_list))
	print hash_dic.items()
	print hash_dic
#	for l, m in (hash_list, file):
#		hash_dic[m]=l
		






"""
toolbar_width=40

sys.stdout.write("[%s]" % (" "* toolbar_width))
sys.stdout.flush()
sys.stdout.write("\b"*(toolbar_width+1))

for i in xrange(toolbar_width):
	time.sleep(0.1)
	sys.stdout.write("-")
	sys.stdout.flush()
	
sys.stdout.write("\n")
		
"""
#Thank you Brian Khuu for this function	
def update_progress(progress):
    barLength = 10 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()



	
	
print "Hello, Welcome to the Maxinatator!"
print "Have fun and when you are finished type DONE. Thank you."
path = raw_input("Please type in or drag and drop a folder: ").strip()
#path = "/Users/max/Desktop/novitas/bates_folder"
csv = raw_input("Enter the csv file you wish to use:  ").strip()
#csv = "/Users/max/Desktop/novitas/example.csv"
while path!="q":
	print "Thank you. We are processing your request right now..."	
		
	createTable()
	
	update_progress(.25)
	time.sleep(1)
					             	                   
	#accessTable()
	
	update_progress(.50)
	time.sleep(1)
	
	#outputHash(accessTable())
	
	update_progress(.75)
	time.sleep(1)
	
	update_progress(1.0)
	time.sleep(1)
	
	create_hash_dic(outputHash(accessTable()), accessTable())
	#list_duplicates(outputHash(accessTable()))
	
		
	print "All finished. Your files have been renamed accordingly."
	path = raw_input("Please type in or drag and drop a folder, or type 'q' to quit: ").strip()
print "Thanks for re-naming with us."



cur.close()	                