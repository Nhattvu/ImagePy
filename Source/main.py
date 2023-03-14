# SOURCES
# https://www.youtube.com/watch?v=6gNpSuE01qE&t=135s
# uses BUILDOZER to build apk, requires Linux
# https://stackoverflow.com/questions/51913956/kivy-user-touch-and-drag-for-cropping-function



import time
import shutil
import os
# This disables the touchpad as a touch screen.
# May have unintended consequences.
os.environ['KCFG_INPUT_%(NAME)S'] = ''
from kivy.lang import Builder
import kivy
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout

from kivy.uix.filechooser import FileChooserListView
from kivymd import images_path
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.core.window import Window
from sympy import content
from kivy.core.image import Image as CoreImage
from kivy.uix.widget import Widget

from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from PIL import Image
from PIL.ExifTags import TAGS

# These are our internal modules which we wrote ourselves
import modules.adaptiveThresholding as adThresh
import modules.histogramEqualization as histEq
from ImgSwtImage import ImgSwtImage
from Project import Project
from MakeApiCall import MakeApiCall

#kivy drop down menu new imports
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
# Required for pop-up boxes
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.textfield import MDTextField

from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.textfield import MDTextField


kivy.require('2.1.0')

class Login(MDScreen):
    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)
        parameters = {}
        # Api Endpoints can be included in an encrypted file
        # Not within scope
        api = "https://imagesuiteapi.basili.bid/health_check"
        response = MakeApiCall.get_user_data(self, api, parameters)
        toast(str(response), duration = 10)

    

class Signup(MDScreen):
    pass

class Projects(MDScreen):
    image = ImgSwtImage()
    project = Project()

    def __init__(self, **kwargs):
        super(Projects, self).__init__(**kwargs)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True,
        )
        

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_manager()
        self.image.path = path
        newPath = self.project.getNewPath(self.image)
        shutil.copy(path,newPath)
        self.image.loadImage(newPath,self,self.project)
        self.project.emptyRedoStack()
        toast(self.image.path)

    def file_manager_open(self):
        self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True
        self.file_manager.background_color_selection_button="brown"

    def import_new_image(self):
        self.file_manager_open()

    def importProject(self, fileName='defaultName.ip'):
        self.project.importProject(fileName)
        print(self.project.undoActions)
        if len(self.project.undoActions) !=0:
            self.image.loadImage(self.project.undoActions[len(self.project.undoActions)-1], self, self.project)
        else: 
            self.image.loadImage(self.image.defaultPath, self, self.project)
        self.project.undoActions.pop()

    def makeNewProject(self):
        self.project.makeNewProject()
        self.image.loadImage(self.image.defaultPath, self, self.project)
        self.project.emptyUndoStack()


class SmoothCard(MDFloatLayout):
    image = ImgSwtImage()
    project = Project()

    def __init__(self, **kwargs):
        super(SmoothCard, self).__init__(**kwargs)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True,
        )
        self.image = ImgSwtImage()
        self.project = Project()


    
        

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_manager()
        self.image.path = path
        newPath = self.project.getNewPath(self.image)
        shutil.copy(path,newPath)
        self.image.loadImage(newPath,self,self.project)
        self.project.emptyRedoStack()
        toast(self.image.path)
    def file_manager_open(self):
        self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True
        self.file_manager.background_color_selection_button="brown"
    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

class Content(MDFloatLayout):
    pass
class Root(MDScreen):

    image = ImgSwtImage()
    project = Project()
    
    def __init__(self, **kwargs):
        super(Root, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True,
        )
        
        # Initializes the image which is temporary data
        self.image = ImgSwtImage()
        # Initializes the project data for use and later saving
        self.project = Project()
        

    def file_manager_open(self):
        self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True
        self.file_manager.background_color_selection_button="brown"

    def equalizeImage(self):
        newPath = self.project.getNewPath(self.image)
        histEq.histogram_Equalization(
            self.image.path,newPath, 0, self.image.imageHeight, 0, self.image.imageWidth)
        self.image.loadImage(newPath, self, self.project)
        self.project.emptyRedoStack()

    
    #def method that routs to root and runs file_manager_open
    def on_enter(self, *args):
        self.file_manager_open()

    #  def test1(self.image.path,newPath, 0, self.image.imageHeight, 0, self.image.imageWidth:) 
    #      print(self.root.ids.TopLeftid.text)

    def test1(self):
        height = self.ids.TopLeftid.text
        xh = height.split(",")
        x = xh[0]
        h = xh[1]
        width = self.ids.BottomRightid.text
        yd = width.split(",")
        y = yd[0]
        d = yd[1]
        newPath = self.project.getNewPath(self.image)
        histEq.histogram_Equalization(
            self.image.path,newPath,int(x),int(h),int(y),int(d))
        self.image.loadImage(newPath, self, self.project) 
        self.ids.info.text = ("\n\nImage was equalized from pixel " + str(x))+(" vertically to pixel " + str(h)) +(" and from pixel " + str(y))+(" horizontally to pixel " + str(d))
        self.project.emptyRedoStack()

    def thresholdImage(self):
        newPath = self.project.getNewPath(self.image)
        adThresh.adaptive_Thresholding(self.image.path, newPath, "Gaussian")
        self.image.loadImage(newPath, self, self.project)
        self.project.emptyRedoStack()

    def test2(self):
        newPath = self.project.getNewPath(self.image)
        adThresh.adaptive_Thresholding(self.image.path, newPath, "Mean")
        self.image.loadImage(newPath, self, self.project)
        self.project.emptyRedoStack()


    def importProject(self, fileName='defaultName.ip'):
        self.project.importProject(fileName)
        print(self.project.undoActions)
        if len(self.project.undoActions) !=0:
            self.image.loadImage(self.project.undoActions[len(self.project.undoActions)-1], self, self.project)
        else: 
            self.image.loadImage(self.image.defaultPath, self, self.project)
        self.project.undoActions.pop()

    def makeNewProject(self):
        self.project.makeNewProject()
        self.image.loadImage(self.image.defaultPath, self, self.project)
        self.project.emptyUndoStack()

    def saveProject(self):
        result = self.project.saveProject()
        goodResult = "File saved Successfully as" + self.project.finalPath
        if result:
            toast()
        else:
            toast("Failed to save project")



    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_manager()
        self.image.path = path
        newPath = self.project.getNewPath(self.image)
        shutil.copy(path,newPath)
        self.image.loadImage(newPath,self,self.project)
        self.project.emptyRedoStack()
        toast(self.image.path)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def menuDropDown(self):
        self.menu_list = [
            {
                "viewclass": "OneLineListItem",
                "text": "Adaptive Mean Threadholding",
                "on_press": lambda x = "Adaptive Mean Threadholding" : self.test2()
            }
        ]
        self.menu = MDDropdownMenu(
            caller = self.ids.menu,
            items = self.menu_list,
            width_mult = 4
        )
        self.menu.open()


class ContentNavigationDrawer(MDBoxLayout):
    pass


class MyScreenManager(ScreenManager):
    pass


class ImgSuite(MDApp):
    dialog = None

    def build(self):
        # Decides what uneditable items will look like 
        # such as the file chooser
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        screen = Root()

        # Sets the left hamburger menu to closed
        screen.nav_drawer.set_state("closed")



        sm = ScreenManager()
        sm.add_widget(Login(name="Login"))
        sm.add_widget(Signup(name="Signup"))
        sm.add_widget(Projects(name="Projects"))
        sm.add_widget(Root(name="Root"))
        return sm


    
    def show_passwordlogin(self, checkbox, value):
        if value: 
            self.root.get_screen('Login').ids.pwd.password = False
            self.root.get_screen('Login').ids.show.text = "Hide password"
        else: 
            self.root.get_screen('Login').ids.pwd.password = True
            self.root.get_screen('Login').ids.show.text = "Show password"
    
    def show_passwordsignup(self, checkbox, value):
        if value: 
            self.root.get_screen('Signup').ids.pwd.password = False
            self.root.get_screen('Signup').ids.pwdconf.password = False
            self.root.get_screen('Signup').ids.show.text = "Hide password"
        else: 
            self.root.get_screen('Signup').ids.pwd.password = True
            self.root.get_screen('Signup').ids.pwdconf.password = True
            self.root.get_screen('Signup').ids.show.text = "Show password"

    
    def remove_limit(self):
        print("true")

    def add_cards(self):
        new_card = SmoothCard()
        self.root.get_screen('Projects').ids.addbuttonid.add_widget(new_card)        
   
   
    def show_custom_dialog(self):
        content_cls = Content()
        self.dialog = MDDialog(
                title="Enter the name of your file:",
                 content_cls=content_cls,
                type="custom",
                buttons = [MDFlatButton(text="Cancel",on_release=self.close_dialog), 

                        MDRectangleFlatButton(text="Ok",on_release=lambda x:self.get_data(x,content_cls),
                        )],
                )

        self.dialog.open()

    def close_dialog(self, instance):
        if self.dialog:
            self.dialog.dismiss()

    def get_data(self, instance_btn, content_cls):
        textfield = content_cls.ids.pin
        value1 = textfield._get_text()
        # do stuffs here
        print(value1)
    
        self.close_dialog(instance_btn)     

    # def infor(self):
    #     img = Image.open(self.image)
    #     exifdata = img.getexif()

    #     for tagid in exifdata:
    #         tagname = TAGS.get(tagid, tagid)

    #         value = exifdata.get(tagid)

    #         print(f"{tagname:16}: {value}")
        


    

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Overwrite Project?",
                text="A Project with this name is already present.",
                buttons=[
                    MDFlatButton(
                        text="NO",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda _: self.dialog.dismiss(),
                    ),
                    MDFlatButton(
                        text="YES",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda _: self.dialog.dismiss(),
                    ),
                ],
            )
        self.dialog.open()

if __name__ == '__main__':
    ImgSuite().run()
