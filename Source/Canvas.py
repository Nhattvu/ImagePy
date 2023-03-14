# Canvas functionality is currently too buggy to be useful
# Debugging is hard and outside of current scope
# Can be moved to UserInterface.py once there is time to implement

#from kivy.graphics import Rectangle
#from kivy.graphics import Color
#from kivy.graphics import Point


# Canvas Functions

    # Canvas Variables
    # rect_box = ObjectProperty(None)
    # t_x = NumericProperty(0.0)
    # t_y = NumericProperty(0.0)
    # x1 = y1 = x2 = y2 = NumericProperty(0.0)




    # def enable_cropping(self):
    #    if(self.path != "Intro.png"):
    #        print("\nRootScreen:")
    #        print(self.ids.main_image.pos)
    #        print(self.ids.main_image.size)
    #       print("\tAbsolute size=", self.ids.main_image.norm_image_size)
    #        print("\tAbsolute pos_x=", self.ids.main_image.center_x -
    #             self.ids.main_image.norm_image_size[0] / 2.)
    #        print("\tAbsolute pos_y=", self.ids.main_image.center_y -
    #              self.ids.main_image.norm_image_size[1] / 2.)

    # def on_touch_down(self, touch):
        # checks whether on start screen
    #    if(self.path != "Intro.png"):
    #        self.x1 = touch.x
    #        self.y1 = touch.y
    #        self.t_x = touch.x
    #        self.t_y = touch.y
    #
    #        touch.grab(self)
    #        print(self.x1, self.y1)

    # def on_touch_move(self, touch):
    #    if touch.grab_current is self:
    #        # not working
    #        self.t_x = touch.x
    #        self.t_y = touch.y

    #        print(self.t_x, self.t_y)

    # def on_touch_up(self, touch):

    #    if touch.grab_current is self and self.path != "Intro.png":
    #        # final position
    #        self.x2 = touch.x
    #        self.y2 = touch.y

    #        print(self.x2, self.y2)