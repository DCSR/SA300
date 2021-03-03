"""

February, 2021

boolean variables controlled by SYSVARS 

"""


from tkinter import *
import tkinter.ttk as ttk
import tkinter.scrolledtext
from tkinter import messagebox
import serial
import serial.tools.list_ports
import os
import glob
import time
import queue
from datetime import date
from datetime import datetime
import ArdLib
import GraphLib
from time import sleep


def main(argv=None):
    if argv is None:
        argv = sys.argv
    gui = GuiClass()
    gui.go()
    return 0

class GuiClass(object):
    def __init__(self):

        self.version = "SA301.01"
        self.varCode = 0
        self.verbose = True
        self.sched = ['0: Do not run', '1: FR(N)', '2: FR1 x 20 trials', '3: FR1 x N trials', '4: PR(step N)', '5: TH', '6: IntA: 5-25', '7: Flush', '8: L2-HD', '9: IntA-HD', '10: 2L-PR-HD']
        self.box1 = Box(1)
        self.box2 = Box(2)
        self.box3 = Box(3)
        self.box4 = Box(4)
        self.box5 = Box(5)
        self.box6 = Box(6)
        self.box7 = Box(7)
        self.box8 = Box(8)
        self.example1List = []
        self.example2List = []
        self.sessionLog = []
        
        # note that boxes[0] is box1
        self.boxes = [self.box1,self.box2,self.box3,self.box4,self.box5,self.box6,self.box7,self.box8]
        # ********  Display stuff ************
        self.X_ZERO = 50
        self.Y_ZERO = 275
        self.CANVAS_WIDTH = 600
        self.CANVAS_HEIGHT = 400
        
        # *****************************
        self.arduino0 = ArdLib.Arduino()
        self.dataStreamOn = True
        self.echoCount = 0

        # ******************* tk - GUI interface   ****************************** 
        self.root = Tk()
        self.root.title(self.version)
        self.root.protocol("WM_DELETE_WINDOW", self.askBeforeExiting) 

        # ***** tk specific variables (StringVars, IntVars and BooleanVars) *****

        self.selectMax_x_Scale = IntVar(value = 180)
        self.selectedBox = IntVar(value = 0)
        self.selectedReinforcer = IntVar(value = 0)
        self.OS_String = StringVar(value="OS = ?")

        self.sys0CheckVar = BooleanVar(value=False)            
        self.sys1CheckVar = BooleanVar(value=False)            
        self.sys2CheckVar = BooleanVar(value=False)            
        self.sys3CheckVar = BooleanVar(value=False)            
        self.sys4CheckVar = BooleanVar(value=False)
        self.sys5CheckVar = BooleanVar(value=False)            
        self.sys6CheckVar = BooleanVar(value=False)            
        self.sys7CheckVar = BooleanVar(value=False) 
        
        self.showDataStreamCheckVar = BooleanVar(value=False)
        self.checkLeversCheckVar = BooleanVar(value=True)
        self.showOutputCheckVar = BooleanVar(value=False)
        self.portString = StringVar(value="----")             # will be assigned value from last line of ini file
        self.B1_lever1CheckVar = BooleanVar(value=False)      # or set it later this way: self.lever1CheckVar.set(False)
        self.B1_lever2CheckVar = BooleanVar(value=False) 
        self.B1_LED1CheckVar   = BooleanVar(value=False)
        self.B1_LED2CheckVar   = BooleanVar(value=False)
        self.B1_pumpCheckVar  = BooleanVar(value=False)
        self.B1_IDStr = StringVar(value="box1")                       
        self.B1_Weight = IntVar(value=100)
        self.B1_sched = StringVar(value="FR")         
        self.B1_Param_value = IntVar(value=1)         
        self.B1_SessionLength = IntVar(value=120)
        self.B1_IBILength = IntVar(value=0)
        self.B1_PumpTime = IntVar(value=4000)
        self.B1_calcPumpTime = BooleanVar(value=True)
        self.B1_L1Resp   = IntVar(value=0)
        self.B1_L2Resp   = IntVar(value=0)
        self.B1_Inf    = IntVar(value=0)
        self.B1_SessionTimeStr = StringVar(value="0:0:00")

        self.B2_lever1CheckVar = BooleanVar(value=False)
        self.B2_lever2CheckVar = BooleanVar(value=False) 
        self.B2_LED1CheckVar   = BooleanVar(value=False)
        self.B2_LED2CheckVar   = BooleanVar(value=False)
        self.B2_pumpCheckVar  = BooleanVar(value=False)
        self.B2_IDStr = StringVar(value="box2")
        self.B2_Weight = IntVar(value=100)
        self.B2_sched = StringVar(value="FR")             
        self.B2_Param_value = IntVar(value=1)        
        self.B2_SessionLength = IntVar(value=2)
        self.B2_IBILength = IntVar(value=0)
        self.B2_PumpTime = IntVar(value=4000)
        self.B2_calcPumpTime = BooleanVar(value=True)
        self.B2_L1Resp   = IntVar(value=0)
        self.B2_L2Resp   = IntVar(value=0)
        self.B2_Inf    = IntVar(value=0)
        self.B2_SessionTimeStr = StringVar(value="0:0:00")

        self.B3_lever1CheckVar = BooleanVar(value=False)
        self.B3_lever2CheckVar = BooleanVar(value=False) 
        self.B3_LED1CheckVar   = BooleanVar(value=False)
        self.B3_LED2CheckVar   = BooleanVar(value=False)
        self.B3_pumpCheckVar  = BooleanVar(value=False)
        self.B3_IDStr = StringVar(value="box3")
        self.B3_Weight = IntVar(value=100)
        self.B3_sched = StringVar(value="FR")            
        self.B3_Param_value = IntVar(value=1)         
        self.B3_SessionLength = IntVar(value=2)
        self.B3_IBILength = IntVar(value=0)
        self.B3_PumpTime = IntVar(value=4000)
        self.B3_calcPumpTime = BooleanVar(value=True)
        self.B3_L1Resp   = IntVar(value=0)
        self.B3_L2Resp   = IntVar(value=0)
        self.B3_Inf    = IntVar(value=0)
        self.B3_SessionTimeStr = StringVar(value="0:0:00")

        self.B4_lever1CheckVar = BooleanVar(value=False)
        self.B4_lever2CheckVar = BooleanVar(value=False) 
        self.B4_LED1CheckVar   = BooleanVar(value=False)
        self.B4_LED2CheckVar   = BooleanVar(value=False)
        self.B4_pumpCheckVar  = BooleanVar(value=False)
        self.B4_IDStr = StringVar(value="box4")
        self.B4_Weight = IntVar(value=100)
        self.B4_sched = StringVar(value="FR")            
        self.B4_Param_value = IntVar(value=1)   
        self.B4_SessionLength = IntVar(value=2)
        self.B4_IBILength = IntVar(value=0)
        self.B4_PumpTime = IntVar(value=4000)
        self.B4_calcPumpTime = BooleanVar(value=True)
        self.B4_L1Resp   = IntVar(value=0)
        self.B4_L2Resp   = IntVar(value=0)
        self.B4_Inf    = IntVar(value=0)
        self.B4_SessionTimeStr = StringVar(value="0:0:00")

        self.B5_lever1CheckVar = BooleanVar(value=False)
        self.B5_lever2CheckVar = BooleanVar(value=False) 
        self.B5_LED1CheckVar   = BooleanVar(value=False)
        self.B5_LED2CheckVar   = BooleanVar(value=False)
        self.B5_pumpCheckVar  = BooleanVar(value=False)
        self.B5_IDStr = StringVar(value="box5")
        self.B5_Weight = IntVar(value=100)
        self.B5_sched = StringVar(value="FR")             
        self.B5_Param_value = IntVar(value=1)       
        self.B5_SessionLength = IntVar(value=2)
        self.B5_IBILength = IntVar(value=0)
        self.B5_PumpTime = IntVar(value=4000)
        self.B5_calcPumpTime = BooleanVar(value=True)
        self.B5_L1Resp   = IntVar(value=0)
        self.B5_L2Resp   = IntVar(value=0)
        self.B5_Inf    = IntVar(value=0)
        self.B5_SessionTimeStr = StringVar(value="0:0:00")

        self.B6_lever1CheckVar = BooleanVar(value=False)
        self.B6_lever2CheckVar = BooleanVar(value=False) 
        self.B6_LED1CheckVar   = BooleanVar(value=False)
        self.B6_LED2CheckVar   = BooleanVar(value=False)
        self.B6_pumpCheckVar  = BooleanVar(value=False)
        self.B6_IDStr = StringVar(value="box6")
        self.B6_Weight = IntVar(value=100)
        self.B6_sched = StringVar(value="FR")           
        self.B6_Param_value = IntVar(value=1)      
        self.B6_SessionLength = IntVar(value=2)
        self.B6_IBILength = IntVar(value=0)
        self.B6_PumpTime = IntVar(value=4000)
        self.B6_calcPumpTime = BooleanVar(value=True)
        self.B6_L1Resp   = IntVar(value=0)
        self.B6_L2Resp   = IntVar(value=0)
        self.B6_Inf    = IntVar(value=0)
        self.B6_SessionTimeStr = StringVar(value="0:0:00")

        self.B7_lever1CheckVar = BooleanVar(value=False)
        self.B7_lever2CheckVar = BooleanVar(value=False) 
        self.B7_LED1CheckVar   = BooleanVar(value=False)
        self.B7_LED2CheckVar   = BooleanVar(value=False)
        self.B7_pumpCheckVar  = BooleanVar(value=False)
        self.B7_IDStr = StringVar(value="box7")
        self.B7_Weight = IntVar(value=100)
        self.B7_sched = StringVar(value="FR")          
        self.B7_Param_value = IntVar(value=1)       
        self.B7_SessionLength = IntVar(value=2)
        self.B7_IBILength = IntVar(value=0)
        self.B7_PumpTime = IntVar(value=4000)
        self.B7_calcPumpTime = BooleanVar(value=True)
        self.B7_L1Resp   = IntVar(value=0)
        self.B7_L2Resp   = IntVar(value=0)
        self.B7_Inf    = IntVar(value=0)
        self.B7_SessionTimeStr = StringVar(value="0:0:00")

        self.B8_lever1CheckVar = BooleanVar(value=False)
        self.B8_lever2CheckVar = BooleanVar(value=False) 
        self.B8_LED1CheckVar   = BooleanVar(value=False)
        self.B8_LED2CheckVar   = BooleanVar(value=False)
        self.B8_pumpCheckVar  = BooleanVar(value=False)
        self.B8_IDStr = StringVar(value="box8")
        self.B8_Weight = IntVar(value=100)
        self.B8_sched = StringVar(value="FR")             
        self.B8_Param_value = IntVar(value=1)        
        self.B8_SessionLength = IntVar(value=2)
        self.B8_IBILength = IntVar(value=0)
        self.B8_PumpTime = IntVar(value=4000)
        self.B8_calcPumpTime = BooleanVar(value=True)
        self.B8_L1Resp   = IntVar(value=0)
        self.B8_L2Resp   = IntVar(value=0)
        self.B8_Inf    = IntVar(value=0)
        self.B8_SessionTimeStr = StringVar(value="0:0:00")

        self.errorsL1 = IntVar(value=0)
        self.errorsL2 = IntVar(value=0)
        self.recoveriesL1 = IntVar(value=0)
        self.recoveriesL2 = IntVar(value=0)
        self.outputErrors = IntVar(value=0)
        self.outputRecoveries = IntVar(value=0)

        # ********************* Menus ********************
        
        menubar = tkinter.Menu(self.root)
        filemenu = tkinter.Menu(menubar,tearoff=False)
        menubar.add_cascade(label="File",menu=filemenu)
        filemenu.add_command(label="Load from INI File",command = self.loadFromINIFile)
        filemenu.add_command(label="Save to INI File",command = self.writeToINIFile)
        filemenu.add_separator()
        filemenu.add_command(label="Save all Data",command = self.saveAllData)
        
        debugMenu = tkinter.Menu(menubar,tearoff=False)
        menubar.add_cascade(label="Debug",menu=debugMenu)
        debugMenu.add_command(label="Doesn't point to anything")
        debugMenu.add_command(label="Toggle Input Echo",command = self.toggleEchoInput)
        debugMenu.add_command(label="Report Feather M0 Status",command = self.reportPortStatus)
        cumRecMenu = tkinter.Menu(menubar,tearoff=False)
        menubar.add_cascade(label="Cum Rec",menu=cumRecMenu)        
        cumRecMenu.add_command(label="Place holder for X axis")
        cumRecMenu.add_command(label="Place holder for Y axis")
        
        self.root.config(menu=menubar)

        # ****************   ControlFrame - top Row ****************
                                                
        self.ControlFrame = ttk.Frame(self.root, borderwidth=3, relief="sunken")
        self.ControlFrame.grid(column = 0, row = 0, columnspan=4, sticky = (EW))
        
        label1 = ttk.Label(self.ControlFrame, text="Feather M0")
        label1.grid(column = 0, row = 0,pady=5, padx=5)       

        portEntry = ttk.Entry(self.ControlFrame, width=8,textvariable = self.portString)
        portEntry.grid(column = 1, row = 0)
        
        connectButton = ttk.Button(self.ControlFrame,text="Connect",\
                                        command = self.connect)
        connectButton.grid(column = 2, row = 0, pady=10, padx=10)

        self.connectLabelText = StringVar(value="Not Connected")

        connectLabel = ttk.Label(self.ControlFrame, textvariable = self.connectLabelText)
        connectLabel.grid(column = 3, row = 0,pady=5, padx=5)

        label3 = ttk.Label(self.ControlFrame, text="_________________________")
        label3.grid(column = 4, row = 0,pady=5, padx=5) 

        startAllBoxesButton = ttk.Button(self.ControlFrame,text="Start Boxes 1-8", \
                                             command = self.startAllBoxes)
        startAllBoxesButton.grid(column = 6, row = 0, padx = 10, sticky = (E))

        stopAllBoxesButton = ttk.Button(self.ControlFrame,text="Stop Boxes 1-8", \
                                            command = self.stopAllBoxes)
        stopAllBoxesButton.grid(column = 7, row = 0, padx =10, sticky = (E))


        #***************************** Right Frame **********************************************************
                                                
        self.RightFrame = ttk.Frame(self.root, borderwidth=3, relief="sunken")
        self.RightFrame.grid(column = 1, row = 1, sticky = (NS))

        self.counterFrame = ttk.Frame(self.RightFrame,borderwidth=3, relief="sunken")
        self.counterFrame.grid(column = 0, row = 0, sticky = (N))


        # row 1  - labels
        L1_Label = ttk.Label(self.counterFrame, text = " L1 ")
        L1_Label.grid(column = 1, row = 0)
        L2_Label = ttk.Label(self.counterFrame, text = " L2 ")
        L2_Label.grid(column = 2, row = 0)
        Infusion_Label = ttk.Label(self.counterFrame, text = "Inf")
        Infusion_Label.grid(column = 3, row = 0)
        

        B1_ID_Label = ttk.Label(self.counterFrame, width=6, textvariable = self.B1_IDStr)
        B1_ID_Label.grid(column = 0, row = 1, pady=5)    
        B1_L1Resp_Label = ttk.Label(self.counterFrame, textvariable = str(self.B1_L1Resp))
        B1_L1Resp_Label.grid(column = 1, row = 1)
        B1_L2Resp_Label = ttk.Label(self.counterFrame, textvariable = str(self.B1_L2Resp))
        B1_L2Resp_Label.grid(column = 2, row = 1)
        B1_Inf_Label = ttk.Label(self.counterFrame, textvariable = str(self.B1_Inf))
        B1_Inf_Label.grid(column = 3, row = 1)      
        B1_Sched_Label = ttk.Label(self.counterFrame, width=10, textvariable = self.B1_sched)
        B1_Sched_Label.grid(column = 4, row = 1)
        B1_TimeLabel = ttk.Label(self.counterFrame, width=6, textvariable = self.B1_SessionTimeStr)
        B1_TimeLabel.grid(column = 5, row = 1)

        B2_ID_Label = ttk.Label(self.counterFrame, width=6, textvariable = self.B2_IDStr)
        B2_ID_Label.grid(column = 0, row = 2, pady=5)
        B2_L1Resp_Label = ttk.Label(self.counterFrame, textvariable = str(self.B2_L1Resp))
        B2_L1Resp_Label.grid(column = 1, row = 2)
        B2_L2Resp_Label = ttk.Label(self.counterFrame, textvariable = str(self.B2_L2Resp))
        B2_L2Resp_Label.grid(column = 2, row = 2)
        B2_Inf_Label = ttk.Label(self.counterFrame, textvariable = str(self.B2_Inf))
        B2_Inf_Label.grid(column = 3, row = 2)
        B2_Sched_Label = ttk.Label(self.counterFrame, width=10, textvariable = self.B2_sched)
        B2_Sched_Label.grid(column = 4, row = 2)        
        B2_TimeLabel = ttk.Label(self.counterFrame, width=6, textvariable = self.B2_SessionTimeStr)
        B2_TimeLabel.grid(column = 5, row = 2)
 
        B3_ID_Label = ttk.Label(self.counterFrame, width=6, textvariable = self.B3_IDStr)
        B3_ID_Label.grid(column = 0, row = 3, pady=5)
        B3_L1Resp_Label = ttk.Label(self.counterFrame, textvariable = str(self.B3_L1Resp))
        B3_L1Resp_Label.grid(column = 1, row = 3)
        B3_L2Resp_Label = ttk.Label(self.counterFrame, textvariable = str(self.B3_L2Resp))
        B3_L2Resp_Label.grid(column = 2, row = 3)
        B3_Inf_Label = ttk.Label(self.counterFrame, textvariable = str(self.B3_Inf))
        B3_Inf_Label.grid(column = 3, row = 3)
        B3_Sched_Label = ttk.Label(self.counterFrame, width=10, textvariable = self.B3_sched)
        B3_Sched_Label.grid(column = 4, row = 3)
        B3_TimeLabel = ttk.Label(self.counterFrame, width=6, textvariable = self.B3_SessionTimeStr)
        B3_TimeLabel.grid(column = 5, row = 3)

        B4_ID_Label = ttk.Label(self.counterFrame, width=6, textvariable = self.B4_IDStr)
        B4_ID_Label.grid(column = 0, row = 4, pady=5)
        B4_L1Resp_Label = ttk.Label(self.counterFrame, textvariable = str(self.B4_L1Resp))
        B4_L1Resp_Label.grid(column = 1, row = 4)
        B4_L2Resp_Label = ttk.Label(self.counterFrame, textvariable = str(self.B4_L2Resp))
        B4_L2Resp_Label.grid(column = 2, row = 4)
        B4_Inf_Label = ttk.Label(self.counterFrame, textvariable = str(self.B4_Inf))
        B4_Inf_Label.grid(column = 3, row = 4)
        B4_Sched_Label = ttk.Label(self.counterFrame, width=10, textvariable = self.B4_sched)
        B4_Sched_Label.grid(column = 4, row = 4)
        B4_TimeLabel = ttk.Label(self.counterFrame, width=6, textvariable = self.B4_SessionTimeStr)
        B4_TimeLabel.grid(column = 5, row = 4)

        B5_ID_Label = ttk.Label(self.counterFrame, width=6, textvariable = self.B5_IDStr)
        B5_ID_Label.grid(column = 0, row = 5, pady=5)
        B5_L1Resp_Label = ttk.Label(self.counterFrame, textvariable = str(self.B5_L1Resp))
        B5_L1Resp_Label.grid(column = 1, row = 5)        
        B5_L2Resp_Label = ttk.Label(self.counterFrame, textvariable = str(self.B5_L2Resp))
        B5_L2Resp_Label.grid(column = 2, row = 5)
        B5_Inf_Label = ttk.Label(self.counterFrame, textvariable = str(self.B5_Inf))
        B5_Inf_Label.grid(column = 3, row = 5)
        B5_Sched_Label = ttk.Label(self.counterFrame, width=10, textvariable = self.B5_sched)
        B5_Sched_Label.grid(column = 4, row = 5)
        B5_TimeLabel = ttk.Label(self.counterFrame, width=6, textvariable = self.B5_SessionTimeStr)
        B5_TimeLabel.grid(column = 5, row = 5)

        B6_ID_Label = ttk.Label(self.counterFrame, width=6, textvariable = self.B6_IDStr)
        B6_ID_Label.grid(column = 0, row = 6, pady=5)
        B6_L1Resp_Label = ttk.Label(self.counterFrame, textvariable = str(self.B6_L1Resp))
        B6_L1Resp_Label.grid(column = 1, row = 6)        
        B6_L2Resp_Label = ttk.Label(self.counterFrame, textvariable = str(self.B6_L2Resp))
        B6_L2Resp_Label.grid(column = 2, row = 6)
        B6_Inf_Label = ttk.Label(self.counterFrame, textvariable = str(self.B6_Inf))
        B6_Inf_Label.grid(column = 3, row = 6)
        B6_Sched_Label = ttk.Label(self.counterFrame, width=10, textvariable = self.B6_sched)
        B6_Sched_Label.grid(column = 4, row = 6)
        B6_TimeLabel = ttk.Label(self.counterFrame, width=6, textvariable = self.B6_SessionTimeStr)
        B6_TimeLabel.grid(column = 5, row = 6)

        B7_ID_Label = ttk.Label(self.counterFrame, width=6, textvariable = self.B7_IDStr)
        B7_ID_Label.grid(column = 0, row = 7, pady=5)
        B7_L1Resp_Label = ttk.Label(self.counterFrame, textvariable = str(self.B7_L1Resp))
        B7_L1Resp_Label.grid(column = 1, row = 7)
        B7_L2Resp_Label = ttk.Label(self.counterFrame, textvariable = str(self.B7_L2Resp))
        B7_L2Resp_Label.grid(column = 2, row = 7)
        B7_Inf_Label = ttk.Label(self.counterFrame, textvariable = str(self.B7_Inf))
        B7_Inf_Label.grid(column = 3, row = 7)
        B7_Sched_Label = ttk.Label(self.counterFrame, width=10, textvariable = self.B7_sched)
        B7_Sched_Label.grid(column = 4, row = 7)
        B7_TimeLabel = ttk.Label(self.counterFrame, width=6, textvariable = self.B7_SessionTimeStr)
        B7_TimeLabel.grid(column = 5, row = 7)

        B8_ID_Label = ttk.Label(self.counterFrame, width=6, textvariable = self.B8_IDStr)
        B8_ID_Label.grid(column = 0, row = 8, pady=5)
        B8_L1Resp_Label = ttk.Label(self.counterFrame, textvariable = str(self.B8_L1Resp))
        B8_L1Resp_Label.grid(column = 1, row = 8)
        B8_L2Resp_Label = ttk.Label(self.counterFrame, textvariable = str(self.B8_L2Resp))
        B8_L2Resp_Label.grid(column = 2, row = 8)
        B8_Inf_Label = ttk.Label(self.counterFrame, textvariable = str(self.B8_Inf))
        B8_Inf_Label.grid(column = 3, row = 8)
        B8_Sched_Label = ttk.Label(self.counterFrame, width=10, textvariable = self.B8_sched)
        B8_Sched_Label.grid(column = 4, row = 8)
        B8_TimeLabel = ttk.Label(self.counterFrame, width=6, textvariable = self.B8_SessionTimeStr)
        B8_TimeLabel.grid(column = 5, row = 8)

        columnLabel1 = ttk.Label(self.counterFrame, text = "Errors")
        columnLabel1.grid(column = 1, row = 10, sticky = (EW))
        columnLabel2 = ttk.Label(self.counterFrame, text = "Recoveries")
        columnLabel2.grid(column = 2, row = 10, sticky = (EW))

        L1Label = ttk.Label(self.counterFrame, text = "Lever 1")
        L1Label.grid(column = 0, row = 11)
        errorsL1Label = ttk.Label(self.counterFrame, textvariable = str(self.errorsL1))
        errorsL1Label.grid(column = 1, row = 11)
        recoveriesL1Label = ttk.Label(self.counterFrame, textvariable = str(self.recoveriesL1))
        recoveriesL1Label.grid(column = 2, row = 11)        

        L2Label = ttk.Label(self.counterFrame, text = "Lever 2")
        L2Label.grid(column = 0, row = 12)
        errorsL2Label = ttk.Label(self.counterFrame, textvariable = str(self.errorsL2))
        errorsL2Label.grid(column = 1, row = 12)
        recoveriesL2Label = ttk.Label(self.counterFrame, textvariable = str(self.recoveriesL2))
        recoveriesL2Label.grid(column = 2, row = 12) 

        outputLabel = ttk.Label(self.counterFrame, text = "Outputs")
        outputLabel.grid(column = 0, row = 13)
        outputErrorsLabel = ttk.Label(self.counterFrame, textvariable = str(self.outputErrors))
        outputErrorsLabel.grid(column = 1, row = 13)
        outputRecoveriesLabel = ttk.Label(self.counterFrame, textvariable = str(self.outputRecoveries))
        outputRecoveriesLabel.grid(column = 2, row = 13) 
                               
        # ********************** noteBookFrame *****************************************

        noteBookFrame = Frame(self.root, borderwidth=0, relief="sunken")
        noteBookFrame.grid(column = 0, row = 1)
        myNotebook = ttk.Notebook(noteBookFrame)
        self.iniTab = Frame(myNotebook)
        self.graphTab = Frame(myNotebook)
        self.diagnosticTab = Frame(myNotebook)
        myNotebook.add(self.iniTab,text = "Initialization")
        myNotebook.add(self.graphTab,text = "Graphs")      
        myNotebook.add(self.diagnosticTab,text = "Diagnostics")
        myNotebook.grid(row=0,column=0)

        # *********************  GraphTab **********************************************

        self.GraphFrame = ttk.Frame(self.graphTab,borderwidth=3, relief="sunken")
        self.GraphFrame.grid(column = 0, row = 0,rowspan=1,sticky = (N,E,W,S))
        
        self.graphButtonFrame = ttk.Frame(self.GraphFrame,borderwidth=3, relief="sunken")
        self.graphButtonFrame.grid(column = 0, row = 1, sticky = (N))
        B1_Radiobutton = ttk.Radiobutton(self.graphButtonFrame, text="Box 1", variable=self.selectedBox, value=0)
        B1_Radiobutton.grid(column = 0, row = 0)
        B2_Radiobutton = ttk.Radiobutton(self.graphButtonFrame, text="Box 2", variable=self.selectedBox, value=1)
        B2_Radiobutton.grid(column = 1, row = 0)
        B3_Radiobutton = ttk.Radiobutton(self.graphButtonFrame, text="Box 3", variable=self.selectedBox, value=2)
        B3_Radiobutton.grid(column = 2, row = 0)
        B4_Radiobutton = ttk.Radiobutton(self.graphButtonFrame, text="Box 4", variable=self.selectedBox, value=3)
        B4_Radiobutton.grid(column = 3, row = 0)
        B5_Radiobutton = ttk.Radiobutton(self.graphButtonFrame, text="Box 5", variable=self.selectedBox, value=4)
        B5_Radiobutton.grid(column = 4, row = 0)
        B6_Radiobutton = ttk.Radiobutton(self.graphButtonFrame, text="Box 6", variable=self.selectedBox, value=5)
        B6_Radiobutton.grid(column = 5, row = 0)
        B7_Radiobutton = ttk.Radiobutton(self.graphButtonFrame, text="Box 7", variable=self.selectedBox, value=6)
        B7_Radiobutton.grid(column = 6, row = 0)
        B8_Radiobutton = ttk.Radiobutton(self.graphButtonFrame, text="Box 8", variable=self.selectedBox, value=7)
        B8_Radiobutton.grid(column = 7, row = 0)
        example1_Radiobutton = ttk.Radiobutton(self.graphButtonFrame, text="PR", variable=self.selectedBox, value=8)
        example1_Radiobutton.grid(column = 8, row = 0)
        example2_Radiobutton = ttk.Radiobutton(self.graphButtonFrame, text="Errors", variable=self.selectedBox, value=9)
        example2_Radiobutton.grid(column = 9, row = 0)

        self.graphButtonFrame = ttk.Frame(self.GraphFrame,borderwidth=3, relief="sunken")
        self.graphButtonFrame.grid(column = 0, row = 2, columnspan = 10)
        topTimeStampButton = ttk.Button(self.graphButtonFrame,text="Timestamps",command=lambda: \
                self.drawAllTimeStamps(self.topCanvas, self.selectedBox.get(),self.selectMax_x_Scale.get()))
        topTimeStampButton.grid(column = 0, row = 0)
        topCumRecButton = ttk.Button(self.graphButtonFrame,text="Cum Rec",command=lambda: \
                self.drawCumulativeRecord(self.topCanvas, self.selectedBox.get(),self.selectMax_x_Scale.get()))
        topCumRecButton.grid(column = 1, row = 0)        
        topEventButton = ttk.Button(self.graphButtonFrame, text="Events",  command=lambda: self.drawEventRecords())
        topEventButton.grid(column = 2, row = 0)

        """
        sessionLogTimeStampButton = ttk.Button(self.graphButtonFrame,text="SessionLog",command=lambda: \
                self.drawSessionLogTimeStamps())
        sessionLogTimeStampButton.grid(column = 3, row = 0)
        """
        
        topClearButton = ttk.Button(self.graphButtonFrame,text="Clear Canvas", \
                command=lambda Canvas = 0: self.clearCanvas(Canvas))
        topClearButton.grid(column = 4, row = 0)

        self.topCanvas = Canvas(self.GraphFrame,width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        self.topCanvas.grid(column = 0, row = 3, columnspan = 10, stick = (W))
        self.topCanvas.create_text(150, 10, fill="blue", text="topCanvas")
    

        self.graphControlFrame = ttk.Frame(self.GraphFrame,borderwidth=3, relief="sunken")
        self.graphControlFrame.grid(column = 0, row = 4, columnspan = 10, sticky = (S))
        X_Axis_Label = ttk.Label(self.graphControlFrame, text="X Axis scales (min)")
        X_Axis_Label.grid(column = 0, row = 2)
        topRadiobutton30 = ttk.Radiobutton(self.graphControlFrame, text="10", variable=self.selectMax_x_Scale, value=10)
        topRadiobutton30.grid(column = 1, row = 2)
        topRadiobutton30 = ttk.Radiobutton(self.graphControlFrame, text="30", variable=self.selectMax_x_Scale, value=30)
        topRadiobutton30.grid(column = 2, row = 2)
        topRadiobutton60 = ttk.Radiobutton(self.graphControlFrame, text="60", variable=self.selectMax_x_Scale, value=60)
        topRadiobutton60.grid(column = 3, row = 2)
        topRadiobutton180 = ttk.Radiobutton(self.graphControlFrame, text="180", variable=self.selectMax_x_Scale, value=180)
        topRadiobutton180.grid(column = 4, row = 2)
        topRadiobutton180 = ttk.Radiobutton(self.graphControlFrame, text="360", variable=self.selectMax_x_Scale, value=360)
        topRadiobutton180.grid(column = 5, row = 2)


        # ********************** Text Boxes - DiagnosticsTab ****************************************
        self.diagnosticFrame = ttk.Frame(self.diagnosticTab,borderwidth=3, relief="sunken")
        self.diagnosticFrame.grid(column = 0, row = 0,rowspan=1, sticky = (N,E,W,S))

        self.diagnostic_IO_Frame = ttk.Frame(self.diagnosticFrame,borderwidth=3, relief="sunken")
        self.diagnostic_IO_Frame.grid(column = 0, row = 0, columnspan = 2, sticky = (W))

        B1_Lever1CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "L1", variable = self.B1_lever1CheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.moveLever1(0,self.B1_lever1CheckVar.get())).grid(column = 1, row = 0)
        B1_Lever2CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "L2", variable = self.B1_lever2CheckVar, \
             onvalue = True, offvalue = False, command=lambda: self.moveLever2(0,self.B1_lever2CheckVar.get())).grid(column = 2, row = 0)
        B1_PumpCheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "Pump", variable = self.B1_pumpCheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.togglePump(0,self.B1_pumpCheckVar.get())).grid(column = 3, row = 0)
        B1_LED1_CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "LED1", variable = self.B1_LED1CheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.toggleLED1(0,self.B1_LED1CheckVar.get())).grid(column = 4, row = 0)
        B1_LED2_CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "LED2", variable = self.B1_LED2CheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.toggleLED2(0,self.B1_LED2CheckVar.get())).grid(column = 5, row = 0)
        B1_L1_TestButton = ttk.Button(self.diagnostic_IO_Frame,text="L1 test", command=lambda: self.sendCode("<L1 0>")).grid(column = 6, row = 0)
        # B1_L2_TestButton = ttk.Button(self.diagnostic_IO_Frame,text="L2 test", command=lambda: self.mimicL2Response(0)).grid(column = 7, row = 0)

        B2_Lever1CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "L1", variable = self.B2_lever1CheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.moveLever1(1,self.B2_lever1CheckVar.get())).grid(column = 1, row = 1)
        B2_Lever2CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "L2", variable = self.B2_lever2CheckVar, \
             onvalue = True, offvalue = False, command=lambda: self.moveLever2(1,self.B2_lever2CheckVar.get())).grid(column = 2, row = 1)
        B2_PumpCheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "Pump", variable = self.B2_pumpCheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.togglePump(1,self.B2_pumpCheckVar.get())).grid(column = 3, row = 1)
        B2_LED1_CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "LED1", variable = self.B2_LED1CheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.toggleLED1(1,self.B2_LED1CheckVar.get())).grid(column = 4, row = 1)
        B2_LED2_CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "LED2", variable = self.B2_LED2CheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.toggleLED2(1,self.B2_LED2CheckVar.get())).grid(column = 5, row = 1)
        B2_L1_TestButton = ttk.Button(self.diagnostic_IO_Frame,text="L2 test", command=lambda: self.sendCode("<L1 1>")).grid(column = 6, row = 1)        

        B3_Lever1CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "L1", variable = self.B3_lever1CheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.moveLever1(2,self.B3_lever1CheckVar.get())).grid(column = 1, row = 2)
        B3_Lever2CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "L2", variable = self.B3_lever2CheckVar, \
             onvalue = True, offvalue = False, command=lambda: self.moveLever2(2,self.B3_lever2CheckVar.get())).grid(column = 2, row = 2)
        B3_PumpCheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "Pump", variable = self.B3_pumpCheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.togglePump(2,self.B3_pumpCheckVar.get())).grid(column = 3, row = 2)
        B3_LED1_CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "LED1", variable = self.B3_LED1CheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.toggleLED1(2,self.B3_LED1CheckVar.get())).grid(column = 4, row = 2)
        B3_LED2_CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "LED2", variable = self.B3_LED2CheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.toggleLED2(2,self.B3_LED2CheckVar.get())).grid(column = 5, row = 2)
        B3_L1_TestButton = ttk.Button(self.diagnostic_IO_Frame,text="L3 test", command=lambda: self.sendCode("<L1 2>")).grid(column = 6, row = 2)

        B4_Lever1CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "L1", variable = self.B4_lever1CheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.moveLever1(3,self.B4_lever1CheckVar.get())).grid(column = 1, row = 3)
        B4_Lever2CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "L2", variable = self.B4_lever2CheckVar, \
             onvalue = True, offvalue = False, command=lambda: self.moveLever2(3,self.B4_lever2CheckVar.get())).grid(column = 2, row = 3)
        B4_PumpCheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "Pump", variable = self.B4_pumpCheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.togglePump(3,self.B4_pumpCheckVar.get())).grid(column = 3, row = 3)
        B4_LED1_CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "LED1", variable = self.B4_LED1CheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.toggleLED1(3,self.B4_LED1CheckVar.get())).grid(column = 4, row = 3)
        B4_LED2_CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "LED2", variable = self.B4_LED2CheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.toggleLED2(3,self.B4_LED2CheckVar.get())).grid(column = 5, row = 3)
        B4_L1_TestButton = ttk.Button(self.diagnostic_IO_Frame,text="L4 test", command=lambda: self.sendCode("<L1 3>")).grid(column = 6, row = 3)

        B5_Lever1CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "L1", variable = self.B5_lever1CheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.moveLever1(4,self.B5_lever1CheckVar.get())).grid(column = 1, row = 4)
        B5_Lever2CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "L2", variable = self.B5_lever2CheckVar, \
             onvalue = True, offvalue = False, command=lambda: self.moveLever2(4,self.B5_lever2CheckVar.get())).grid(column = 2, row = 4)
        B5_PumpCheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "Pump", variable = self.B5_pumpCheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.togglePump(4,self.B5_pumpCheckVar.get())).grid(column = 3, row = 4)
        B5_LED1_CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "LED1", variable = self.B5_LED1CheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.toggleLED1(4,self.B5_LED1CheckVar.get())).grid(column = 4, row = 4)
        B5_LED2_CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "LED2", variable = self.B5_LED2CheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.toggleLED2(4,self.B5_LED2CheckVar.get())).grid(column = 5, row = 4)
        B5_L1_TestButton = ttk.Button(self.diagnostic_IO_Frame,text="L5 test", command=lambda: self.sendCode("<L1 4>")).grid(column = 6, row = 4)

        B6_Lever1CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "L1", variable = self.B6_lever1CheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.moveLever1(5,self.B6_lever1CheckVar.get())).grid(column = 1, row = 5)
        B6_Lever2CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "L2", variable = self.B6_lever2CheckVar, \
             onvalue = True, offvalue = False, command=lambda: self.moveLever2(5,self.B6_lever2CheckVar.get())).grid(column = 2, row = 5)
        B6_PumpCheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "Pump", variable = self.B6_pumpCheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.togglePump(5,self.B6_pumpCheckVar.get())).grid(column = 3, row = 5)
        B6_LED1_CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "LED1", variable = self.B6_LED1CheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.toggleLED1(5,self.B6_LED1CheckVar.get())).grid(column = 4, row = 5)
        B6_LED2_CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "LED2", variable = self.B6_LED2CheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.toggleLED2(5,self.B6_LED2CheckVar.get())).grid(column = 5, row = 5)
        B6_L1_TestButton = ttk.Button(self.diagnostic_IO_Frame,text="L6 test", command=lambda: self.sendCode("<L1 5>")).grid(column = 6, row = 5)

        B7_Lever1CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "L1", variable = self.B7_lever1CheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.moveLever1(6,self.B7_lever1CheckVar.get())).grid(column = 1, row = 6)
        B7_Lever2CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "L2", variable = self.B7_lever2CheckVar, \
             onvalue = True, offvalue = False, command=lambda: self.moveLever2(6,self.B7_lever2CheckVar.get())).grid(column = 2, row = 6)
        B7_PumpCheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "Pump", variable = self.B7_pumpCheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.togglePump(6,self.B7_pumpCheckVar.get())).grid(column = 3, row = 6)        
        B7_LED1_CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "LED1", variable = self.B7_LED1CheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.toggleLED1(6,self.B7_LED1CheckVar.get())).grid(column = 4, row = 6)
        B7_LED2_CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "LED2", variable = self.B7_LED2CheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.toggleLED2(6,self.B7_LED2CheckVar.get())).grid(column = 5, row = 6)
        B7_L1_TestButton = ttk.Button(self.diagnostic_IO_Frame,text="L7 test", command=lambda: self.sendCode("<L1 6>")).grid(column = 6, row = 6)

        B8_Lever1CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "L1", variable = self.B8_lever1CheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.moveLever1(7,self.B8_lever1CheckVar.get())).grid(column = 1, row = 7)
        B8_Lever2CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "L2", variable = self.B8_lever2CheckVar, \
             onvalue = True, offvalue = False, command=lambda: self.moveLever2(7,self.B8_lever2CheckVar.get())).grid(column = 2, row = 7)
        B8_PumpCheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "Pump", variable = self.B8_pumpCheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.togglePump(7,self.B8_pumpCheckVar.get())).grid(column = 3, row = 7)
        B8_LED1_CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "LED1", variable = self.B8_LED1CheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.toggleLED1(7,self.B8_LED1CheckVar.get())).grid(column = 4, row = 7)
        B8_LED2_CheckButton = Checkbutton(self.diagnostic_IO_Frame, text = "LED2", variable = self.B8_LED2CheckVar, \
                onvalue = True, offvalue = False, command=lambda: self.toggleLED2(7,self.B8_LED2CheckVar.get())).grid(column = 5, row = 7)
        B8_L1_TestButton = ttk.Button(self.diagnostic_IO_Frame,text="L8 test", command=lambda: self.sendCode("<L1 7>")).grid(column = 6, row = 7)

        self.startStopButtonFrame = ttk.Frame(self.diagnosticFrame,borderwidth=3, relief="sunken")
        self.startStopButtonFrame.grid(column = 2, row = 0, sticky = (N))

        B1_StartButton = ttk.Button(self.startStopButtonFrame,text="Start", \
                command=lambda boxIndex = 0: self.startSession(boxIndex)).grid(column = 0, row = 0)
        B1_StopButton = ttk.Button(self.startStopButtonFrame,text="Stop", \
                command=lambda boxIndex = 0: self.stopSession(boxIndex)).grid(column = 1, row = 0) 

        B2_StartButton = ttk.Button(self.startStopButtonFrame,text="Start", \
                command=lambda boxIndex = 1: self.startSession(boxIndex)).grid(column = 0, row = 1)
        B2_StopButton = ttk.Button(self.startStopButtonFrame,text="Stop", \
                command=lambda boxIndex = 1: self.stopSession(boxIndex)).grid(column = 1, row = 1)

        B3_StartButton = ttk.Button(self.startStopButtonFrame,text="Start", \
                command=lambda boxIndex = 2: self.startSession(boxIndex)).grid(column = 0, row = 2)
        B3_StopButton = ttk.Button(self.startStopButtonFrame,text="Stop", \
                command=lambda boxIndex = 2: self.stopSession(boxIndex)).grid(column = 1, row = 2)

        B4_StartButton = ttk.Button(self.startStopButtonFrame,text="Start", \
                command=lambda boxIndex = 3: self.startSession(boxIndex)).grid(column = 0, row = 3)
        B4_StopButton = ttk.Button(self.startStopButtonFrame,text="Stop", \
                command=lambda boxIndex = 3: self.stopSession(boxIndex)).grid(column = 1, row = 3)

        B5_StartButton = ttk.Button(self.startStopButtonFrame,text="Start", \
                command=lambda boxIndex = 4: self.startSession(boxIndex)).grid(column = 0, row = 4)
        B5_StopButton = ttk.Button(self.startStopButtonFrame,text="Stop", \
                command=lambda boxIndex = 4: self.stopSession(boxIndex)).grid(column = 1, row = 4)

        B6_StartButton = ttk.Button(self.startStopButtonFrame,text="Start", \
                command=lambda boxIndex = 5: self.startSession(boxIndex)).grid(column = 0, row = 5)
        B6_StopButton = ttk.Button(self.startStopButtonFrame,text="Stop", \
                command=lambda boxIndex = 5: self.stopSession(boxIndex)).grid(column = 1, row = 5)

        B7_StartButton = ttk.Button(self.startStopButtonFrame,text="Start", \
                command=lambda boxIndex = 6: self.startSession(boxIndex)).grid(column = 0, row = 6)
        B7_StopButton = ttk.Button(self.startStopButtonFrame,text="Stop", \
                command=lambda boxIndex = 6: self.stopSession(boxIndex)).grid(column = 1, row = 6)

        B8_StartButton = ttk.Button(self.startStopButtonFrame,text="Start", \
                command=lambda boxIndex = 7: self.startSession(boxIndex)).grid(column = 0, row = 7)
        B8_StopButton = ttk.Button(self.startStopButtonFrame,text="Stop", \
                command=lambda boxIndex = 7: self.stopSession(boxIndex)).grid(column = 1, row = 7) 

        self.diagnosticButtonFrame = ttk.Frame(self.diagnosticFrame,borderwidth=3, relief="sunken")
        self.diagnosticButtonFrame.grid(column = 0, row = 1, sticky = (N))
        
        testButton1 = ttk.Button(self.diagnosticButtonFrame,text="Report Parameters", command = self.reportParameters)
        testButton1.grid(column = 0, row = 1, columnspan = 2)
        testButton2 = ttk.Button(self.diagnosticButtonFrame,text="resetChips()",command = self.resetChips)
        testButton2.grid(column = 0, row = 2, sticky = (EW))
        testButton3 = ttk.Button(self.diagnosticButtonFrame,text="Abort All!",command = self.abort)
        testButton3.grid(column = 1, row = 2, sticky = (EW))
        testButton4 = ttk.Button(self.diagnosticButtonFrame,text="checkOutputPorts()",command = self.checkOutputPorts)
        testButton4.grid(column = 0, row = 3, sticky = (EW))        
        testButton5 = ttk.Button(self.diagnosticButtonFrame,text="Diagnostics",command = self.diagnostics)
        testButton5.grid(column = 1, row = 3, sticky = (EW))
        testButton6 = ttk.Button(self.diagnosticButtonFrame,text="printSessionLog()",command = self.printSessionLog)
        testButton6.grid(column = 0, row = 4, sticky = (EW))        
        testButton7 = ttk.Button(self.diagnosticButtonFrame,text="test1()",command = self.testFunction1)
        testButton7.grid(column = 1, row = 4, sticky = (EW))


        # Eight tkinter boolean vars widgets

        sys0label = ttk.Label(self.diagnosticButtonFrame, text="CheckL1")
        sys0label.grid(column = 0, row = 7, sticky = (W))
        sys0FalseRadiobutton = ttk.Radiobutton(self.diagnosticButtonFrame, text="False", variable=self.sys0CheckVar, value=0)
        sys0FalseRadiobutton.grid(column = 1, row = 7, sticky = (W))
        sys0TrueRadiobutton = ttk.Radiobutton(self.diagnosticButtonFrame, text="True", variable=self.sys0CheckVar, value=1)
        sys0TrueRadiobutton.grid(column = 2, row = 7, sticky = (W))

        sys1label = ttk.Label(self.diagnosticButtonFrame, text="CheckL2")
        sys1label.grid(column = 0, row = 8, sticky = (W))
        sys1FalseRadiobutton = ttk.Radiobutton(self.diagnosticButtonFrame, text="False", variable=self.sys1CheckVar, value=0)
        sys1FalseRadiobutton.grid(column = 1, row = 8, sticky = (W))
        sys1TrueRadiobutton = ttk.Radiobutton(self.diagnosticButtonFrame, text="True", variable=self.sys1CheckVar, value=1)
        sys1TrueRadiobutton.grid(column = 2, row = 8, sticky = (W))

        sys2label = ttk.Label(self.diagnosticButtonFrame, text="checkOutputs")
        sys2label.grid(column = 0, row = 9, sticky = (W))
        sys2FalseRadiobutton = ttk.Radiobutton(self.diagnosticButtonFrame, text="False", variable=self.sys2CheckVar, value=0)
        sys2FalseRadiobutton.grid(column = 1, row = 9, sticky = (W))
        sys2TrueRadiobutton = ttk.Radiobutton(self.diagnosticButtonFrame, text="True", variable=self.sys2CheckVar, value=1)
        sys2TrueRadiobutton.grid(column = 2, row = 9, sticky = (W))

        sys3label = ttk.Label(self.diagnosticButtonFrame, text="abortEnabled")
        sys3label.grid(column = 0, row = 10, sticky = (W))
        sys3FalseRadiobutton = ttk.Radiobutton(self.diagnosticButtonFrame, text="False", variable=self.sys3CheckVar, value=0)
        sys3FalseRadiobutton.grid(column = 1, row = 10, sticky = (W))
        sys3TrueRadiobutton = ttk.Radiobutton(self.diagnosticButtonFrame, text="True", variable=self.sys3CheckVar, value=1)
        sys3TrueRadiobutton.grid(column = 2, row = 10, sticky = (W))

        sys4label = ttk.Label(self.diagnosticButtonFrame, text="send maxDelta")
        sys4label.grid(column = 0, row = 11, sticky = (W))
        sys4FalseRadiobutton = ttk.Radiobutton(self.diagnosticButtonFrame, text="False", variable=self.sys4CheckVar, value=0)
        sys4FalseRadiobutton.grid(column = 1, row = 11, sticky = (W))
        sys4TrueRadiobutton = ttk.Radiobutton(self.diagnosticButtonFrame, text="True", variable=self.sys4CheckVar, value=1)
        sys4TrueRadiobutton.grid(column = 2, row = 11, sticky = (W))

        sys5label = ttk.Label(self.diagnosticButtonFrame, text="verbose")
        sys5label.grid(column = 0, row = 12, sticky = (W))
        sys5FalseRadiobutton = ttk.Radiobutton(self.diagnosticButtonFrame, text="False", variable=self.sys5CheckVar, value=0)
        sys5FalseRadiobutton.grid(column = 1, row = 12, sticky = (W))
        sys5TrueRadiobutton = ttk.Radiobutton(self.diagnosticButtonFrame, text="True", variable=self.sys5CheckVar, value=1)
        sys5TrueRadiobutton.grid(column = 2, row = 12, sticky = (W))

        sys6label = ttk.Label(self.diagnosticButtonFrame, text="showDebugOutput")
        sys6label.grid(column = 0, row = 13, sticky = (W))
        sys6FalseRadiobutton = ttk.Radiobutton(self.diagnosticButtonFrame, text="False", variable=self.sys6CheckVar, value=0)
        sys6FalseRadiobutton.grid(column = 1, row = 13, sticky = (W))
        sys6TrueRadiobutton = ttk.Radiobutton(self.diagnosticButtonFrame, text="True", variable=self.sys6CheckVar, value=1)
        sys6TrueRadiobutton.grid(column = 2, row = 13, sticky = (W))

        sys7label = ttk.Label(self.diagnosticButtonFrame, text="Label7")
        sys7label.grid(column = 0, row = 14, sticky = (W))
        sys7FalseRadiobutton = ttk.Radiobutton(self.diagnosticButtonFrame, text="False", variable=self.sys7CheckVar, value=0)
        sys7FalseRadiobutton.grid(column = 1, row = 14, sticky = (W))
        sys7TrueRadiobutton = ttk.Radiobutton(self.diagnosticButtonFrame, text="True", variable=self.sys7CheckVar, value=1)
        sys7TrueRadiobutton.grid(column = 2, row = 14, sticky = (W))

        sendConfigButton = ttk.Button(self.diagnosticButtonFrame,text="Send config",command = self.sendSysVars)
        sendConfigButton.grid(column = 0, row = 15, columnspan = 3)

        # ***************************************************************************************
               
        self.topTextFrame = ttk.Frame(self.diagnosticFrame,borderwidth=3, relief="sunken")
        self.topTextFrame.grid(column = 1, row = 1)
        showDataStreamCheckButton = Checkbutton(self.topTextFrame, text = "Show Data Steam", variable = self.showDataStreamCheckVar, \
                onvalue = True, offvalue = False)
        showDataStreamCheckButton.grid(column = 0, row = 0, sticky = (EW))       
        self.topTextbox = tkinter.scrolledtext.ScrolledText(self.topTextFrame,height=20,width= 25)
        self.topTextbox.grid(column = 0, row = 1,sticky = (N))
        self.topTextbox.insert('1.0',"\n")
        self.bottomTextFrame = ttk.Frame(self.diagnosticFrame,borderwidth=3, relief="sunken")
        self.bottomTextFrame.grid(column = 2, row = 1)
        showOutputStreamCheckButton = Checkbutton(self.bottomTextFrame, text = "Show Output", variable = self.showOutputCheckVar, \
                onvalue = True, offvalue = False)
        showOutputStreamCheckButton.grid(column = 0, row = 0, sticky = (EW)) 
        self.bottomTextbox = tkinter.scrolledtext.ScrolledText(self.bottomTextFrame,height=20,width= 25)
        self.bottomTextbox.grid(column = 0, row = 1,sticky = (N))        
        self.bottomTextbox.insert('1.0',"Text Box\n")


        # ********************** Lists used to read and write to initialization file ******************
        self.IDStrList = [self.B1_IDStr, self.B2_IDStr, self.B3_IDStr, self.B4_IDStr, \
                          self.B5_IDStr, self.B6_IDStr, self.B7_IDStr, self.B8_IDStr]
        self.WeightList = [self.B1_Weight,self.B2_Weight,self.B3_Weight,self.B4_Weight, \
                           self.B5_Weight,self.B6_Weight,self.B7_Weight,self.B8_Weight]
        self.schedList = [self.B1_sched,self.B2_sched,self.B3_sched,self.B4_sched, \
                          self.B5_sched,self.B6_sched,self.B7_sched,self.B8_sched, ]
        self.paramNumList = [self.B1_Param_value,self.B2_Param_value,self.B3_Param_value,self.B4_Param_value, \
                             self.B5_Param_value,self.B6_Param_value,self.B7_Param_value,self.B8_Param_value,]
        self.SessionLengthList = [self.B1_SessionLength,self.B2_SessionLength,self.B3_SessionLength,self.B4_SessionLength, \
                                  self.B5_SessionLength,self.B6_SessionLength,self.B7_SessionLength,self.B8_SessionLength]
        self.IBILengthList = [self.B1_IBILength,self.B2_IBILength,self.B3_IBILength,self.B4_IBILength, \
                                  self.B5_IBILength,self.B6_IBILength,self.B7_IBILength,self.B8_IBILength]
        self.PumpTimeList = [self.B1_PumpTime,self.B2_PumpTime,self.B3_PumpTime,self.B4_PumpTime, \
                             self.B5_PumpTime,self.B6_PumpTime,self.B7_PumpTime,self.B8_PumpTime,]
        self.calcPumpTimeList = [self.B1_calcPumpTime,self.B2_calcPumpTime,self.B3_calcPumpTime,self.B4_calcPumpTime, \
                                 self.B5_calcPumpTime,self.B6_calcPumpTime,self.B7_calcPumpTime,self.B8_calcPumpTime,]

        # ********************* Lists used in periodic check  ****************************************

        self.B1_boolVarList = [self.B1_lever1CheckVar, self.B1_lever2CheckVar, self.B1_pumpCheckVar, self.B1_LED1CheckVar, self.B1_LED2CheckVar]
        self.B2_boolVarList = [self.B2_lever1CheckVar, self.B2_lever2CheckVar, self.B2_pumpCheckVar, self.B2_LED1CheckVar, self.B2_LED2CheckVar]
        self.B3_boolVarList = [self.B3_lever1CheckVar, self.B3_lever2CheckVar, self.B3_pumpCheckVar, self.B3_LED1CheckVar, self.B3_LED2CheckVar]
        self.B4_boolVarList = [self.B4_lever1CheckVar, self.B4_lever2CheckVar, self.B4_pumpCheckVar, self.B4_LED1CheckVar, self.B4_LED2CheckVar]
        self.B5_boolVarList = [self.B5_lever1CheckVar, self.B5_lever2CheckVar, self.B5_pumpCheckVar, self.B5_LED1CheckVar, self.B5_LED2CheckVar]
        self.B6_boolVarList = [self.B6_lever1CheckVar, self.B6_lever2CheckVar, self.B6_pumpCheckVar, self.B6_LED1CheckVar, self.B6_LED2CheckVar]
        self.B7_boolVarList = [self.B7_lever1CheckVar, self.B7_lever2CheckVar, self.B7_pumpCheckVar, self.B7_LED1CheckVar, self.B7_LED2CheckVar]
        self.B8_boolVarList = [self.B8_lever1CheckVar, self.B8_lever2CheckVar, self.B8_pumpCheckVar, self.B8_LED1CheckVar, self.B8_LED2CheckVar]

        self.sysVarList = [self.sys0CheckVar, self.sys1CheckVar, self.sys2CheckVar, self.sys3CheckVar, \
                           self.sys4CheckVar, self.sys5CheckVar, self.sys6CheckVar, self.sys7CheckVar]
        
        self.boolVarLists = [self.B1_boolVarList,self.B2_boolVarList,self.B3_boolVarList,self.B4_boolVarList, \
                              self.B5_boolVarList,self.B6_boolVarList,self.B7_boolVarList,self.B8_boolVarList, \
                              self.sysVarList]
        self.L1ResponsesList = [self.B1_L1Resp,self.B2_L1Resp,self.B3_L1Resp,self.B4_L1Resp, \
                              self.B5_L1Resp,self.B6_L1Resp,self.B7_L1Resp,self.B8_L1Resp]
        self.L2ResponsesList = [self.B1_L2Resp,self.B2_L2Resp,self.B3_L2Resp,self.B4_L2Resp, \
                              self.B5_L2Resp,self.B6_L2Resp,self.B7_L2Resp,self.B8_L2Resp]
        self.InfList = [self.B1_Inf,self.B2_Inf,self.B3_Inf,self.B4_Inf, \
                        self.B5_Inf,self.B6_Inf,self.B7_Inf,self.B8_Inf]

        self.sessionTimeStrList = [self.B1_SessionTimeStr, self.B2_SessionTimeStr,self.B3_SessionTimeStr, self.B4_SessionTimeStr, \
                                   self.B5_SessionTimeStr, self.B6_SessionTimeStr,self.B7_SessionTimeStr, self.B8_SessionTimeStr]
        
        # ********************* Initialization Parameters ****************************

        INI_Frame = ttk.Frame(self.iniTab, borderwidth = 3, relief="sunken")
        INI_Frame.grid(column = 0, row = 0, sticky=(W, E))
        
        """
        The GUIClass has lists of ttk variables (IntVar or textvariable) which 
        map onto variables in each Box object.
        ID, weight, sched (1..4), pumptime, calcPumpTime (boolean), sessionlength

        """
        B1_ROW_ =  ttk.Label(INI_Frame, text="BOX 1").grid(column=0, row=0, sticky=(W, E))
        B1_ID_Entry = ttk.Entry(INI_Frame, width=6,textvariable=self.B1_IDStr).grid(column = 1, row = 0) 
        B1_Weight_Entry = ttk.Entry(INI_Frame, width=6,textvariable=self.B1_Weight).grid(column = 2, row = 0)
        B1_Param = Spinbox(INI_Frame, textvariable = self.B1_Param_value, width = 3, from_=1, to=1000).grid(column=3, row=0)
        B1_SchedComboBox = ttk.Combobox(INI_Frame, textvariable=self.B1_sched, width = 15, \
                values = self.sched).grid(column=4, row=0)
        B1_SessionLength = Spinbox(INI_Frame, textvariable = self.B1_SessionLength, width = 3, \
                values = [2, 5, 30, 60, 90, 120, 180, 240, 300, 360]).grid(column=5, row=0)
        B1_IBILength = Spinbox(INI_Frame, textvariable = self.B1_IBILength, width = 3, \
                values = [0, 5, 10, 15, 20, 25, 30]).grid(column=6, row=0)
        B1_PumpTime = Spinbox(INI_Frame, textvariable = str(self.B1_PumpTime), width = 3, from_=300, to=600).grid(column=7,row=0)
        B1_CalcPumpTime = Checkbutton(INI_Frame, text = "Calc  ", variable = self.B1_calcPumpTime, \
                onvalue = True, offvalue = False, command=lambda boxIndex = 0: \
                self.calcPumpTime(self.B1_calcPumpTime.get(),boxIndex)).grid(column=8, row=0)


        B2_ROW_ =  ttk.Label(INI_Frame, text="BOX 2").grid(column=0, row=1, sticky=(W, E))
        B2_ID_Entry = ttk.Entry(INI_Frame, width=6,textvariable=self.B2_IDStr).grid(column = 1, row=1) 
        B2_Weight_Entry = ttk.Entry(INI_Frame, width=6,textvariable=self.B2_Weight).grid(column = 2, row=1)
        B2_Param = Spinbox(INI_Frame, textvariable = self.B2_Param_value, width = 3, from_=1, to=1000).grid(column=3, row=1)
        B2_SchedComboBox = ttk.Combobox(INI_Frame, textvariable=self.B2_sched, width = 15, \
                values = self.sched).grid(column=4, row=1)
        B2_SessionLength = Spinbox(INI_Frame, textvariable = self.B2_SessionLength, width = 3, \
                values = [2, 5, 30, 60, 90, 120, 180, 240, 300, 360]).grid(column=5, row=1)
        B2_IBILength = Spinbox(INI_Frame, textvariable = self.B2_IBILength, width = 3, \
                values = [0, 5, 10, 15, 20, 25, 30]).grid(column=6, row=1)
        B2_PumpTime = Spinbox(INI_Frame, textvariable = str(self.B2_PumpTime), width = 3, from_=300, to=600).grid(column=7,row=1)
        B2_CalcPumpTime = Checkbutton(INI_Frame, text = "Calc  ", variable = self.B2_calcPumpTime, \
                onvalue = True, offvalue = False, command=lambda boxIndex = 1: \
                self.calcPumpTime(self.B2_calcPumpTime.get(),boxIndex)).grid(column=8, row=1)


        B3_ROW_ =  ttk.Label(INI_Frame, text="BOX 3").grid(column=0, row=2, sticky=(W, E))
        B3_ID_Entry = ttk.Entry(INI_Frame, width=6,textvariable=self.B3_IDStr).grid(column = 1, row=2) 
        B3_Weight_Entry = ttk.Entry(INI_Frame, width=6,textvariable=self.B3_Weight).grid(column = 2, row=2)
        B3_Param = Spinbox(INI_Frame, textvariable = self.B3_Param_value, width = 3, from_=1, to=1000).grid(column=3, row=2)
        B3_SchedComboBox = ttk.Combobox(INI_Frame, textvariable=self.B3_sched, width = 15, \
                values = self.sched).grid(column=4, row=2)
        B3_SessionLength = Spinbox(INI_Frame, textvariable = self.B3_SessionLength, width = 3, \
                values = [30, 60, 90, 120, 180, 240, 300, 360]).grid(column=5, row=2)
        B3_IBILength = Spinbox(INI_Frame, textvariable = self.B3_IBILength, width = 3, \
                values = [0, 5, 10, 15, 20, 25, 30]).grid(column=6, row=2)
        B3_PumpTime = Spinbox(INI_Frame, textvariable = str(self.B3_PumpTime), width = 3, from_=300, to=600).grid(column=7,row=2)
        B3_CalcPumpTime = Checkbutton(INI_Frame, text = "Calc  ", variable = self.B3_calcPumpTime, \
                onvalue = True, offvalue = False, command=lambda boxIndex = 2: \
                self.calcPumpTime(self.B3_calcPumpTime.get(),boxIndex)).grid(column=8, row=2)

        B4_ROW_ =  ttk.Label(INI_Frame, text="BOX 4").grid(column=0, row=3, sticky=(W, E))
        B4_ID_Entry = ttk.Entry(INI_Frame, width=6,textvariable=self.B4_IDStr).grid(column = 1, row=3) 
        B4_Weight_Entry = ttk.Entry(INI_Frame, width=6,textvariable=self.B4_Weight).grid(column = 2, row=3)
        B4_Param = Spinbox(INI_Frame, textvariable = self.B4_Param_value, width = 3, from_=1, to=1000).grid(column=3, row=3)
        B4_SchedComboBox = ttk.Combobox(INI_Frame, textvariable=self.B4_sched, width = 15,
                values = self.sched).grid(column=4, row=3)
        B4_SessionLength = Spinbox(INI_Frame, textvariable = self.B4_SessionLength, width = 3, \
                values = [30, 60, 90, 120, 180, 240, 300, 360]).grid(column=5, row=3)
        B4_IBILength = Spinbox(INI_Frame, textvariable = self.B4_IBILength, width = 3, \
                values = [0, 5, 10, 15, 20, 25, 30]).grid(column=6, row=3)
        B4_PumpTime = Spinbox(INI_Frame, textvariable = str(self.B4_PumpTime), width = 3, from_=300, to=600).grid(column=7,row=3)
        B4_CalcPumpTime = Checkbutton(INI_Frame, text = "Calc  ", variable = self.B4_calcPumpTime, \
                onvalue = True, offvalue = False, command=lambda boxIndex = 3: \
                self.calcPumpTime(self.B4_calcPumpTime.get(),boxIndex)).grid(column=8, row=3)

        B5_ROW_ =  ttk.Label(INI_Frame, text="BOX 5").grid(column=0, row=4, sticky=(W, E))
        B5_ID_Entry = ttk.Entry(INI_Frame, width=6,textvariable=self.B5_IDStr).grid(column = 1, row = 4) 
        B5_Weight_Entry = ttk.Entry(INI_Frame, width=6,textvariable=self.B5_Weight).grid(column = 2, row = 4)
        B5_Param = Spinbox(INI_Frame, textvariable = self.B5_Param_value, width = 3, from_=1, to=1000).grid(column=3, row=4)
        B5_SchedComboBox = ttk.Combobox(INI_Frame, textvariable=self.B5_sched, width = 15, \
                values = self.sched).grid(column=4, row=4)
        B5_SessionLength = Spinbox(INI_Frame, textvariable = self.B5_SessionLength, width = 3, \
                values = [30, 60, 90, 120, 180, 240, 300, 360]).grid(column=5, row=4)
        B5_IBILength = Spinbox(INI_Frame, textvariable = self.B5_IBILength, width = 3, \
                values = [0, 5, 10, 15, 20, 25, 30]).grid(column=6, row=4)
        B5_PumpTime = Spinbox(INI_Frame, textvariable = str(self.B5_PumpTime), width = 3, from_=300, to=600).grid(column=7,row=4)
        B5_CalcPumpTime = Checkbutton(INI_Frame, text = "Calc  ", variable = self.B5_calcPumpTime, \
                onvalue = True, offvalue = False, command=lambda boxIndex = 4: \
                self.calcPumpTime(self.B5_calcPumpTime.get(),boxIndex)).grid(column=8, row=4)
        
        B6_ROW_ =  ttk.Label(INI_Frame, text="BOX 6").grid(column=0, row=5, sticky=(W, E))
        B6_ID_Entry = ttk.Entry(INI_Frame, width=6,textvariable=self.B6_IDStr).grid(column = 1, row=5) 
        B6_Weight_Entry = ttk.Entry(INI_Frame, width=6,textvariable=self.B6_Weight).grid(column = 2, row=5)
        B6_Param = Spinbox(INI_Frame, textvariable = self.B6_Param_value, width = 3, from_=1, to=1000).grid(column=3, row=5)
        B6_SchedComboBox = ttk.Combobox(INI_Frame, textvariable=self.B6_sched, width = 15, \
                values = self.sched).grid(column=4, row=5)
        B6_SessionLength = Spinbox(INI_Frame, textvariable = self.B6_SessionLength, width = 3, \
                values = [30, 60, 90, 120, 180, 240, 300, 360]).grid(column=5, row=5)
        B6_IBILength = Spinbox(INI_Frame, textvariable = self.B6_IBILength, width = 3, \
                values = [0, 5, 10, 15, 20, 25, 30]).grid(column=6, row=5)
        B6_PumpTime = Spinbox(INI_Frame, textvariable = str(self.B6_PumpTime), width = 3, from_=300, to=600).grid(column=7,row=5)
        B6_CalcPumpTime = Checkbutton(INI_Frame, text = "Calc  ", variable = self.B6_calcPumpTime, \
                onvalue = True, offvalue = False, command=lambda boxIndex = 5: \
                self.calcPumpTime(self.B6_calcPumpTime.get(),boxIndex)).grid(column=8, row=5)

        B7_ROW_ =  ttk.Label(INI_Frame, text="BOX 7").grid(column=0, row=6, sticky=(W, E))
        B7_ID_Entry = ttk.Entry(INI_Frame, width=6,textvariable=self.B7_IDStr).grid(column = 1, row=6) 
        B7_Weight_Entry = ttk.Entry(INI_Frame, width=6,textvariable=self.B7_Weight).grid(column = 2, row=6)
        B7_Param = Spinbox(INI_Frame, textvariable = self.B7_Param_value, width = 3, from_=1, to=1000).grid(column=3, row=6)
        B7_SchedComboBox = ttk.Combobox(INI_Frame, textvariable=self.B7_sched, width = 15, \
                values = self.sched).grid(column=4, row=6)
        B7_SessionLength = Spinbox(INI_Frame, textvariable = self.B7_SessionLength, width = 3, \
                values = [30, 60, 90, 120, 180, 240, 300, 360]).grid(column=5, row=6)
        B7_IBILength = Spinbox(INI_Frame, textvariable = self.B7_IBILength, width = 3, \
                values = [0, 5, 10, 15, 20, 25, 30]).grid(column=6, row=6)
        B7_PumpTime = Spinbox(INI_Frame, textvariable = str(self.B7_PumpTime), width = 3, from_=300, to=600).grid(column=7,row=6)
        B7_CalcPumpTime = Checkbutton(INI_Frame, text = "Calc  ", variable = self.B7_calcPumpTime, \
                onvalue = True, offvalue = False, command=lambda boxIndex = 6: \
                self.calcPumpTime(self.B7_calcPumpTime.get(),boxIndex)).grid(column=8, row=6)

        B8_ROW_ =  ttk.Label(INI_Frame, text="BOX 8").grid(column=0, row=7, sticky=(W, E))
        B8_ID_Entry = ttk.Entry(INI_Frame, width=6,textvariable=self.B8_IDStr).grid(column = 1, row=7) 
        B8_Weight_Entry = ttk.Entry(INI_Frame, width=6,textvariable=self.B8_Weight).grid(column = 2, row=7)
        B8_Param = Spinbox(INI_Frame, textvariable = self.B8_Param_value, width = 3, from_=1, to=1000).grid(column=3, row=7)
        B8_SchedComboBox = ttk.Combobox(INI_Frame, textvariable=self.B8_sched, width = 15, \
                values = self.sched).grid(column=4, row=7)
        B8_SessionLength = Spinbox(INI_Frame, textvariable = self.B8_SessionLength, width = 3, \
                values = [30, 60, 90, 120, 180, 240, 300, 360]).grid(column=5, row=7)
        B8_IBILength = Spinbox(INI_Frame, textvariable = self.B8_IBILength, width = 3, \
                values = [0, 5, 10, 15, 20, 25, 30]).grid(column=6, row=7)
        B8_PumpTime = Spinbox(INI_Frame, textvariable = str(self.B8_PumpTime), width = 3, from_=300, to=600).grid(column=7,row=7)
        B8_CalcPumpTime = Checkbutton(INI_Frame, text = "Calc  ", variable = self.B8_calcPumpTime, \
                onvalue = True, offvalue = False, command=lambda boxIndex = 7: \
                self.calcPumpTime(self.B8_calcPumpTime.get(),boxIndex)).grid(column=8, row=7)
        """
            1     2      3     4      5      6    
            RatID Weight Ratio Sched Session Pump")
                  (gms)              (min)   (10 mSec)
        """
        aLabel =  ttk.Label(INI_Frame, text="RatID ").grid(column=1, row=12)
        aLabel =  ttk.Label(INI_Frame, text="Weight").grid(column=2, row=12)
        aLabel =  ttk.Label(INI_Frame, text="N").grid(column=3, row=12)
        aLabel =  ttk.Label(INI_Frame, text="Protocol ").grid(column=4, row=12)
        aLabel =  ttk.Label(INI_Frame, text="Block ").grid(column=5, row=12)
        aLabel =  ttk.Label(INI_Frame, text="IBI*").grid(column=6, row=12)        
        aLabel =  ttk.Label(INI_Frame, text="Pump").grid(column=7, row=12)
        aLabel =  ttk.Label(INI_Frame, text="(gms)").grid(column=2, row=13)
        aLabel =  ttk.Label(INI_Frame, text="(Min)").grid(column=5, row=13)
        aLabel =  ttk.Label(INI_Frame, text="(Min)").grid(column=6, row=13)
        aLabel =  ttk.Label(INI_Frame, text="(10 mSec)").grid(column=7, row=13)

        #['0: Do not run', '1: FR(N)', '2: FR1 x 20 trials', '3: FR1 x N trials', '4: PR(step N)', '5: TH', '6: IntA: 5-25', '7: Flush', '8: L2-HD', '9: IntA-HD', '10: 2L-PR-HD']


        aLabel = ttk.Label(INI_Frame, text="0: Do Not Run - enough said").grid(column=1, sticky = W, columnspan=7, row=14)
        aLabel = ttk.Label(INI_Frame, text="1: FR(N) - Session length = block length (min)").grid(column=1, sticky = W, columnspan=7, row=15)
        aLabel = ttk.Label(INI_Frame, text="2: FR1 x 20 - Session length = block length (min). Stops after 20 infusions").grid(column=1, sticky = W, columnspan=7, row=16)
        aLabel = ttk.Label(INI_Frame, text="3: FR1 x N trials - Session length = block length (min). Stops after N infusions").grid(column=1, sticky = W, columnspan=7, row=17)
        aLabel = ttk.Label(INI_Frame, text="4: PR starting at step N (usually 1); Session length = block length (min)").grid(column=1, sticky = W, columnspan=7, row=18)
        aLabel = ttk.Label(INI_Frame, text="5: TH - 13 Trials - uses Block length (typically 10 min) and IBI (Typically 0 min)").grid(column=1, sticky = W, columnspan=7, row=19)
        aLabel = ttk.Label(INI_Frame, text="6: IntA: 5 - 25. Defaults to 5 min trials and 25 min. ").grid(column=1, sticky = W, columnspan=7, row=20)
        aLabel = ttk.Label(INI_Frame, text="7: Flush: N Infusions separated by Block time").grid(column=1, sticky = W, columnspan=7, row=21)
        aLabel = ttk.Label(INI_Frame, text="8: L2-HD - HD on Lever Two. Session length = block length (min)").grid(column=1, sticky = W, columnspan=7, row=22)
        aLabel = ttk.Label(INI_Frame, text="9: IntA-HD. Block(min) and IBI(min); Session length = block length (min)").grid(column=1, sticky = W, columnspan=7, row=23)
        aLabel = ttk.Label(INI_Frame, text="10: 2L-PR-HD. HD access determined by N (sec)").grid(column=1, sticky = W, columnspan=7, row=24)
        aLabel = ttk.Label(INI_Frame, text="* IBI - applies to TH and IntA-HD").grid(column=1, sticky = W, columnspan=7, row=25)

        self.loadFromINIFile()
        self.readExampleFiles()
        

        #********************* END of GUI_Class __INIT__(self) ********************

    def sendSysVars(self):
        self.updateVarCode()
        self.outputText("<SYSVARS "+str(self.varCode)+">")

    def calcPumpTime(self,checked,boxIndex):
        """
        4 sec * 5 mg/ml * 0.025 ml/sec / 0.333kg = 1.5 mg/kg
        weight(g) * 12.012 = mSec pump time for 1.5 mg/kg
        Pump time is set in 10mSec intervals so weight(g) * 1.2012 yields proper pumptime setting
        """
        if (checked == 0):
            self.PumpTimeList[boxIndex].set(400)
        else:
            t = int(self.WeightList[boxIndex].get() * 1.2012)
            self.PumpTimeList[boxIndex].set(t)
            # print(boxIndex, "weight = ", self.WeightList[boxIndex].get()," pumptime =", t)           

    def loadFromINIFile(self):
        """
        Reads 8 lines from SA300.ini, parses the line (depending on the position of spaces)
        into "" which are assigned to Parameters in each Box.
        Lists as used to iterate over each variable.
        """       
        if (self.verbose):
            print("Reading SA300.ini")
        iniFile = open('SA300.ini','r')
        for i in range(8):
            aLine = iniFile.readline().rstrip("\n")   # read line 
            tokens = aLine.split()
            if (self.verbose):
                print(tokens)
            self.IDStrList[i].set(tokens[0])
            self.WeightList[i].set(tokens[1])
            self.schedList[i].set(self.sched[int(tokens[2])])
            self.paramNumList[i].set(tokens[3])
            self.SessionLengthList[i].set(tokens[4])
            self.IBILengthList[i].set(tokens[5])
            self.PumpTimeList[i].set(tokens[6])
            self.calcPumpTimeList[i].set(tokens[7])
        aString = iniFile.readline().rstrip("\n")      # COM number (done differently on a Mac)
        self.portString.set(aString)
        # print("portString = "+aString)
        aString = iniFile.readline().rstrip("\n")   # read next line
        tokens = aString.split()
        self.varCode = int(tokens[0])
        # print("self.varCode =",self.varCode,format(self.varCode,'08b'))       
        for bit in range(8):
            mask = (2**bit)     # mask (eg. 00001000)
            # Uses AND and mask to determine whether to set bit
            if (self.varCode & mask > 0): self.sysVarList[bit].set(True)
            else: self.sysVarList[bit].set(False)
        iniFile.close()

    def updateVarCode(self):
        self.varCode = 0
        for bit in range(8):
            # print(self.sysVarList[bit].get())
            if (self.sysVarList[bit].get() == False):               
                # Set bit to 0 if False
                # uses AND and a mask (eg. 11110111)
                self.varCode = self.varCode & (255 - (2**bit))           
            else:
                # Set bit to 1 if True
                # uses OR and a number (eg. 1,2,4,8 etc)
                self.varCode = self.varCode | (2**bit)
        # print("self.varCode =",self.varCode,format(self.varCode,'08b'))

    def writeToINIFile(self):
        INIfileName = "SA300.ini"
        if (self.verbose):
            print("Writing", INIfileName)
        iniFile = open(INIfileName,'w')        
        for i in range(8):
            schedIndex = self.sched.index(self.schedList[i].get())
            IDStr = self.IDStrList[i].get()
            if (len(IDStr) == 0): IDStr = 'box'+str(i+1)
            tempStr = IDStr+' '+ \
            str(self.WeightList[i].get())+' '+ \
            str(schedIndex)+' '+ \
            str(self.paramNumList[i].get())+' '+ \
            str(self.SessionLengthList[i].get())+' '+ \
            str(self.IBILengthList[i].get())+' '+ \
            str(self.PumpTimeList[i].get())
            if (self.calcPumpTimeList[i].get() == True):
                tempStr = tempStr+' 1'
            else:
                tempStr = tempStr+' 0'
            if (self.verbose):
                print(tempStr)
            iniFile.write(tempStr+'\n')
        iniFile.write(self.portString.get()+'\n')
        self.updateVarCode()
        iniFile.write(str(self.varCode)+'\n')       
        iniFile.close()
        
    def readExampleFiles(self):
        self.example1List = []
        aFile = open('PR_Example_File.dat','r')
        for line in  aFile:
            pair = line.split()
            pair[0] = int(pair[0])
            self.example1List.append(pair)
        aFile.close()
        self.example2List = []
        aFile = open('ErrorData.py','r')
        for line in  aFile:
            pair = line.split()
            pair[0] = int(pair[0])
            self.example2List.append(pair)
        aFile.close()
    
    def saveFile(self,subject_ID,dataList):        
        today = date.today()
        ID_Date = subject_ID+"_"+today.strftime("%b_%d")
        extension = ".dat"
        fileName = ID_Date+extension
        while os.path.isfile(fileName) == True:
            ID_Date = ID_Date+"a"
            fileName = ID_Date+extension
        print("   Saving file to", fileName)
        fileToSave = open(fileName,'w')
        for pairs in dataList:
            line = str(pairs[0])+" "+pairs[1]+"\n"
            fileToSave.write(line)
        fileToSave.close()

    def saveAllData(self):
        print("Trying to save data")

        for i in range(8):
            tempStr = "Box "+str(i+1)
            if (self.boxes[i].sessionStarted == True):               
                if (self.boxes[i].sessionCompleted == False):
                    tempStr = tempStr+" still running"
                    print(tempStr)
                else:
                    tempStr = tempStr+" session completed - "
                    if (self.boxes[i].dataSaved == True):
                        tempStr = tempStr+" data previously saved"
                        print(tempStr)
                    else:
                        print(tempStr)
                        self.saveFile(self.boxes[i].subject_ID_string,self.boxes[i].dataList)
                        self.boxes[i].dataSaved = True
            else:
                print(tempStr+" no data to save")

        """
        if len(self.box1.dataList) > 0:
            self.saveFile(self.box1.subject_ID_string,self.box1.dataList)
        if len(self.box2.dataList) > 0:
            self.saveFile(self.box2.subject_ID_string,self.box2.dataList)
        if len(self.box3.dataList) > 0:
            self.saveFile(self.box3.subject_ID_string,self.box3.dataList)
        if len(self.box4.dataList) > 0:
            self.saveFile(self.box4.subject_ID_string,self.box4.dataList)
        if len(self.box5.dataList) > 0:
            self.saveFile(self.box5.subject_ID_string,self.box5.dataList)
        if len(self.box6.dataList) > 0:
            self.saveFile(self.box6.subject_ID_string,self.box6.dataList)
        if len(self.box7.dataList) > 0:
            self.saveFile(self.box7.subject_ID_string,self.box7.dataList)
        if len(self.box8.dataList) > 0:
            self.saveFile(self.box8.subject_ID_string,self.box8.dataList)
        """

    def dumpData(self):
        for pairs in self.boxes[self.selectedBox.get()].dataList:
            line = str(pairs[0])+" "+pairs[1]
            print(line)

    """

    def errorRecord(self,aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, dataList, charList, aLabel):
        x = x_zero
        y = y_zero
        x_scaler = x_pixel_width / (max_x_scale*60*1000)
        aCanvas.create_text(x_zero-50, y_zero-5, fill="blue", text = aLabel)
        aCanvas.create_text(x_zero-20, y_zero-5, fill="blue", text = "error")
        aCanvas.create_text(x_zero-20, y_zero+5, fill="blue", text = "recover")
        
        for pairs in dataList:
            if pairs[1] in charList:
                newX = (x_zero + pairs[0] * x_scaler // 1)
                aCanvas.create_line(x, y, newX, y)                              # draw line to newX
                if (len(charList) == 1):                                        # one char in List = ["P"]
                    aCanvas.create_line(newX, y, newX, y-10)                    # draw a line upward
                else:                                                           # two chars in list = ["B","b"]
                    if pairs[1] == charList[0]:                                 # if first char
                        newY = y_zero - 10
                        aCanvas.create_line(newX, y_zero, newX, newY, fill="red")   # move y upwards
                    else:                                                       # if second char in list
                        newY = y_zero + 10                                      # move y downwards      
                        aCanvas.create_line(newX, y_zero, newX, newY, fill="green")           # draw line from y-zero up or down
                    # y = newY                                                  # no need to remember
                x = newX
        for pairs in dataList:
            if pairs[1] == '*':
                newX = (x_zero + pairs[0] * x_scaler // 1)
                aCanvas.create_text(newX, y_zero+10, fill="blue",text= '*')  # show char underneath


    def drawSessionLogTimeStamps(self):
        # This procedure drawa some of the data from self.sessionLog to the screen.
        # It does not clear the screen so it can be overlaid onto data from Timestamps or events. 
        
        # In order to debug the program and test ways of graphing the data, the following
        # procedure creates a faux (local) sessionLog when no session is running. 
        # If a session is running (and self.sessionLog contains data) those data will be plotted.
        
        if (len(self.sessionLog) < 2):
            sessionLog = []
            sessionLog.append("0 SA300 started Feb/03/2021/14:43:19")
            sessionLog.append("300000 A Millis() on Connect1")    # On connect - 5 min after Feather reset
            sessionLog.append("300000 & chipsReset() 0")
            sessionLog.append("900000 M Session started - Box: 1")
            sessionLog.append("900050 M Session started - Box: 2")
            sessionLog.append("960000 @ Input error on port 1")   # # 1 min into Box 1 session          (16 min)
            sessionLog.append("964000 # Recovered from input error on port 1")      # 1 min plus 4 sec
            sessionLog.append("1020000 @ Input error on port 1")                    # 2 min into Box 1 session (17 min)
            sessionLog.append("1050000 @ Input error on port 1") 
            sessionLog.append("1080000 @ Input error on port 1") 
            sessionLog.append("1110000 @ Input error on port 1") 
            sessionLog.append("1140000 @ Input error on port 1") 
            sessionLog.append("1150000 # Recovered from input error on port 1")     # 2 min 4 sec        
            sessionLog.append("1500000 $ Output error on port 4")                   # 10 min into Box 1 session                             (25 min)
            sessionLog.append("1500050 ! Session Aborted!")                         # 10 min + 50 mSec
            sessionLog.append("1500100 m Session ended - Box: 1")
            sessionLog.append("1500150 m Session ended - Box: 2")
            sessionLog.append("1500200 ( enterSafeMode()")                          # 11 min 4 sec
        else:
            sessionLog = self.sessionLog


        # *********  Create a list containing only the timeStamp and strCode  ********
        timeStamp = 0
        strCode = "XX"
        logList = []
        for i in range (1, len(sessionLog)-1):
            line = sessionLog[i]
            tokens = line.split( )
            timeStamp = int(tokens[0])
            strCode = tokens[1]
            logList.append([timeStamp, strCode])

        # ********* Examine list and pull relevant info ***********
        
        # Error codes are time stamped with millis() on Feather. Since the Feather might not have
        # been reset for days, time zero might be a long time ago. There's a need to adjust the timestamp
        # to reflect a more appropriate starting point.  Two possible time zeros are:
        # connectTime - this is when the FeatherM0 acknowledges a USB connection with an 'A'
        # boxStartTime - thsi is when the first box indicates it has started with an 'M'
        

        connectTime = 0                         
        boxStartTime  = 0
        boxStartTimeFound = False;

        for pairs in logList:               # Search through the list
            if (pairs[1] == "A"):
                connectTime = pairs[0]
            elif (pairs[1] == "M"):
                if (boxStartTimeFound == False):
                    boxStartTime = pairs[0]
                    boxStartTimeFound = True

        print("connectTime = ",connectTime)
        print("boxStartTime = ", boxStartTime)
    
        Tzero = connectTime
        connectStr = "Tzero is time serial connection made"
        if (boxStartTime > connectTime):
            Tzero = boxStartTime
            connectStr = "Tzero is First Box Start Time"

        # ******** Subtract Tzero from all timestamps in logList
        # This should bring the times in line with the Box data coming from Feather
          
        for i in range (0, len(logList)):
            logList[i][0] = logList[i][0] - Tzero

        # ******** Adjust time zero to bring it in line with Graph Tab "TimeStamps" and "Events"
        
        max_x_scale = self.selectMax_x_Scale.get()
        if max_x_scale == 360: x_divisions = 12
        elif max_x_scale == 180: x_divisions = 6
        elif max_x_scale == 60: x_divisions = 6
        elif max_x_scale == 30: x_divisions = 6
        elif max_x_scale == 10: x_divisions = 10
        x_zero = 75
        y_zero = 375  # self.Y_ZERO = 275 
        x_pixel_width = 500
        
        aCanvas = self.topCanvas
        GraphLib.drawXaxis(aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, x_divisions)
        aCanvas.create_text(x_zero+50, y_zero-40, fill="blue", text = connectStr)
       
        GraphLib.eventRecord(aCanvas, x_zero, y_zero-80, x_pixel_width, max_x_scale, logList, ["@"], "Input Error")
        GraphLib.eventRecord(aCanvas, x_zero, y_zero-60, x_pixel_width, max_x_scale, logList, ["$"], "Output Error")

        # **** Check if session was aborted and, if so, draw a big red line
        # **** Search logList for the abort char '!'
        
        x_abort = 0        # define for use in plotting abort time
        for pairs in logList:
            if (pairs[1] == "!"):
                print("Aborted at: ",pairs[0])
                x_scaler = x_pixel_width / (max_x_scale*60*1000)
                x_abort = (x_zero + pairs[0] * x_scaler // 1)           
                aCanvas.create_line(x_abort, y_zero-55, x_abort, y_zero-85, width=3, fill="red")
                aCanvas.create_text(x_abort+60, y_zero-70, fill="red", text = "Session Aborted")



        # self.errorRecord(aCanvas, x_zero, y_zero-95,  x_pixel_width, max_x_scale, logList, ["@","#"], "In")
        # self.errorRecord(aCanvas, x_zero, y_zero-65,  x_pixel_width, max_x_scale, logList, ["$","%"], "Out")
        # self.errorRecord(aCanvas, x_zero, y_zero-55,  x_pixel_width, max_x_scale, logList, ["&"], "ChipReset")

        # ****** End of Feb 3 Stuff ****************************
                          
        """

    def drawAllTimeStamps(self,aCanvas,selectedList, max_x_scale):

        if (selectedList < 8): dataList = self.boxes[self.selectedBox.get()].dataList
        elif (selectedList == 8): dataList = self.example1List
        elif (selectedList == 9): dataList = self.example2List
        

        aCanvas.delete('all')
        # max_x_scale = self.topMax_x_Scale.get()
        if max_x_scale == 360: x_divisions = 12
        elif max_x_scale == 180: x_divisions = 6
        elif max_x_scale == 60: x_divisions = 6
        elif max_x_scale == 30: x_divisions = 6
        elif max_x_scale == 10: x_divisions = 10
        x_zero = 75
        y_zero = 375  # self.Y_ZERO = 275 
        x_pixel_width = 500

        startTime = 0;
        if len(dataList) > 0:
            firstEntry=(dataList[0])
            if (firstEntry[1] == 'M'):
                startTime = firstEntry[0]
                print("StartTime =",startTime)

        topRow = 40
        spacing = 15
        GraphLib.drawXaxis(aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, x_divisions)
        
        #GraphLib.eventRecord(aCanvas, x_zero, topRow, x_pixel_width, max_x_scale, dataList, ["~",","], "Lever 2")
        
        GraphLib.eventRecord(aCanvas, x_zero, topRow, x_pixel_width, max_x_scale, dataList, ["T","t"], "L1 Trial")
        GraphLib.eventRecord(aCanvas, x_zero, topRow+(spacing), x_pixel_width, max_x_scale, dataList, ["=","."], "Lever 1")        
        GraphLib.eventRecord(aCanvas, x_zero, topRow+(spacing*2), x_pixel_width, max_x_scale, dataList, ["L"], "L1 Resp")
        GraphLib.eventRecord(aCanvas, x_zero, topRow+(spacing*3), x_pixel_width, max_x_scale, dataList, ["P","p"], "Pump")
        GraphLib.eventRecord(aCanvas, x_zero, topRow+(spacing*4), x_pixel_width, max_x_scale, dataList, ["S","s"], "Stim")
        GraphLib.eventRecord(aCanvas, x_zero, topRow+(spacing*5), x_pixel_width, max_x_scale, dataList, ["O","o"], "TimeOut")        
        GraphLib.eventRecord(aCanvas, x_zero, topRow+(spacing*6), x_pixel_width, max_x_scale, dataList, ["Z","z"], "HD Trial") 
        GraphLib.eventRecord(aCanvas, x_zero, topRow+(spacing*7), x_pixel_width, max_x_scale, dataList, ["~",","], "Lever 2")
        GraphLib.eventRecord(aCanvas, x_zero, topRow+(spacing*8), x_pixel_width, max_x_scale, dataList, ["H","h"], "HD Resp")     
        GraphLib.eventRecord(aCanvas, x_zero, topRow+(spacing*9), x_pixel_width, max_x_scale, dataList, ["B","b"], "Block")
        GraphLib.eventRecord(aCanvas, x_zero, topRow+(spacing*10), x_pixel_width, max_x_scale, dataList, ["I","i"], "IBI")
        GraphLib.eventRecord(aCanvas, x_zero, topRow+(spacing*11), x_pixel_width, max_x_scale, dataList, ["G","E"], "Session")
        aCanvas.create_text(15, topRow+(spacing*12)+4, fill="red", text="Errors", anchor = W)
        GraphLib.eventRecord(aCanvas, x_zero, topRow+(spacing*14),  x_pixel_width, max_x_scale, dataList, ["@"], "@ Input", t_zero = startTime)       
        GraphLib.eventRecord(aCanvas, x_zero, topRow+(spacing*15),  x_pixel_width, max_x_scale, dataList, ["#"], "# Recover", t_zero = startTime)
        GraphLib.eventRecord(aCanvas, x_zero, topRow+(spacing*16),  x_pixel_width, max_x_scale, dataList, ["$"], "$ Output", t_zero = startTime)
        GraphLib.eventRecord(aCanvas, x_zero, topRow+(spacing*17),  x_pixel_width, max_x_scale, dataList, ["%"], "% Recover", t_zero = startTime)
        GraphLib.eventRecord(aCanvas, x_zero, topRow+(spacing*18),  x_pixel_width, max_x_scale, dataList, ["&"], "& Reset", t_zero = startTime)
        GraphLib.eventRecord(aCanvas, x_zero, topRow+(spacing*19),  x_pixel_width, max_x_scale, dataList, ["!"], "! Abort",t_zero = startTime)
        GraphLib.eventRecord(aCanvas, x_zero, topRow+(spacing*20),  x_pixel_width, max_x_scale, dataList, ["("], "( Safe",t_zero = startTime)


        """
        codeDict = {'A':' Millis() on Connect ', \
                    '@':' Input error on port ', \
                    '#':' Recovered from input error on port ', \
                    '$':' Output error on port ', \
                    '%':' Recovered from output error ', \
                    '&':' chipsReset() ', \
                    '!':' Session Aborted! ', \
                    'r':' Recovery after resetChips() ', \
                    'M':' Session started - Box: ', \
                    'm':' Session ended - Box: ', \
                    '(':' enterSafeMode() '
                    }

        """

     

    def sendCode(self, codeStr):
        self.outputText(codeStr)
    
    def reportParameters(self):
        self.outputText("<R 0>")    # Report parameters
        self.outputText("<R 1>")
        self.outputText("<R 2>")
        self.outputText("<R 3>")
        self.outputText("<R 4>")
        self.outputText("<R 5>")
        self.outputText("<R 6>")
        self.outputText("<R 7>")

    def resetChips(self):
        self.outputText("<r>")       # Reset Chips

    def abort(self):
        self.outputText("<Abort>")       # Abort!

    def diagnostics(self):
        self.outputText("<D>")       # Get Diagnostics

    def checkOutputPorts(self):
        self.outputText("<O>")       # checkOutputPort()

    def printSessionLog(self):  
        print("****** SessionLog *******")
        for line in self.sessionLog:
            print(line)
        print("****** End SessionLog ***")

    def testFunction1(self):         # temp use
        # self.display_abort_msg()
        self.outputText("<A>")

    def toggleCheckLevers(self,checkLeversState):
        if (checkLeversState): self.outputText("<CL>")
        else: self.outputText("<cl>")

    def toggleDebugVar(self,index,level):
        if (level): self.outputText("<Debug 0 1>")
        else: self.outputText("<Debug 0 0>")

    def drawCumulativeRecord(self, aCanvas, selectedList, max_x_scale):
        aCanvas.delete('all')
        x_zero = self.X_ZERO
        y_zero = self.Y_ZERO
        x_pixel_width = 500                               
        y_pixel_height = 230
        # max_x_scale = 120
        x_divisions = 12
        if (max_x_scale == 10) or (max_x_scale == 30): x_divisions = 10
        max_y_scale = 100
        y_divisions = 10
        if (selectedList < 8):
            dataList = self.boxes[self.selectedBox.get()].dataList
            aTitle = self.boxes[self.selectedBox.get()].subject_ID_string
        elif (selectedList == 8):
            dataList = self.example1List
            aTitle = "PR example"
        elif (selectedList == 9):
            dataList = self.example2List
            aTitle = "IntA example"
        GraphLib.drawXaxis(aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, x_divisions)
        GraphLib.drawYaxis(aCanvas, x_zero, y_zero, y_pixel_height, max_y_scale, y_divisions, True)
        GraphLib.cumRecord(aCanvas, x_zero, y_zero, x_pixel_width, y_pixel_height, max_x_scale, max_y_scale, dataList, True, aTitle)
        
    def drawEventRecords(self):

        max_x_scale = self.selectMax_x_Scale.get()
        if max_x_scale == 360: x_divisions = 12
        elif max_x_scale == 180: x_divisions = 6
        elif max_x_scale == 60: x_divisions = 6
        elif max_x_scale == 30: x_divisions = 6
        elif max_x_scale == 10: x_divisions = 10
        x_zero = 75
        y_zero = 375  # self.Y_ZERO = 275 
        x_pixel_width = 500

        aCanvas = self.topCanvas
        GraphLib.drawXaxis(aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, x_divisions)

        aCanvas.delete('all')
        aCanvas.create_text(150, 10, fill="blue", text="topCanvas")
        GraphLib.drawXaxis(aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, x_divisions)
        #                eventRecord(aCanvas, x_zero, y_zero, x_pixel_width, max_x_scale, dataList, charList, aLabel):
        GraphLib.eventRecord(self.topCanvas, x_zero, y_zero-330, x_pixel_width, max_x_scale, self.box1.dataList, ["P"], "Box 1")
        GraphLib.eventRecord(self.topCanvas, x_zero, y_zero-310, x_pixel_width, max_x_scale, self.box2.dataList, ["P"], "Box 2")
        GraphLib.eventRecord(self.topCanvas, x_zero, y_zero-290, x_pixel_width, max_x_scale, self.box3.dataList, ["P"], "Box 3")
        GraphLib.eventRecord(self.topCanvas, x_zero, y_zero-270, x_pixel_width, max_x_scale, self.box4.dataList, ["P"], "Box 4")
        GraphLib.eventRecord(self.topCanvas, x_zero, y_zero-250, x_pixel_width, max_x_scale, self.box5.dataList, ["P"], "Box 5")
        GraphLib.eventRecord(self.topCanvas, x_zero, y_zero-230, x_pixel_width, max_x_scale, self.box6.dataList, ["P"], "Box 6")
        GraphLib.eventRecord(self.topCanvas, x_zero, y_zero-210, x_pixel_width, max_x_scale, self.box7.dataList, ["P"], "Box 7")
        GraphLib.eventRecord(self.topCanvas, x_zero, y_zero-190, x_pixel_width, max_x_scale, self.box8.dataList, ["P"], "Box 8")

    def clearCanvas(self, aCanvas):
        if (aCanvas == 0):
            self.topCanvas.delete('all')
        else:
            self.bottomCanvas.delete('all')

        GraphLib.drawXaxis
        

        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def moveLever1(self,boxIndex,state):
        if (state == True): tempStr = "<= "+str(boxIndex)+">"
        else: tempStr = "<. "+str(boxIndex)+">"
        self.outputText(tempStr)

    def moveLever2(self,boxIndex,state):
        if (state == True): tempStr = "<~ "+str(boxIndex)+">"
        else: tempStr = "<, "+str(boxIndex)+">"
        self.outputText(tempStr)

    def togglePump(self,boxIndex,state):
        if (state == True): tempStr = "<P "+str(boxIndex)+">"
        else: tempStr = "<p "+str(boxIndex)+">"
        self.outputText(tempStr)

    def toggleLED1(self,boxIndex,state):
        if (state == True): tempStr = "<S "+str(boxIndex)+">"
        else: tempStr = "<s "+str(boxIndex)+">"
        self.outputText(tempStr)

    def toggleLED2(self,boxIndex,state):
        if (state == True): tempStr = "<C "+str(boxIndex)+">"
        else: tempStr = "<c "+str(boxIndex)+">"
        self.outputText(tempStr)
            
    def connect(self):
        self.portList = []
        self.nt_portList = []
        self.portList = []
        if (os.name == "posix"):
            print("OS = posix (Mac)")
            self.OS_String.set("OS = posix (Mac)")
            self.portList = glob.glob('/dev/tty.usbmodem*')
            print("comports =", self.portList)
            if (len(self.portList) > 0):
                print("found ", self.portList[0])
                self.arduino0.connect(self.portList[0])
                tempStr = "Mac OS found "+str(len(self.portList))+" arduino"
                self.writeToTextbox(tempStr,0)                 
            else:
                self.writeToTextbox("No Feather found",0)
                
        elif(os.name == "nt"):
            self.OS_String.set("OS = Windows")
            print("Found Windows OS")
            ports = ['COM%s' % (i + 1) for i in range(256)]
            # The above generate a list ['COM1', 'COM2', 'COM3', 'COM4'...]
            # The it tests which has a connection
            portList = []
            for port in ports:
                try:
                    s = serial.Serial(port)
                    s.close()
                    self.nt_portList.append(port)
                except (OSError, serial.SerialException):
                    pass
            print("Possible COM ports:",self.nt_portList)
            print("COM port from INI file: ",self.portString.get())
            self.arduino0.connect(self.portString.get())
            
        if self.arduino0.activeConnection == True:
                self.connectLabelText.set("Connected")
                self.writeToTextbox("Connected!",0)
                time.sleep(2)
                # Request version number from sketch name and version Feather M0
                self.outputText("<A>")
                self.sendSysVars()
                timeNow = datetime.now()
                dateTimeStr = timeNow.strftime("%b/%d/%Y/%H:%M:%S")
                if len(self.sessionLog) > 0: self.sessionLog = []
                self.sessionLog.append([0,"FeatherM0 connected "+dateTimeStr])
        else:
            self.writeToTextbox("Unable to connect",0)
            self.connectLabelText.set("Unable to connect")
                     
    def startSession(self,boxIndex):
        if self.arduino0.activeConnection == True:
            listIndex = boxIndex
            # initialize the box
            self.boxes[listIndex].initialize(self.IDStrList[listIndex].get(),self.WeightList[listIndex].get(),self.schedList[listIndex].get(),1.5)
            # clear any responses and infusion counts if any
            self.L1ResponsesList[listIndex].set(0)
            self.L2ResponsesList[listIndex].set(0)
            self.InfList[listIndex].set(0)
            protocolNum = self.sched.index(self.schedList[listIndex].get())          
            self.outputText("<PROTOCOL "+str(boxIndex)+" "+str(protocolNum)+">")
            self.outputText("<PARAM "+str(boxIndex)+" "+str(self.paramNumList[listIndex].get())+">")
            self.outputText("<TIME "+str(boxIndex)+" "+str(self.SessionLengthList[listIndex].get()*60)+">")
            self.outputText("<IBI "+str(boxIndex)+" "+str(self.IBILengthList[listIndex].get()*60)+">")
            self.outputText("<PUMP "+str(boxIndex)+" "+str(self.PumpTimeList[listIndex].get())+">")
            # send Go signal
            self.outputText("<G "+str(boxIndex)+">")
            sched = self.schedList[listIndex].get()
            if sched == "0: Do not run":
                self.boxes[boxIndex].sessionStarted = False
            else:
                self.boxes[boxIndex].sessionStarted = True
                """
                if (self.Tzero == 0) self.outputText("<Q "+str(boxIndex)+">")
                """
                
        else:           
           self.writeToTextbox("No arduino connected",0)

    def startAllBoxes(self):
        self.writeToINIFile()
        self.outputText("<SYSVARS "+str(self.varCode)+">")
        for i in range(8):
            self.startSession(i)
            sleep(0.1) # Time in seconds.           

    def stopSession(self, boxIndex):
        self.outputText("<Q "+str(boxIndex)+">")

    def stopAllBoxes(self):
        for i in range(8):
            self.stopSession(i)
            # sleep(0.25) # Time in seconds.

    def sessionEnded(self, boxIndex):
        """
        Called when Feather sends "E" indicating that a box session has timed out
        or a "Q" command was received. 
        """
        self.boxes[boxIndex].sessionEnded()
        tempStr = "Box "+str(boxIndex+1)+" ended" 
        self.writeToTextbox(tempStr,0)
        

    def reportPhase(self,arduino):
        print("Report Phase for ardunino number",arduino)
        """
        self.outputText("<r>")
            { Serial.print(millis());
              if (phase == 0) Serial.println(" Prestart");
              if (phase == 1) Serial.println(" timein");
              if (phase == 2) Serial.println(" timeout");
              if (phase == 3) Serial.println(" finished");
        """

    def toggleEchoInput(self):
        self.outputText("<E>")       

    def reportPortStatus(self):

        if self.arduino0.activeConnection == True:
            self.writeToTextbox("arduino connected",0)
        else:
            self.writeToTextbox("arduino not connected", 0)          
                       
        print(self.arduino0.serialPort)
        print("Input",self.arduino0.inputThread)
        print("Output",self.arduino0.outputThread)
        print("input Queue", self.arduino0.inputQ)
        print("Output Queue", self.arduino0.outputQ)

    def updateTimer(self,sessionTime,listIndex):
        #sessionTime = (inputTokens[2])
        h = str(sessionTime // 3600)
        m = str((sessionTime % 3600) // 60)
        if (len(m) < 2):
            m = "0"+m
        s = str((sessionTime % 60))
        if (len(s) < 2):
            s = "0"+s
        self.sessionTimeStrList[listIndex].set(h+":"+m+":"+s)

    def display_abort_msg(self):
        """
        Non-blocking message window; tkinter info and error messgaes block until msg acknowledged or answered
        """
        
        labelfont = ('times', 20, 'bold')        
        msg_window = Toplevel(self.root) # Child of root window 
        msg_window.geometry("650x180+300+300")  # Size of window, plus x and y placement offsets 
        msg_window.title("Error Message")
        msg_window.config(bg='red')
        msg_window.config(borderwidth=5)
        msg_window.config(relief="sunken")
        self.msgStr = StringVar()
        self.msgStr.set("                   Session was ABORTED \r due to an unrecoverable input or output error ")

        label1 = ttk.Label(msg_window,textvariable = self.msgStr, background="White",foreground="Red")
        #option must be -column, -columnspan, -in, -ipadx, -ipady, -padx, -pady, -row, -rowspan, or -sticky
        label1.config(font=labelfont)       
        label1.grid(row=1,column=1, padx = 20, pady = 20, sticky='nesw')

        button1 = ttk.Button(msg_window, text='  OK  ',command = msg_window.destroy)
        button1.grid(row=2,column=1, padx=20, pady=10)

    def handleErrorTimeStamps(self,timeStamp,strCode,num1,num2):
        """
        Takes an error timestamp and updates the appropriate tkinter error IntVars,
        Then adds the timestamp to all data files of boxes currently running.        
        """

        codeDict = {'A':' Millis() on Connect ', \
                    '@':' Input error on port ', \
                    '#':' Recovered from input error on port ', \
                    '$':' Output error on port ', \
                    '%':' Recovered from output error ', \
                    '&':' chipsReset() ', \
                    '!':' Session Aborted! ', \
                    'r':' Recovery after resetChips() ', \
                    '(':' enterSafeMode() '
                    }

        self.sessionLog.append(str(timeStamp)+" "+strCode+codeDict[strCode]+str(num1))
        
        for i in range(8):
            if (self.boxes[i].sessionStarted == True) and (strCode != "A"):
                self.boxes[i].dataList.append([timeStamp, strCode])

        if (strCode == "A"):
            hrs = int(timeStamp/3600000)
            minutes = int((timeStamp - (hrs * 3600000))/60000)
            print("****************************************************")
            print(hrs,"hr(s) and",minutes,"min since FeatherM0 was rebooted")
            print("****************************************************")
        elif (strCode == "@"):
            if (num1 == 1): self.errorsL1.set(self.errorsL1.get()+1)
            elif (num1 == 2): self.errorsL1.set(self.errorsL2.get()+1)
        elif (strCode == "#"):
            if (num1 == 1): self.recoveriesL1.set(self.recoveriesL1.get()+1)
            if (num1 == 2): self.recoveriesL1.set(self.recoveriesL2.get()+1)   
        elif (strCode == "$"):
            self.outputErrors.set(self.outputErrors.get()+1)    
        elif (strCode == "%"):
            self.outputRecoveries.set(self.outputRecoveries.get()+1)
        elif (strCode == "r"):
            self.outputRecoveries.set(self.outputRecoveries.get()+1)   
        elif (strCode == "!"):
            print("self.send_abort_msg()")
            self.display_abort_msg()

    def handleInput(self, inputLine):
        """
        Document this!
        """
        codeNum = 99                  # Codes for box number, timer, errorCode etc. 
        strCode = "XX"                # either single char code or string comment
        timeStamp = 0                 # time in mSec
        level = 0                     # sets level of checkbox; also used for lever number in error codes
        index = -1         # For boxes, used as index of boolean VarList 
                                      # Checkboxes are organized in two dimensional arrays [BoxNum, Varlist]
        if (self.showDataStreamCheckVar.get() == 1):
            self.writeToTextbox(inputLine,0)
            # print(inputLine)
        tokens = inputLine.split()
        # print(inputLine, "length = ", len(tokens))
        try:
            if len(tokens) > 1:
                #print(tokens[0],tokens[1])
                codeNum = (int(tokens[0].decode()))
                strCode = tokens[1].decode()   # convert from "byte literal"
            if len(tokens) > 2:
                timeStamp = int(tokens[2].decode())
            if len(tokens) > 3:
                level = (int(tokens[3].decode()))
                index = (int(tokens[4].decode()))
        except:
            print('exception at getInput: ',tokens)   
        if (codeNum in [0,1,2,3,4,5,6,7]):
            listIndex = codeNum           
            if (strCode == "*"):    # timers get updated but nothing gets added to datafile
                self.updateTimer(timeStamp,listIndex)
            else:                   # every other timestamp gets added to the datafile
                self.boxes[listIndex].dataList.append([timeStamp, strCode])     # append timestamp to dataList - eventually datafile
                if (index >= 0):
                    self.boolVarLists[listIndex][index].set(level)           # update checkbox                   
                if (strCode == "L"):
                    self.L1ResponsesList[listIndex].set(self.L1ResponsesList[listIndex].get()+1)    # update L1 label
                elif (strCode == "H"):
                    self.L2ResponsesList[listIndex].set(self.L2ResponsesList[listIndex].get()+1)    # update HD label
                elif (strCode == "P"):
                    self.InfList[listIndex].set(self.InfList[listIndex].get()+1)                # update infusion label
                elif (strCode == "E"):
                    self.boxes[listIndex].sessionEnded()
        elif (codeNum == 8): self.boolVarLists[8][index].set(level)           # update debug checkbox 
        elif (codeNum == 9):
            print(strCode)
            # self.writeToTextbox(strCode,0)
        elif (codeNum == 10):     # Stuff for sessionLog
            self.handleErrorTimeStamps(timeStamp, strCode, level, index)     # level and index for various info as needed

    def periodic_check(self):
        if self.arduino0.activeConnection == True:    
            while not self.arduino0.inputQ.empty():
                try:
                    inputLine = self.arduino0.getInput()
                    self.handleInput(inputLine)
                except queue.Empty:
                    pass
        self.root.after(100, self.periodic_check)  # procedure reschedules its own reoccurance in 100 mSec

    def writeToTextbox(self,text,aTextBox):
        if aTextBox == 0:
            self.topTextbox.insert('1.0',text)
            self.topTextbox.insert('1.0',"\n")
        else:
            self.bottomTextbox.insert('1.0',text)
            self.bottomTextbox.insert('1.0',"\n")
        # print(text)

    def outputText(self,text):
        self.arduino0.outputQ.put(text)
        if self.showOutputCheckVar.get() == 1:
            self.writeToTextbox(text,1)
    
    def about(self):
        messagebox.showinfo("About",__doc__,parent=self.root)
        return
    
    def askBeforeExiting(self):
        self.saveAllData()
        aBoxStillRunning = False
        for i in range(8):
            if (self.boxes[i].sessionStarted == True) and (self.boxes[i].sessionCompleted == False):
                print("Box "+ str(i+1)+" still running")
                aBoxStillRunning = True

        response = True
        if aBoxStillRunning == True:
            response = messagebox.askyesno("Close Warning", "At Least One Box Is Still Running\n\n"+ \
                                           "End Session without Saving?")
        if (response == True):
            self.root.destroy()

    def go(self):
        self.root.after(100, self.periodic_check)
        self.root.mainloop()

class Box(object):
    def __init__(self,boxNum):
        """
        This function essentially creates a new box. Initial values are arbitrary
        The initialize procedure sets (or resets) the values after the box has been created. 
        """
        self.boxNum = boxNum
        self.sessionStarted = False
        self.sessionCompleted = False
        self.dataSaved = False       
        self.subject_ID_string = 'box'+str(boxNum)
        self.weight = 330
        self.schedNum = 0      # To Do: define schedules such as 0 = "do not run", 1 = FR etc.
        self.dose = 1.0
        self.dataList = []

    def initialize(self,ID_Str, initWeight, initSched, initDose):
        self.sessionStarted = True
        self.sessionCompleted = False
        self.dataSaved = False
        self.subject_ID_string = ID_Str
        self.weight = initWeight
        self.schedNum = initSched
        self.dose = initDose
        self.dataList = []

    def sessionEnded(self):
        """
        self.sessionCompleted is an important boolean which indicates that a session has started
        and has ended. It is used to decide whether to save a data file.

        This procedure is called when "E" is recieved from Feather indicating that the session has
        timed out or has met other criteria. But the Feather could also be responding to a "Q"
        command, which tells it to quit regardless of whether a session was runnning or not.       
        """
        if self.sessionStarted == True:                
            self.sessionCompleted = True

if __name__ == "__main__":
    sys.exit(main())  
    # exit(main())  see  http://stackoverflow.com/questions/6501121/the-difference-between-exit-and-sys-exit-in-python
