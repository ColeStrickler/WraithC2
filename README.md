# WraithC2 - A Basic C2 framework written in Python

# So what is a C2?
C2 stands for "command & control" and a C2 framework is used by hackers to control their malware from a central web-facing server.

# How does Wraith C2 Work?
![c2_overview](https://user-images.githubusercontent.com/82488869/162101228-440b0ddd-4a5e-427c-90b9-92603115f174.png)

WraithC2 is made up of two components, an agent and a webserver. The webserver is where the command and controlling will take place, while the agent will communicate
to the webserver's REST API to get tasks, execute them, and return results and data back to the server.

The webserver is set up using the Flask framework. The database is currently sqlite, but could easily be changed to any other SQL variety. The agent is written in python,
but could easily be compiled with pyinstaller for more stealth and better utility.

# CasperAgent Features

- command line access
- screenshots
- webcam spying
- keylogger
- 

