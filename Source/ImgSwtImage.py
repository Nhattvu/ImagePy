# This class represents a single image in the app

from kivy.core.image import Image as CoreImage

class ImgSwtImage():
    defaultPath = "./Source/Intro.png"
    path = defaultPath
    image = CoreImage(path)
    imageHeight = image.height
    imageWidth = image.width


    def loadImage(self, path, myRoot, project):

        project.undoActions.append(path)
        self.path = path
        myRoot.imageViewer.source = path
        self.image = CoreImage(path)
        self.imageHeight = self.image.height
        self.imageWidth = self.image.width
        myRoot.imgHeightLabel.text = ("Image Height: " + str(self.imageHeight))
        myRoot.imgWidthLabel.text = ("Image Width: " + str(self.imageWidth))

    