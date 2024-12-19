import PySimpleGUI as sg
import helper_functions
import panel
import mysql.connector

# Connect to database
server = '127.0.0.1'
db = 'minimart'
username = 'root'
pwd = ''
conn = mysql.connector.connect(host=server, database=db, user=username, password=pwd,use_unicode=True, charset="utf8")
cur=conn.cursor()

def login_form():
	layout=[
	[sg.Text('Username',size=10),sg.InputText(size=20)],
	[sg.Text('Password',size=10),sg.InputText(password_char='*',size=20)],
	[sg.Text('Forget password',enable_events=True,key='ForgetPass',size=(15,1))],
	[sg.Submit(),sg.Cancel()]
	]
	window=sg.Window('Login Form',layout)
	while True:
		event,values=window.read()
  
  		# if user closes window or clicks cancel
		if event==sg.WIN_CLOSED or event=='Cancel':			
			break
		
		if event=='Submit':
			user=values[0]
			password=values[1]
   
			# Reading database to check if User and Pass are in the login table
			sql='select * from login'
			User_list=helper_functions.table_read(conn,sql,1,3)
			for us in User_list:
				if user==us[0] and password==us[1]:
					window.close()
					panel.panel_form()
					break
				else:
					sg.popup('Incorrect password')
		
		if event=='ForgetPass':
			sg.popup('Contact the admin for password recovery')
	
login_form()
