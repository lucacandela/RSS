from datetime import datetime
from twilio.rest import Client
import praw
import config
sub = str(input("What subreddit shall I search? "))
tsv = str(input("What phrase should I search for in /r/%s? " % sub))

client = Client(config.account_sid, config.auth_token)
message = client.api.account.messages

sendMessage = True
getCommenter = False

def bot_login():
	r = praw.Reddit(username = config.username,
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
       		user_agent = "TropicalMemer's keyword Checker v0.1")	
	return r

def run_bot(r):
	counter = 0
	for comment in r.subreddit(sub).stream.comments():
		counter += 1
		commenturl = 'http://www.reddit.com/comments/'+ comment.submission.id + '/' +sub + '/' + comment.id
		submissiontime = datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')
		commenter = str(comment.author)
		if tsv in comment.body:
			if getCommenter == True:
				print (str(counter) +": X	String found in new comment	| " + submissiontime + " | /u/" + commenter + ": " + commenturl)
			else:
				print (str(counter) +": X	String found in new comment	| " + submissiontime + " | " + commenturl)
			#if comment.id in config.checkedsubmissions:
			#	("Already messaged TropicalMemer about " + commenturl)
			#if comment.id not in config.checkedsubmissions:
			if sendMessage == True:
				r.redditor('TropicalMemer').message(tsv+" found in new comment", commenturl)
				#message.create(to="+18583421959", from_="+18587042346", 
				#			  body=("Your phrase was found here. " + "\""+commenturl+"\""))
			# |	Find a way to write to the submission url
			# |	to the config.py file next door and save it
			# |	so that it doesn't notify you of the same 
			# |	submission twice if you rerun the program
			# |	config.checkedsubmissions.extend(comment.permalink)
		else:
			if getCommenter == True:
				print (str(counter) + ":	Nothing found in new comment	| " + submissiontime + " | /u/" + commenter + ": " + commenturl)
			else:
				print (str(counter) + ":	Nothing found in new comment	| " + submissiontime + " | " + commenturl)
r = bot_login()
run_bot(r)