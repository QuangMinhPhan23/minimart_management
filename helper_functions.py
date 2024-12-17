#Module for UI
import PySimpleGUI as sg
#Module for Wamp server
#Module for checking
import re
#Module for system
import io
import os
#Module for image
from PIL import Image
#Module for copying directory and file
#Module for exporting PDF file
from fpdf import FPDF
#Generating QR and export to PDF file
import qrcode
import winsound
#Module for controling camera
import cv2
#Module for decoding codebar
from pyzbar.pyzbar import decode
from datetime import date

#Checking ID
def Check_cm(cm):
    flag=True
    chk= (re.findall('\d{10}',cm))
    if chk==[] or len(cm)>10:
        flag=False
    return flag

#Checking phone_num
def Check_phone(so):
    flag=True
    chk= (re.findall('0[1-9]\d{8}',so))
    if chk==[] or len(so)>10:
        flag=False
    return flag

#Checking if a file is existing in a directory
def file_excist(filename,path_to_file):
    path=path_to_file + "\\"+ filename 
    isFile = os.path.isfile(path)
    return isFile

#Formating (Date Picker yyyy-mm-dd)=>(dd/mm/yyyy) to display in the table
def Format_Date(StrA):
    Li=StrA.split('-')
    date=Li[2]+"/"+Li[1]+"/"+Li[0]
    return date

#Formating date getting form the displayed grid (đ/mm/yyyy)=>(yy-mm-dd) to save in the database
def Format_DateC(StrA):
    Li=StrA.split('/')
    date=Li[2]+"-"+Li[1]+"-"+Li[0]
    return date

#Getting file name from full path
def Get_file(Path_str):
    Li=Path_str.split('/')
    n=len(Li)
    filename=Li[n-1]
    return filename

#Displaying image file to image componet with key of imagekey
def image_display(window,file_path,image_key):    
    if os.path.exists(file_path):
        image = Image.open(file_path)
        image.thumbnail((100, 120))
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        window[image_key].update(data=bio.getvalue())

# Reading data from the table in the database
def table_read(conn,sql,start_col,end_col):
    cur = conn.cursor()
    cur.execute(sql)
    Data=[]
    dong=[] 
    row = cur.fetchone()
    while row:
        for i in range(start_col,end_col):
            dong.append(row[i])        
        Data.append(dong)
        dong=[] 
        row = cur.fetchone()
    return Data

# Creating QR code
def QR_generate(any1,any2,any3,any4,any5):
    data = str(any1)+'-'+str(any2)+'-'+str(any3)+'-'+str(any4)+'-'+str(any5)     
    # Encoding data using make() function
    img = qrcode.make(data) 
    # Saving as an image file
    img.save('qr_code.png')
 
# Scanning QR code return the id
def QR_trace():
    cap=cv2.VideoCapture(0)
    cap.set(3,400) #3-width
    cap.set(4,300) #4-Height
    used_codes=[]    

    camera=True
    while camera==True:
        success, frame=cap.read()
        for code in decode(frame):
            if code.data.decode('utf-8') not in used_codes:
                print('New QR is detected')
                print(code.data.decode('utf-8'))                
                camera=False
                cap.release()            
        cv2.imshow('Testing-Code-Scan',frame)
        cv2.waitKey(1)
    QR_data=code.data.decode('utf-8')
    QR_list=QR_data.split('-')
    id=QR_list[0]    
    cv2.destroyAllWindows()
    winsound.PlaySound('test.wav', winsound.SND_FILENAME)
    return id

#Clearing displayed data
def Reset_data_staff(window,Key_list):
    for i in range(8):
        if i==3:
            window[Key_list[3]].update(value=True)
        if i==4:
            window[Key_list[4]].update(value=False)
        window[Key_list[i]].update(value='')
    image_path='images_staff/t1.png'
    image = Image.open(image_path)
    image.thumbnail((100, 120))
    bio = io.BytesIO()
    image.save(bio, format="PNG")
    window["-IMAGE-"].update(data=bio.getvalue())   
    
def Reset_data_product(window,Keylist):
    for i in range(5):
        window[Keylist[i]].update(value='')
    image_path='images_products/den.jpg'
    image = Image.open(image_path)
    image.thumbnail((100, 120))
    bio = io.BytesIO()
    image.save(bio, format="PNG")
    window["-IMAGE-"].update(data=bio.getvalue()) 
    
def Reset_data_quotation(window,Keylist):
    for i in range(5):
        window[Keylist[i]].update(value='') 
        
def Reset_data_selling(window,Keylist):
    for i in range(9):
        window[Keylist[i]].update(value='')  

def PDF_extract_staff(ten,ns,phone,cm,im_name,im):
    pdf = FPDF()
    pdf.add_page()
    pdf.alias_nb_pages()
    pdf.set_font('Arial','B',16)
    pdf.cell(150,10,ten,align='C')

    pdf.set_xy(30,30)
    pdf.set_font('Arial','B',14)
    pdf.cell(100,10,'Date of birth: '+ns,align='L')

    pdf.set_xy(30,40)
    pdf.set_font('Arial','B',14)
    pdf.cell(100,10,'Phone number: '+phone,align='L')
    
    pdf.set_xy(30,50)
    pdf.set_font('Arial','B',14)
    pdf.cell(100,10,'Identification number: '+cm,align='L')
    
    pdf.set_xy(30,60)
    pdf.image('images_staff/'+im, w = 80)
    
    pdf.set_xy(120,60)
    pdf.image(im_name, w = 80)

    pdf.output('report.pdf')
    os.startfile('report.pdf')
    
def PDF_extract_product(p_id,pn,d,qr,im,available):
    pdf = FPDF()
    pdf.add_page()                    
    pdf.alias_nb_pages()                    
    pdf.set_font('Arial','B',16)
    pdf.cell(200,10,'PRODUCT INFORMATION',align='C')

    pdf.set_xy(30,30)
    pdf.set_font('Arial','B',14)
    pdf.cell(100,10,'PRODUCT ID : '+p_id,align='L')
    
    pdf.set_xy(30,40)
    pdf.set_font('Arial','B',14)
    pdf.cell(100,10,'PRODUCT NAME : '+pn,align='L')
    
    pdf.set_xy(30,50)
    pdf.set_font('Arial','B',14)
    pdf.cell(100,10,'ORIGIN : '+d,align='L')
    
    pdf.set_xy(30,60)
    pdf.set_font('Arial','B',14)
    pdf.cell(100,10,'AVAILABILITY : '+str(available),align='L')
    
    pdf.set_xy(110,50)
    pdf.image('images_products/'+im,w=100)
    pdf.set_xy(30,70)
    pdf.image(qr,w=50)
    pdf.output('report.pdf','F')
    os.startfile('report.pdf')
    
def PDF_extract_quotation(i_id,p_id,price,qr,date,supplier):
    pdf = FPDF()
    pdf.add_page()                    
    pdf.alias_nb_pages()                    
    pdf.set_font('Arial','B',16)
    pdf.cell(200,10,'PRICE INFORMATION',align='C')

    pdf.set_xy(30,30)
    pdf.set_font('Arial','B',14)
    pdf.cell(100,10,'PRICE_ID : '+i_id,align='L')
    
    pdf.set_xy(30,40)
    pdf.set_font('Arial','B',14)
    pdf.cell(100,10,'PRODUCT_ID : '+p_id,align='L')
    
    pdf.set_xy(30,50)
    pdf.set_font('Arial','B',14)
    pdf.cell(100,10,'PRICE : '+price,align='L')
    
    pdf.set_xy(30,60)
    pdf.set_font('Arial','B',14)
    pdf.cell(100,10,'APPLIED_DATE : '+str(date),align='L')
    
    pdf.set_xy(30,70)
    pdf.set_font('Arial','B',14)
    pdf.cell(100,10,'SUPPLIER : '+str(supplier),align='L')
    
    pdf.set_xy(30,80)
    pdf.image(qr,w=50)
    pdf.output('report.pdf','F')
    os.startfile('report.pdf')
    
def PDF_extract_selling(DataValues,Order_id,today,total):
    pdf = FPDF()
    pdf.add_page()
    pdf.alias_nb_pages()
    pdf.set_font('Arial','B',17)
    pdf.cell(200,10,'RECEIPT',align='C')

    pdf.set_xy(10,30)
    pdf.set_font('Arial','B',14)
    pdf.cell(100,10,'RECEIPT_ID: '+Order_id,align='L')

    pdf.set_xy(10,40)
    pdf.set_font('Arial','B',14)
    pdf.cell(100,10,'ON DATE: '+str(today),align='L')
    
    pdf.set_xy(10,50)
    pdf.set_font('Arial','B',14)
    pdf.cell(100,10,'TOTAL: '+str(total),align='L')
    
    pdf.set_xy(10,70)
    pdf.set_font('Arial','B',12)
    pdf.cell(100,10,'PRODUCT ID: ',align='L')

    pdf.set_xy(50,70)
    pdf.set_font('Arial','B',10)
    pdf.cell(100,10,'PRODUCT NAME: ',align='L')

    pdf.set_xy(100,70)
    pdf.set_font('Arial','B',12)
    pdf.cell(100,10,'ORIGIN: ',align='L')

    pdf.set_xy(130,70)
    pdf.set_font('Arial','B',12)
    pdf.cell(100,10,'UNIT PRICE: ',align='L')

    pdf.set_xy(170,70)
    pdf.set_font('Arial','B',12)
    pdf.cell(100,10,'QUANTITY: ',align='L')

    pdf.set_xy(210,70)
    pdf.set_font('Arial','B',12)
    pdf.cell(100,10,'AMOUNT: ',align='L')

    y=70
    for row in DataValues:
        y+=10
        
        pdf.set_xy(10,y)
        pdf.cell(100,10,str(row[1]),align='L')

        pdf.set_xy(50,y)
        pdf.cell(100,10,str(row[2]),align='L')

        pdf.set_xy(100,y)
        pdf.cell(100,10,str(row[3]),align='L')

        pdf.set_xy(130,y)
        pdf.cell(100,10,str(row[4]),align='L')

        pdf.set_xy(170,y)
        pdf.cell(100,10,str(row[5]),align='L')

        pdf.set_xy(210,y)
        pdf.cell(100,10,str(row[6]),align='L')



    pdf.output('receipt.pdf','F')
    os.startfile('receipt.pdf')
   
    
def create_price_id(DList):
    n=len(DList)
    mid=DList[n-1][0]   
    so=int(mid[2:])+1
    if len(str(so))==1:
        p_id="IP00"+str(so)
    if len(str(so))==2:
        p_id="IP0"+str(so)
    if len(str(so))==3:
        p_id="IP"+str(so)
    return p_id

def create_product_id(DList):
    n=len(DList)
    mid=DList[n-1][0]   
    so=int(mid[2:])+1
    if len(str(so))==1:
        p_id="SP00"+str(so)
    if len(str(so))==2:
        p_id="SP0"+str(so)
    if len(str(so))==3:
        p_id="SP"+str(so)
    return p_id

#The function to generating unique code
def create_staff_id(DList):
    n=len(DList)
    mid=DList[n-1][0]   
    so=int(mid[2:])+1
    if len(str(so))==1:
        ms="NV00"+str(so)
    if len(str(so))==2:
        ms="NV0"+str(so)
    if len(str(so))==3:
        ms="NV"+str(so)
    return ms

def create_order_id(conn):
    today = date.today()
    sql="select * from selling where date='"+str(today)+"' order by ordinal_num ASC" #Generating order ID
    OR_List=table_read(conn,sql,0,2)
    if OR_List==[]:
        Order_id="OD"+str(today)+"-0001"
    else:
        Last_or=OR_List[len(OR_List)-1]
        ID=Last_or[1]
        ID_list=ID.split("-")
        num=int(ID_list[3])+1
        if num<10:
            Order_id='OD'+str(today)+'-000'+str(num)
        if num>=10 and num<100:
            Order_id='OD'+str(today)+'-00'+str(num)
        if num>=100 and num<1000:
            Order_id='OD'+str(today)+'-0'+str(num)
        if num>=100 and num<10000:
            Order_id='OD'+str(today)+'-'+str(num)
    return Order_id