import wx
import cv2
import numpy as np

class MaskTester(wx.Frame):
    def __init__(self, parent, fps=15, height=240,width=320):
        wx.Frame.__init__(self, parent)
        self.SetName("Mask Tester Controller")
        
        #Boolean to handle exiting CV2 IMSHOW window
        self.exists = True
        
        #Colors for applying the mask
        self.upper_color = self.color_RGB2HSV([0,0,0])
        self.lower_color = self.color_RGB2HSV([0,0,0])
        
        self.cap = cv2.VideoCapture(0)
        cv2.useOptimized()
        self.cap.set(3, height)
        self.cap.set(4, width)
        
        ## GUI CODE BELOW ##
        MainBox    = wx.BoxSizer(wx.HORIZONTAL)
        
        StaticBox1 = wx.StaticBox(self,label='Lower Color')
        StaticBox2 = wx.StaticBox(self,label='Upper Color')
        LowerBox  = wx.StaticBoxSizer(StaticBox1, wx.VERTICAL)
        LowerSizer = wx.FlexGridSizer(3,3,10,15)
        UpperBox  = wx.StaticBoxSizer(StaticBox2, wx.VERTICAL)
        UpperSizer = wx.FlexGridSizer(3,3,10,15)
        
        ComboBoxSizer = wx.FlexGridSizer(1,2,10,15)
        self.ComboBoxText = wx.StaticText(self,id=1,label="Image from:\t")
        self.Choices  = ["Frame","HSV","Mask","Res"]
        self.ComboBox = wx.ComboBox(self,value=self.Choices[0],choices=self.Choices,style=wx.CB_READONLY)
        ComboBoxSizer.Add(self.ComboBoxText,flag=wx.ALIGN_CENTER)
        ComboBoxSizer.Add(self.ComboBox,flag=wx.ALIGN_CENTER)
        
        self.R_lowerTextLabel = wx.StaticText(self,id=1,label="R")
        self.G_lowerTextLabel = wx.StaticText(self,id=2,label="G")
        self.B_lowerTextLabel = wx.StaticText(self,id=3,label="B")
        self.R_lower = wx.Slider(self,id=1,value=0,minValue=0,maxValue=255,size=(200,20),style=wx.SL_HORIZONTAL)
        self.G_lower = wx.Slider(self,id=2,value=0,minValue=0,maxValue=255,size=(200,20),style=wx.SL_HORIZONTAL)
        self.B_lower = wx.Slider(self,id=3,value=0,minValue=0,maxValue=255,size=(200,20),style=wx.SL_HORIZONTAL)
        self.R_lowerText = wx.StaticText(self,id=1,label="0")
        self.G_lowerText = wx.StaticText(self,id=2,label="0")
        self.B_lowerText = wx.StaticText(self,id=3,label="0")
        
        LowerSizer.Add(self.R_lowerTextLabel,flag=wx.ALIGN_CENTER)
        LowerSizer.Add(self.R_lower,flag=wx.ALIGN_CENTER)
        LowerSizer.Add(self.R_lowerText,flag=wx.ALIGN_CENTER)
        LowerSizer.Add(self.G_lowerTextLabel,flag=wx.ALIGN_CENTER)
        LowerSizer.Add(self.G_lower,flag=wx.ALIGN_CENTER)
        LowerSizer.Add(self.G_lowerText,flag=wx.ALIGN_CENTER)
        LowerSizer.Add(self.B_lowerTextLabel,flag=wx.ALIGN_CENTER)
        LowerSizer.Add(self.B_lower,flag=wx.ALIGN_CENTER)
        LowerSizer.Add(self.B_lowerText,flag=wx.ALIGN_CENTER)
        
        self.R_upperTextLabel = wx.StaticText(self,id=1,label="R")
        self.G_upperTextLabel = wx.StaticText(self,id=2,label="G")
        self.B_upperTextLabel = wx.StaticText(self,id=3,label="B")
        self.R_upper = wx.Slider(self,id=4,value=0,minValue=0,maxValue=255,size=(200,20),style=wx.SL_HORIZONTAL)
        self.G_upper = wx.Slider(self,id=5,value=0,minValue=0,maxValue=255,size=(200,20),style=wx.SL_HORIZONTAL)
        self.B_upper = wx.Slider(self,id=6,value=0,minValue=0,maxValue=255,size=(200,20),style=wx.SL_HORIZONTAL)
        self.R_upperText = wx.StaticText(self,id=4,label="0")
        self.G_upperText = wx.StaticText(self,id=5,label="0")
        self.B_upperText = wx.StaticText(self,id=6,label="0")
        
        UpperSizer.Add(self.R_upperTextLabel,flag=wx.ALIGN_CENTER)
        UpperSizer.Add(self.R_upper,flag=wx.ALIGN_CENTER)
        UpperSizer.Add(self.R_upperText,flag=wx.ALIGN_CENTER)
        UpperSizer.Add(self.G_upperTextLabel,flag=wx.ALIGN_CENTER)
        UpperSizer.Add(self.G_upper,flag=wx.ALIGN_CENTER)
        UpperSizer.Add(self.G_upperText,flag=wx.ALIGN_CENTER)
        UpperSizer.Add(self.B_upperTextLabel,flag=wx.ALIGN_CENTER)
        UpperSizer.Add(self.B_upper,flag=wx.ALIGN_CENTER)
        UpperSizer.Add(self.B_upperText,flag=wx.ALIGN_CENTER)
        
        LowerBox.Add(LowerSizer,flag=wx.ALIGN_CENTER)
        UpperBox.Add(UpperSizer,flag=wx.ALIGN_CENTER)
        
        ControlSizer = wx.FlexGridSizer(3,1,1,1)
        ControlSizer.Add(ComboBoxSizer,flag=wx.ALIGN_CENTER)
        ControlSizer.Add(LowerBox,flag=wx.ALIGN_CENTER)
        ControlSizer.Add(UpperBox,flag=wx.ALIGN_CENTER)
        
        MainBox.Add(ControlSizer,flag=wx.ALIGN_CENTER)
        
        self.sliders = [self.R_lower,self.G_lower,self.B_lower,
                        self.R_upper,self.G_upper,self.B_upper]
        for slider in self.sliders:
            slider.Bind(wx.EVT_SLIDER,self.OnAdjust)
        
        self.ComboBox.Bind(wx.EVT_COMBOBOX, self.OnComboBox)
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        
        self.SetSizer(MainBox)
        self.Centre()
        self.Fit()
        self.Show(True)
        self.GenerateFrame()
    
    def OnComboBox(self,event):
        cv2.destroyAllWindows()
    
    def OnExit(self,event):
        self.exists = False
        self.Destroy()
    
    def OnAdjust(self, event):
        id = event.GetId()
        if id == 1:
            self.R_lowerText.SetLabel(str(self.R_lower.GetValue()))
        elif id == 2:
            self.G_lowerText.SetLabel(str(self.G_lower.GetValue()))
        elif id == 3:
            self.B_lowerText.SetLabel(str(self.B_lower.GetValue()))
        elif id == 4:
            self.R_upperText.SetLabel(str(self.R_upper.GetValue()))
        elif id == 5:
            self.G_upperText.SetLabel(str(self.G_upper.GetValue()))
        elif id == 6:
            self.B_upperText.SetLabel(str(self.B_upper.GetValue()))
        else:
            print("Unknown Event Id Called")
        
        self.UpdateColors()
    
    def color_RGB2HSV(self,RGB):
        BGR = [RGB[2],RGB[1],RGB[0]]
        #BGR = list(reversed(RGB))
        HSV = cv2.cvtColor(np.uint8([[BGR]]),cv2.COLOR_BGR2HSV)
        return np.array(HSV[0][0])
    
    def UpdateColors(self):
        RGB_lower = [self.sliders[i].GetValue() for i in range(0,3)]
        RGB_upper = [self.sliders[i].GetValue() for i in range(3,6)]
        self.lower_color = self.color_RGB2HSV(RGB_lower)
        self.upper_color = self.color_RGB2HSV(RGB_upper)
    
    def GenerateFrame(self):
        while self.exists:
            ret, frame = self.cap.read()
            if self.ComboBox.GetStringSelection() == "Frame":
                cv2.imshow('Frame', frame)
            else:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                if self.ComboBox.GetStringSelection() == "HSV":
                    cv2.imshow('HSV', hsv)
                else:
                    mask = cv2.inRange(hsv, self.lower_color, self.upper_color)
                    if self.ComboBox.GetStringSelection() == "Mask":
                        cv2.imshow('Mask', mask)
                    else:
                        res  = cv2.bitwise_and(frame,frame, mask=mask)
                        cv2.imshow('Res',res)
            val = cv2.waitKey(60) & 0xFF
            if val == 27:
                break
        cv2.destroyAllWindows()


app = wx.App()
window = MaskTester(None)
app.MainLoop()
