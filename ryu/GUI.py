#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import *
import ImageTk

class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()


    def initUI(self):
      
        self.parent.title("Dynamic Routing-RYU Controller-OpenvSwitch")
        
	self.parent.canvas=Canvas(width=10, height=40)
	self.parent.canvas.pack(expand=YES, fill=BOTH)
	#self.parent.image=ImageTk.PhotoImage(file="/home/archanas/ryu/roger.jpg")
	#self.parent.canvas.create_image(10,10,image=self.parent.image,anchor=NW)
        
        self.columnconfigure(0, pad=10)
        self.columnconfigure(1, pad=10)
        self.columnconfigure(2, pad=10)
        
        self.rowconfigure(0, pad=10)
        self.rowconfigure(1, pad=10)
	self.rowconfigure(2, pad=20)	      
	def m1():
		execfile("/home/archanas/ryu/Run_topo.py")       
        c1 = Button(self, text=" Create Mininet Topology", command=m1)
        c1.grid(row=0, column=0, padx=10, pady=10, sticky=E+W+S+N)

	def m2():
		execfile("/home/archanas/ryu/Run_controller.py")
        c2 = Button(self, text=" Run Controller", command=m2)
        c2.grid(row=0, column=1,padx=10, pady=10, sticky=E+W+S+N)

	def m3():
		execfile("/home/archanas/ryu/Run_dumper.py")
        c3 = Button(self, text= "log link details", command=m3)
        c3.grid(row=0, column=2,padx=10, pady=10, sticky=E+W+S+N)    
        
	def m4():
		execfile("/home/archanas/ryu/Run_shortest_path.py")     
        c4 = Button(self, text="Run Shortest Path", command=m4)
        c4.grid(row=1, column=0,padx=10, pady=10, sticky=E+W+S+N)

	def m5():
		execfile("/home/archanas/ryu/5.py")        
        c5 = Button(self, text="Use table to run Flows", command=m5)
        c5.grid(row=1, column=1,padx=10, pady=10, sticky=E+W+S+N )         

	
	def m6():
		import sys
		sys.exit()
        c6 = Button(self, text="Exit", command=m6)
        c6.grid(row=2, column=1, padx=30, pady=30, sticky=E+W+S+N) 
 
	
	def m9():
		execfile("/home/archanas/ryu/remove.py")
	c9=Button(self, text="Delete log files", command=m9)
	c9.grid(row=1, column=2, padx=10, pady=10, sticky=E+W+S+N)
	

        self.pack()

def main():
  
    root = Tk()
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
