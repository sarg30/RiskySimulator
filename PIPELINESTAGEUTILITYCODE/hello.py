from userinstruct import takeinput
from kivymd.app import MDApp
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder
import os
from kivy.core.window import Window
import ctypes
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
Window.size = (screensize[0]/1.4, screensize[1]/1.4)
arr = []
class FileChoosePopup(Popup):
    load = ObjectProperty()


class Tab(TabbedPanel):
    file_path = StringProperty("No file chosen")
    the_popup = ObjectProperty(None)

    def open_popup(self):
        self.the_popup = FileChoosePopup(load=self.load)
        self.the_popup.open()


        

    def load(self, selection):
        self.file_path = str(selection[0])
        self.the_popup.dismiss()
        global arr
        #print(self.file_path)
        # check for non-empty list i.e. file selected
        if self.file_path:
            
            arr = takeinput(self.file_path)
            #print(arr)
            ele =""
            count =0
            count2=0
            for i in arr:
                count=count+1
                ele = ele + str(count) +" "
                for j in i:
                    ele = ele+" "+j
                ele = ele +"\n"
                if count==1:
                    count2=len(ele)
       
            self.ids.newstuff.text = ele
            self.ids.newstuff.select_text(0,count2)
            self.ids.get_file.text = self.file_path


Builder.load_file('main.kv')


class RiscSimulator(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        #Window.clearcolor =  (0,0,1,1)
        return Tab()


if __name__ == "__main__":
    RiscSimulator().run()