from datetime import datetime
from twilio.rest import Client
import praw
import config
sub = str(input("What subreddit shall I look in? "))
tsv = str(input("What phrase should I look for in /r/%s? "%sub))

client = Client(config.account_sid, config.auth_token)
message = client.api.account.messages

sendMessage = True
getCommenter = True

def bot_login():
	r = praw.Reddit(username = config.username,
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
       		user_agent = "TropicalMemer's ESV-TSV Checker v0.1")	
	return r

def run_bot(r):
	counter = 0
	for submission in r.subreddit(sub).stream.submissions():
		submissiontime = datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')
		counter +=1
		author = str(submission.author)
		if tsv in submission.selftext or tsv in submission.title:
			if getCommenter == True:
				print (str(counter) +": X	String found!!	| " + submissiontime+ " | /u/"+ author + ": " + submission.title)
			else:
				print (str(counter) +": X	String found!!	| " + submissiontime+ " | " + submission.title)
			#if submission.url in config.checkedsubmissions:
			#	print ("Already messaged TropicalMemer about " + submission.url)
			#if submission.url not in config.checkedsubmissions:
			if sendMessage == True:
				r.redditor('TropicalMemer').message("Your TSV matched an ESV of " + tsv, submission.url)
				#message.create(to="+18583421959", from_="+18582950094", 
				#			  body=("Your phrase was found here. " + "\""+submission.url+"\""))
				# |	Find a way to write to the submission url
				# |	to the config.py file next door and save it
				# |	so that it doesn't notify you of the same 
				# |	submission twice if you rerun the program
			#	config.checkedsubmissions.extend(submission.url)
		else:
			if getCommenter == True:
				print (str(counter) + ":	Nothing found..	| " + submissiontime + " | /u/" + author + ": " + submission.title)
			else:
				print (str(counter) + ":	Nothing found..	| " + submissiontime + " | " + submission.title)
r = bot_login()
run_bot(r)
