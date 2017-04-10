#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
import tkMessageBox
import tkSimpleDialog
import os,sys,csv
from tkFileDialog import *
class App(object):
    file_name = "installist"
    changed = False
    def __init__(self,master):
        self.master = master
        master.title("Installation List: Nomik Install Tool")
        master.geometry("640x480")
        
        
        menubar = Menu(master)
        filemenu = Menu(menubar,tearoff=0)
        filemenu.add_command(label="New",command=self.new_file)
        filemenu.add_command(label="Open",command=self.open_file)
        filemenu.add_command(label="Save",command=self.save_file)
        filemenu.add_command(label="Save as",command=self.save_as_file)
	filemenu.add_command(label="Install",command=self.install_everything)
        filemenu.add_command(label="Exit",command=self.exit_menu)
        menubar.add_cascade(label="File",menu=filemenu)

        master.config(menu=menubar)
        
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)
        
        self.text = Text(master,yscrollcommand=scrollbar.set)
        
        self.text.pack(side=LEFT,fill=BOTH,expand=1)
        scrollbar.config(command=self.text.yview)
        
        self.text.bind("<Key>",self.key_callback)
        #~ self.text.bind("<Return>",self.return_key)
        
        master.protocol("WM_DELETE_WINDOW",self.close_window)
        
        
        if len(sys.argv) > 1:
            if sys.platform == "win32":
                if sys.argv[1][-4:] == ".nomcsv":
                    try:
                        f = open(sys.argv[1])
                        for line in f:
                            self.text.insert(END,line)
                        f.close()
                        self.file_name = sys.argv[1]
                        self.master.title(self.file_name[self.file_name.rfind("/")+1:] + ": Nomik Install Tool")
                        self.changed = False
                    except IOError:
                        tkMessageBox.showwarning("Open file","Cannot open this file...")
            else:
                try:
                    f = open(sys.argv[1])
                    for line in f:
                        self.text.insert(END,line)
                    f.close()
                    self.file_name = sys.argv[1]
                    self.master.title(self.file_name[self.file_name.rfind("/")+1:] + ": Nomik Install Tool")
                    self.changed = False
                except IOError:
                    tkMessageBox.showwarning("Open file","Cannot open this file...")
       
    def open_file(self):
        filename = str(askopenfilename(title="Open File",filetypes=[('Nomik Install List','.nomcsv')]))
        if len(filename) > 0:
            self.text.delete("1.0",END)
            try:
                f = open(filename)
                for line in f:
                    self.text.insert(END,line)
                f.close()
                self.file_name = filename
                self.master.title(filename[filename.rfind("/")+1:] + ": Nomik Install Tool")
                self.changed = False
            except IOError:
                tkMessageBox.showwarning("Open file","Cannot open this file...") 
                
    def save_file(self):
        if self.file_name == "installist":
            self.save_as_file()
        else:
            f = open(self.file_name,"w")
            text = self.text.get("1.0",END).encode("utf-8")
            f.write(text)
            f.close()
            self.changed = False   
            self.master.title(self.file_name[self.file_name.rfind("/")+1:] + ": Nomik Install Tool")
    
    def save_as_file(self):
        filename = str(asksaveasfilename(title="Save as File",defaultextension=".nomcsv",filetypes=[('Nomik Install Lists','.nomcsv')]))
        if len(filename) > 0:
            f = open(filename,"w")
            text = self.text.get("1.0",END).encode("utf-8")
            f.write(text)
            f.close()
            self.file_name = filename
            self.master.title(filename[filename.rfind("/")+1:] + ": Nomik Install Tool")
            self.changed = False

    def install_everything(self):
	csvfilename = tkSimpleDialog.askstring("Install Command", "Enter your installation list filename") + ".nomcsv"
    	installist = open(csvfilename)
    	reader = csv.reader(installist)
    	data = list(reader)
    	lines = len(data)
	command = tkSimpleDialog.askstring("Install Command", "Enter your installation command here.")
    	i = 0
    	for row in data:
            package = row[0]
            i += 1
            os.system(command+" "+package)
        tkMessageBox.showinfo("Information", "Installation complete")

    def close_window(self):
        if self.changed:
            if tkMessageBox.askyesno("Quit","do you want to save the list..."):
                if self.file_name == "installist":
                    self.save_as_file()
                else:
                    f = open(self.file_name,"w")
                    text = self.text.get("1.0",END).encode("utf-8")
                    f.write(text)
                    f.close()
                    self.master.destroy()
            else:
                self.master.destroy()
        else:
            self.master.destroy()
        
    def key_callback(self,event):
        if not self.changed:
            self.master.title("*" + self.file_name[self.file_name.rfind("/")+1:] + ": Nomik Install Tool")
            self.changed = True
                
    def open_file_menu(self):
        if self.changed:
            if tkMessageBox.askyesno("Quit","do you want to save the file..."):
                if self.file_name == "installist":
                    obj = Save_File(self,"Save as")
                else:
                    f = open(self.file_name,"w")
                    text = self.text.get("1.0",END).encode("utf-8")
                    f.write(text)
                    f.close()
                    
            self.text.delete("1.0",END)
            self.file_name = "installist"
            self.master.title("Installation List: Nomik Install Tool")
            self.changed = False
        obj = Open_File(self,"Open")

    def save_as_file_menu(self):
        obj = Save_File(self,"Save")

        
    def save_file_menu(self):
        if self.file_name == "installist":
            obj = Save_File(self,"Save as")
        else:
            f = open(self.file_name,"w")
            text = self.text.get("1.0",END).encode("utf-8")
            f.write(text)
            f.close()
            self.changed = False
            self.master.title(self.file_name[self.file_name.rfind("/")+1:] + ": Nomik Install Tool")

    def new_file(self):
        if self.changed:
            if tkMessageBox.askyesno("New","Do you want to save the file..."):
                if self.file_name == "installist":
                    obj = Save_File(self,"Save as")
                else:
                    f = open(self.file_name,"w")
                    text = self.text.get("1.0",END).encode("utf-8")
                    f.write(text)
                    f.close()
        self.text.delete("1.0",END)
        self.file_name = "installist.nomcsv"
        self.master.title("Installation List: Nomik Install Tool")
        self.changed = False
        
    def exit_menu(self):
        if self.changed:
            if tkMessageBox.askyesno("Quit","do you want to save the file..."):
                if self.file_name == "installist":
                    self.save_as_file()
                else:
                    f = open(self.file_name,"w")
                    text = self.text.get("1.0",END).encode("utf-8")
                    f.write(text)
                    f.close()
                    self.master.destroy()
            else:
                self.master.destroy()
        else:
            self.master.destroy()


def main():
    root = Tk()
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()
