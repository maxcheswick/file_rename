#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author - Max Cheswick 


import os, csv, glob, shutil
import MySQLdb as mdb


con = mdb.connect( host="localhost",
	                   user = "root",
	                   passwd="",
	                   db="novitas")
cur = con.cursor()	                   
myDic={}	 

                 
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
				
path = raw_input("Please type in or drag and drop a folder: ").strip()
print "Thank you. We are processing your request right now..."	
		
createTable()				             	                   
accessTable()	                   
print "All finished. Your files have been renamed accordingly."
con.commit()
cur.close()	                