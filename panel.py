import PySimpleGUI as sg
import staff_management
import product_management
import selling_management
import quotation_management

def panel_form():
    
	layout=[
	[sg.Button('Selling Management',size=20)],
	[sg.Button('Staff Management',size=20)],
	[sg.Button('Inventory Management',size=20)],
	[sg.Button('Quotation Management',size=20)]]
	window=sg.Window('Control panel',layout)
 
	while True:
		event,values=window.read()
		if event==sg.WIN_CLOSED or event=='Cancel':
			break
		if event=='Selling Management':
			selling_management.mainform()
		if event=='Staff Management':
			staff_management.main_form()	
		if event=='Inventory Management':
			product_management.hang_hoa()
		if event=='Quotation Management':
			quotation_management.quotation()