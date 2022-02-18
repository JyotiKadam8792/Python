import PyPDF2
import DateTime
import tkinter
import csv
import os


##file_name = open("one.pdf",'rb')
##root = tkinter.Tk()
##root.withdraw()
# file_name = filedialog.askopenfilename()

# pdf_folder = r"C:\Users\91897\Desktop\Corporate_Trainings\BBI\PDF_File_Encryption"

#pdf_in_file = open('one.pdf', 'rb')
import tkinter
from tkinter import filedialog
file = filedialog.askopenfilename()

with open(file,"rb") as file_obj:

     inputpdf = PyPDF2.PdfFileReader(file)
     pages_no = inputpdf.numPages

     from datetime import datetime

     timestr = datetime.now().strftime("%Y_%B_%d_%H_%M_%S")
     # print(timestr)
     filename = file + "_" + timestr + ".pdf"
     # print(filename)
     f = open(filename, "w")
     path_folder = os.getcwd()
     file_folder = os.path.join(path_folder, filename)
     os.path.getsize(file_folder)

     output = PyPDF2.PdfFileWriter()

     for i in range(pages_no):
         inputpdf = PyPDF2.PdfFileReader(file)

         output.addPage(inputpdf.getPage(i))
         output.encrypt('admin@123')



         #with open("simple_password_protected.pdf", "wb") as outputStream:
         with open(filename ,"wb") as outputStream:
              output.write(outputStream)

with open("example.csv", "w") as file_obj:
    csv_file_obj = csv.writer(file_obj)
    csv_file_obj.writerow(["Datetime","FileName","FileSize"])
    csv_file_obj.writerows([[timestr,filename,os.path.getsize(file_folder)/1024]])

#print("size of file is {} bytes".format(os.path.getsize(filename)))
#file.close()