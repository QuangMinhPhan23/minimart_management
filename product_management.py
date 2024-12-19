import PySimpleGUI as sg
import os
import shutil
import mysql.connector
import helper_functions

# Connect to database
server = '127.0.0.1'
db = 'minimart'
username = 'root'
pwd = ''
conn = mysql.connector.connect(host=server, database=db, user=username, password=pwd,use_unicode=True, charset="utf8")
cur = conn.cursor()

# File types for file browse
file_types = [("JPEG (*.jpg)", "*.jpg"), ("All files (*.*)", "*.*")]

def hang_hoa():
    
    sql = 'select * from product ORDER BY ordinal_num ASC'
    DataValues=helper_functions.table_read(conn,sql,1,6)
    D_Datavalues=DataValues

    Keylist=['product_id','product_name','origin','-FILE-', 'available_quantity']
    Headings=['Product_ID','Product_Name','Origin','Image', 'Available']

    Panel=[[sg.Input(size=10,key=Keylist[0],visible=False),
        sg.Text(Headings[1],size=11),sg.Input(size=13,key=Keylist[1],focus=True),sg.Button('Add row',size=(9,1)),sg.Button('Save Edit',disabled=True,size=(9,1))],
            [sg.Text(Headings[2],size=11),sg.Input(size=13,key=Keylist[2]),sg.Button('Delete row',size=(9,1)),sg.Button("Reset",size=(9,1))],
        [sg.Text(text='File upload',size=11),sg.Input(size=(13,1),key=Keylist[3],readonly=True),sg.FileBrowse(file_types=file_types,target='-FILE-',size=(9,1)),sg.Exit(size=(9,1))],
        [sg.Text(Headings[4],size=11),sg.Input(size=(13,1),key=Keylist[4]),sg.Button('QR scan',size=(9,1)),sg.Button('PDF FILE',size=(9,1),disabled=True)]
    ]

    Picture=[[sg.Image(r'',key='-IMAGE-',size=(100,120))]]
    layout=[[sg.Frame('INFORMATION ABOUT THE PRODUCT',Panel,expand_x = True),sg.Frame('Image',Picture)],
        [sg.Table(D_Datavalues,Headings,justification='left',key='mytable',enable_events=True,size=(200,10))]]
    window=sg.Window('Product Management',layout)

    while True:
        event,values=window.read() 
        if event in (None, 'Exit'):
          break    
      
        # Show image
        if event == "Load Image":
            filename = values['-FILE-']          
            helper_functions.image_display(window,filename,'-IMAGE-')             
        
        if event=='Reset':
            helper_functions.Reset_data_product(window,Keylist) 

        flag=True
        if event=='Add row':
            values[Keylist[0]]=helper_functions.create_product_id(DataValues)  
                            
            # Check if all fields are filled
            for i in range(5):
                if values[Keylist[i]]=='':
                    flag=False
                    
            if flag==True:   
                                   
                # Find image name file
                work_directory=os.getcwd()
                destination_folder=os.path.join(work_directory,"images_products")
                sources_path=values['-FILE-']
                upload_file=helper_functions.Get_file(sources_path)
                if helper_functions.file_excist(upload_file,destination_folder)==False:
                    shutil.copy(sources_path,destination_folder)

                # Update data to the table      
                D_Datavalues.append([values[Keylist[0]],values[Keylist[1]],values[Keylist[2]],upload_file,values[Keylist[4]]])
                DataValues.append([values[Keylist[0]],values[Keylist[1]],values[Keylist[2]],upload_file,values[Keylist[4]]])
                window['mytable'].update(values=D_Datavalues)
                # Reset data
                helper_functions.Reset_data_product(window,Keylist)
            
                # Update to database
                rw=[values[Keylist[0]],values[Keylist[1]],values[Keylist[2]],upload_file,values[Keylist[4]]]
                #         Product_id       product_name           origin          image     available_quantity
    
                sql="INSERT INTO product (ordinal_num,product_id,product_name,origin,image, available_quantity) VALUES (Null,'"
                sql+=str(rw[0])+"','"+str(rw[1])+"','"+str(rw[2])+"','"+str(rw[3])+"','"+str(rw[4])+"');"     
                cur.execute(sql)            
            else:
                sg.popup('Not enough data')

        if event =='mytable':
            if values['mytable']==[]:
                sg.popup('No row selected')
            else:            
                # Get the row selected
                editRow=values['mytable'][0]           
                Erow=D_Datavalues[editRow]           
                td_update=[Erow[0],Erow[1],Erow[2],Erow[3],Erow[4]]
                
                # Update to the Update Form
                for i in range(5):
                    window[Keylist[i]].update(value=td_update[i])            
                window['Save Edit'].update(disabled=False)
                window['PDF FILE'].update(disabled=False) 
            
                # Show image
                work_directory=os.getcwd()
                destination_folder=os.path.join(work_directory,"images_products")
                if helper_functions.file_excist(Erow[3],destination_folder)==True:
                    image_path='images_products/'+ Erow[3]
                else:
                    image_path='images_products/den.jpg'
                helper_functions.image_display(window,image_path,'-IMAGE-')
                
        if event=='Save Edit':
            # Check if all fields are filled
            flag=True
            for i in range(4):
                if values[Keylist[i]]=='':
                    flag=False
                    break
            if flag==True:            
                product_ID=Erow[0]                      
               
                work_directory=os.getcwd()
                destination_folder=os.path.join(work_directory,"images_products")
                sources_path=values['-FILE-']
                upload_file=helper_functions.Get_file(sources_path)
                Li=sources_path.split('/')
                n=len(Li)
                if n>1:
                    if helper_functions.file_excist(upload_file,destination_folder)==False:
                        shutil.copy(sources_path,destination_folder)
                    hinh=upload_file
                else:
                    hinh=values[Keylist[3]]
                    
                td=[values[Keylist[0]],values[Keylist[1]],values[Keylist[2]],hinh,values[Keylist[4]]]
                
                # Update the edited value to the DataValues
                for i in range(len(D_Datavalues)):
                    if D_Datavalues[i][0]==product_ID:
                        D_Datavalues[i]=td                                       
            
                for i in range(len(DataValues)):
                    if DataValues[i][0]==product_ID:
                        DataValues[i]=td                    
                        
            # Update to the table
                window['mytable'].update(values=D_Datavalues)
            #Loop to clean box
                for i in range(4):
                    window[Keylist[i]].update(value='')
                window['Save Edit'].update(disabled=True)
                
                # Update to database
                sql="UPDATE product SET product_name='"+td[1]+"', origin='"+td[2]+"',image='"+td[3]+"',available_quantity='"+td[4]+"' WHERE product_id='"+td[0]+"';"
                cur.execute(sql)  
                # Reset data
                helper_functions.Reset_data_product(window,Keylist)
            else:
                sg.popup('Not enough data')                 
                
        if event =='Delete row':
            if values['mytable']==[]:
                sg.popup('No row selected')
            else:
                if sg.popup_ok_cancel('Can not undo Delete : Contine?')=='OK':
                    # Update to database
                    editRow=values['mytable'][0]                
                    rw=D_Datavalues[editRow]                   
                    sql="DELETE FROM product WHERE product_id='"+rw[0]+"'"
                    cur.execute(sql)                
                    del D_Datavalues[values['mytable'][0]]   
                                 
                    # Update to the table
                    window['mytable'].update(values=D_Datavalues)
                    helper_functions.Reset_data_product(window,Keylist)
                    
        # Extract to PDF file
        if event=='PDF FILE':
            if values['mytable']==[]:
                sg.popup('No row selected')
            else:            
                editRow=values['mytable'][0]
                sg.popup('Do you want to extract to PDF file?')                   
                Erow=D_Datavalues[editRow]            
                helper_functions.QR_generate(Erow[0],Erow[1],Erow[2],Erow[3],Erow[4])
                helper_functions.PDF_extract_product(Erow[0],Erow[1],Erow[2],'qr_code.png',Erow[3],Erow[4])
                
        if event=='QR scan':
            maso=helper_functions.QR_trace()
            for nv in D_Datavalues:
                if nv[0]==maso:
                    Erow=nv
                    break
        
            td_update=[Erow[0],Erow[1],Erow[2],Erow[3],Erow[4]]
            
            #Update lên Form Update
            for i in range(5):
                window[Keylist[i]].update(value=td_update[i])            
            window['Save Edit'].update(disabled=False)
            window['PDF FILE'].update(disabled=False) 
            
            work_directory=os.getcwd()
            destination_folder=os.path.join(work_directory,"images_products")
            if helper_functions.file_excist(Erow[3],destination_folder)==True:
                image_path='images_products/'+ Erow[3]
            else:
                image_path='images_products/den.jpg'
            helper_functions.image_display(window,image_path,'-IMAGE-')

    # if conn:
    #     conn.close()
    window.close() 
