import PySimpleGUI as sg
import os                       #Module for system
import shutil
import helper_functions
import mysql.connector

server = '127.0.0.1'
db = 'minimart'
username = 'root'
pwd = ''
conn = mysql.connector.connect(host=server, database=db, user=username, password=pwd,use_unicode=True, charset="utf8")
cur = conn.cursor()

# All types of image files
file_types = [("JPEG (*.jpg)", "*.jpg"), ("All files (*.*)", "*.*")]

def main_form():
    
    sql = 'select * from staff ORDER BY ordinal_num ASC'
    DataValues=helper_functions.table_read(conn,sql,1,8)

    # Modify date and gender showing on the table
    for i in range(len(DataValues)):
        DataValues[i][2]=helper_functions.Format_Date(str(DataValues[i][2]))
        if DataValues[i][3]==1:
            DataValues[i][3]='Male'
        if DataValues[i][3]==0:
            DataValues[i][3]='Female'


    D_Datavalues=DataValues
    
    Key_list=['staff_id','name','date_of_birth','Male','Female','id','phone_num','-FILE-']
    Headings=['Staff_ID','Name','Date_of_Birth','Gender','ID_num','Phone_num','Image']

    Panel=[[sg.Input(size=10,key=Key_list[0],visible=False),
        sg.Text(Headings[1],size=11),sg.Input(size=20,key=Key_list[1],focus=True),
        sg.Text(Headings[2],size=10),sg.Input(size=16,key=Key_list[2],readonly=True),sg.CalendarButton('Chọn ngày', close_when_date_chosen=True,  target=Key_list[2],default_date_m_d_y=(1,None,1980), location=(0,0), no_titlebar=False)],       
        [sg.Text(Headings[3],size=11),sg.Radio('Male',1,default=True,key='Male',size=5),sg.Radio('Female',1,default=False,key='Female',size=5),sg.Text(Headings[4],size=10),sg.Input(size=16,key=Key_list[5],enable_events=True)],
        [sg.Text(Headings[5],size=11),sg.Input(size=20,key=Key_list[6],enable_events=True),
        sg.FileBrowse(file_types=file_types,target="-FILE-",size=9),sg.Input(size=(16, 1), key=Key_list[7],readonly=True),sg.Button('QR scan',size=(9,1))],
        [sg.Button('PDF FILE',size=(9,1),disabled=True),sg.Button('Add row',size=(9,1)),sg.Button('Save Edit',disabled=True,size=(9,1)),sg.Button('Delete row',size=(9,1)),sg.Exit(size=(7,1)),sg.Button("Reset",size=(8,1))]
        ]
    
    Picture=[[sg.Image(r'',key='-IMAGE-',size=(100,120))]]
    
    # Create layout by combining Panel and Picture
    layout=[[sg.Frame('Staff information',Panel,expand_x = True),sg.Frame('Image',Picture)],
        [sg.Table(D_Datavalues,Headings,justification='left',key='mytable',enable_events=True)]]
    window=sg.Window('Staff management',layout)

    while True:
        
        event,values=window.read()
        if event in (None, 'Exit'):
            break
        
        # Limit the number of characters in the ID to 10
        if len(values['id']) > 10:
            window.Element('id').Update(values['id'][:-1])
            
        # Limit the numbers in the phone number to 10
        if len(values['phone_num']) > 10:
            window.Element('phone_num').Update(values['phone_num'][:-1])                 

        if event=='Reset':
            helper_functions.Reset_data_staff(window, Key_list) 

        flag=True
        if event=='Add row':
            values[Key_list[0]]=helper_functions.create_staff_id(DataValues) 
                             
            # Check if all fields are filled
            for i in range(8):
                if values[Key_list[i]]=='':
                    flag=False
                    break  
                
            if helper_functions.Check_phone(values[Key_list[6]])==False:
                flag=False
                sg.popup('Invalid phone number') 
                continue

            if helper_functions.Check_cm(values[Key_list[5]])==False:
                flag=False
                sg.popup('Invalid ID number')  
                continue  
            
            # If all fields are filled, add the row to the table
            if flag==True:                      
                if values[Key_list[3]]==True:
                    gender='Male'
                if values[Key_list[3]]==False:
                    gender='Female'
                    
                # Convert yy-mm-dd h:m:s to dd/mm/yy
                old_date=values[Key_list[2]][:10]
                new_date=helper_functions.Format_Date(old_date)

                # Get the current working directory
                # Get the path to the destination folder
                # Get the path of the uploaded file
                # Get the name of the uploaded file
                work_directory=os.getcwd()
                destination_folder=os.path.join(work_directory,"images_staff")
                sources_path=values['-FILE-']
                upload_file=helper_functions.Get_file(sources_path)
                # Save the uploaded file if it does not exist in the images folder
                if helper_functions.file_excist(upload_file,destination_folder)==False:
                    shutil.copy(sources_path,destination_folder)

                # Update the table
                D_Datavalues.append([values[Key_list[0]],values[Key_list[1]],new_date,gender,values[Key_list[5]],values[Key_list[6]],upload_file])
                DataValues.append([values[Key_list[0]],values[Key_list[1]],new_date,gender,values[Key_list[5]],values[Key_list[6]],upload_file])
                window['mytable'].update(values=D_Datavalues)
                helper_functions.Reset_data_staff(window,Key_list)
            
                # Insert the data into the database
                rw=[values[Key_list[0]],values[Key_list[1]],old_date,gender,values[Key_list[5]],values[Key_list[6]],upload_file]
                #             StaffID            name      date       gender     identification        phone_num       image
                     
                if rw[3]=='Male':
                    ph=1
                if rw[3]=='Female':
                    ph=0
                sql="INSERT INTO staff (ordinal_num,staff_id,staff_name,date_of_birth,gender,identification,mobile_phone,image) VALUES (Null,'"
                sql+=str(rw[0])+"','"+str(rw[1])+"','"+str(rw[2])+"','"+str(ph)+"','"+str(rw[4])+"','"+str(rw[5])+"','"+str(rw[6])+"');"     
                cur.execute(sql)            
            else:
                sg.popup('Not enough information')
                
        if event =='mytable':
            if values['mytable']==[]:
                sg.popup('No row selected')
            else:   
                         
                # Row selected (List)
                row_selected_index=values['mytable'][0]                  
                selected_row=D_Datavalues[row_selected_index]           
            
                # Modify gender to True or False
                if selected_row[3]=='Male':
                    td_update=[selected_row[0],selected_row[1],selected_row[2],True,False,selected_row[4],selected_row[5],selected_row[6]]
                if selected_row[3]=='Female':
                    td_update=[selected_row[0],selected_row[1],selected_row[2],False,True,selected_row[4],selected_row[5],selected_row[6]]
                
                # Update the form
                for i in range(8):
                    window[Key_list[i]].update(value=td_update[i])            
                window['Save Edit'].update(disabled=False)
                window['PDF FILE'].update(disabled=False) 
            
                # Display the image
                work_directory=os.getcwd()
                # Get the path to the destination folder
                destination_folder=os.path.join(work_directory,"images_staff")
                # If the staff has an image
                if helper_functions.file_excist(selected_row[6],destination_folder)==True:
                    image_path='images_staff/'+ selected_row[6]
                else:
                    image_path='images_staff/t1.png'
                helper_functions.image_display(window,image_path,'-IMAGE-')

        if event=='Save Edit':
            
            # Check if all fields are filled
            flag=True
            for i in range(8):
                if values[Key_list[i]]=='':
                    flag=False
                    break
                
            if helper_functions.Check_phone(values[Key_list[6]])==False:
                flag=False
                sg.popup('Invalid phone number') 

            if helper_functions.Check_cm(values[Key_list[5]])==False:
                flag=False
                sg.popup('Invalid ID number')  
                
            if flag==True:            
                staff_id=selected_row[0]            
            
                # New or same image file
                # Case 1: New image file
                work_directory=os.getcwd()
                destination_folder=os.path.join(work_directory,"images_staff")
                sources_path=values['-FILE-']
                upload_file=helper_functions.Get_file(sources_path)
                Li=sources_path.split('/')
                n=len(Li)
                if n>1:
                    # Save the uploaded file if it does not exist in the images folder
                    if helper_functions.file_excist(upload_file,destination_folder)==False:
                        shutil.copy(sources_path,destination_folder)
                    image=upload_file
                    
                else:
                    # Case 2: Same image file
                    image=values[Key_list[7]]

                # Change the date format to dd/mm/yy
                if len(values[Key_list[2]])>10:
                    Date_string=str(values[Key_list[2]])[:10]
                    new_date=helper_functions.Format_Date(Date_string)
                else:
                    new_date=values[Key_list[2]]

                if values[Key_list[3]]==True:
                    td=[values[Key_list[0]],values[Key_list[1]],new_date,'Male',values[Key_list[5]],values[Key_list[6]],image]
                if values[Key_list[3]]==False:
                    td=[values[Key_list[0]],values[Key_list[1]],new_date,'Female',values[Key_list[5]],values[Key_list[6]],image]
            
                # Update the value to be edited for D_Datavalues
                for i in range(len(D_Datavalues)):
                    if D_Datavalues[i][0]==staff_id:
                        D_Datavalues[i]=td   
                                                            
                # Update the table
                for i in range(len(DataValues)):
                    if DataValues[i][0]==staff_id:
                        DataValues[i]=td                    
                        
                # Update the table
                window['mytable'].update(values=D_Datavalues)
                
                #Loop to clean box
                for i in range(8):
                    window[Key_list[i]].update(value='')
                window['Save Edit'].update(disabled=True)
                
                # Update the database
                ns=helper_functions.Format_DateC(td[2])
                if td[3]=='Male':
                    ph='1'
                if td[3]=='Female':
                    ph='0'        
                   
                sql="UPDATE staff SET staff_name='"+td[1]+"',date_of_birth='"+ns+"',gender="+ph
                sql+=",identification='"+td[4]+"',mobile_phone='"+td[5]+"',image='"+td[6]+"' WHERE staff_id='"+td[0]+"';"
                cur.execute(sql)
                
                # Delete the inputs after editing
                helper_functions.Reset_data_staff(window,Key_list)
            else:
                sg.popup('Not enough information')                 
                
        if event =='Delete row':
            if values['mytable']==[]:
                sg.popup('No row selected')
            else:
                if sg.popup_ok_cancel('Can not undo Delete : Contine?')=='OK':
                    #Cập nhật vào DataBase
                    row_selected_index=values['mytable'][0]                
                    rw=D_Datavalues[row_selected_index]
                    ms=rw[0]                    
                    sql="DELETE FROM staff WHERE staff_id='"+ms+"'"
                    cur.execute(sql)                
                    del D_Datavalues[values['mytable'][0]]                
                #Cập nhật lên Bảng hiển thị
                    window['mytable'].update(values=D_Datavalues)

        if event=='PDF FILE':
            if values['mytable']==[]:
                sg.popup('No row selected')
            else:            
                row_selected_index=values['mytable'][0] #Chỉ số dòng được chọn trên Table
                sg.popup('Do you want to extract to PDF file?')                   
                selected_row=D_Datavalues[row_selected_index]            
                ms=selected_row[0]
                ten=selected_row[1]
                ns=selected_row[2]
                phai=selected_row[3]
                cm=selected_row[4]
                im=selected_row[6]
                helper_functions.QR_generate(selected_row[0],selected_row[1],selected_row[2],selected_row[3],selected_row[4])
                helper_functions.PDF_extract_staff(selected_row[0],selected_row[1],selected_row[2],selected_row[3],selected_row[4],'qr_code.png',selected_row[6])
                
        if event=='QR scan':
            maso=helper_functions.QR_trace()
            print(maso)
            for nv in D_Datavalues:
                if nv[0]==maso:
                    selected_row=nv
                    break
            if selected_row[3]=='Male':
                td_update=[selected_row[0],selected_row[1],selected_row[2],True,False,selected_row[4],selected_row[5],selected_row[6]]
            if selected_row[3]=='Female':
                td_update=[selected_row[0],selected_row[1],selected_row[2],False,True,selected_row[4],selected_row[5],selected_row[6]]
            
            #Update form
            for i in range(8):
                window[Key_list[i]].update(value=td_update[i])            
            window['Save Edit'].update(disabled=False)
            window['PDF FILE'].update(disabled=False) 
       
            work_directory=os.getcwd()
            destination_folder=os.path.join(work_directory,"images_staff")
            if helper_functions.file_excist(selected_row[6],destination_folder)==True:
                image_path='images_staff/'+ selected_row[6]
            else:
                image_path='images_staff/t1.png'
            helper_functions.image_display(window,image_path,'-IMAGE-')

    # if conn:
    #     conn.close()
    window.close()
