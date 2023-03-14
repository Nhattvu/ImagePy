import os
from ImgSwtImage import ImgSwtImage
from xml.dom import minidom
from xml.dom.minidom import parse
from shutil import make_archive
from shutil import unpack_archive
from shutil import copytree
from shutil import rmtree
from shutil import move

# TO DO
#   NEED TO MAKE PROJECT FILE FORMAT

class Project():
    projectName = "defaultName"
    projectsPath = './Projects/'
    tempPath = projectsPath + projectName + '/'
    finalPath = projectsPath + projectName + '.ip'
    historyPath = './History/'
    redoActions = []
    undoActions = []
    

    def getNewPath(self, ImgSwtImage):
        # Figures out the name of the next file
        # Each file has an index
        # Doesn't create the file
        currentPath = ImgSwtImage.path
        newIndex = str(len(self.undoActions))
        fileExtension = os.path.splitext(currentPath)[1]
        newPath = self.historyPath + newIndex + fileExtension
        print("newPath: " + newPath)
        return newPath
    
    def undo(self, myRoot):

        if len(self.undoActions) >= 2:
            self.redoActions.append(self.undoActions.pop())
            myRoot.image.loadImage(self.undoActions.pop(), myRoot, self)
            print("undoStack",self.undoActions,"redoStack",self.redoActions)

    def redo(self, myRoot):

        if len(self.redoActions) >= 1:
            myRoot.image.loadImage(self.redoActions.pop(), myRoot, self)
            print("undoStack",self.undoActions,"redoStack",self.redoActions)
    
    def emptyRedoStack(self):
        self.redoActions = []

    def emptyUndoStack(self):
        self.undoActions = []
    
    def saveDataToXML(self):

        # Document object is created here 
        root = minidom.Document()

        # Root Node 'Project' is created here
        project_RootNode = root.createElement('Project')
        project_RootNode.setAttribute('name', self.projectName)
        root.appendChild(project_RootNode)

        # Undo and Redo child nodes are created and added
        undo_Node = root.createElement('undoList')
        redo_Node = root.createElement('redoList')
        project_RootNode.appendChild(undo_Node)
        project_RootNode.appendChild(redo_Node)

        # Undo and Redo Items are created as child nodes and added
        for element in self.undoActions:
            newNode = root.createElement('File')
            newNode.setAttribute('name', str(element))
            undo_Node.appendChild(newNode)
        for element in self.redoActions:
            newNode = root.createElement('File')
            newNode.setAttribute('name', str(element))
            redo_Node.appendChild(newNode)

        # File is written to disk
        xml_str = root.toprettyxml(indent ="\t")
        if not os.path.exists(self.tempPath):
            os.makedirs(self.tempPath)
        outputDir = self.tempPath+'ProjectData.xml'
        with open(outputDir, "w") as f:
            f.write(xml_str)



    def saveProject(self):
        
        if os.path.exists(self.tempPath):
    #        if USER AGREES to delete project:
    # Issues with commented out pop-up kept me from finishing
            rmtree(self.tempPath)
            copytree(self.historyPath, self.tempPath)
    #        else:
    #            return False
        else:
            copytree(self.historyPath, self.tempPath)
        self.saveDataToXML()
        make_archive(self.projectName,'zip',root_dir=self.tempPath,base_dir=None)
        rmtree(self.tempPath)
        move('./'+self.projectName+'.zip',self.finalPath)
        return True
    
    def importProject(self, projectFileName):
        self.emptyRedoStack()
        self.emptyUndoStack()
        if os.path.exists(self.historyPath):
            rmtree(self.historyPath)
        os.makedirs(self.historyPath)
        unpack_archive(self.projectsPath+projectFileName, self.historyPath, 'zip')
        self.projectName = os.path.splitext(projectFileName)[0]
        xmlData = parse(self.historyPath+'ProjectData.xml')
        # Importing Undo List
        undoList = xmlData.getElementsByTagName('undoList')
        for item in undoList:
            for File in item.getElementsByTagName('File'):
                self.undoActions.append(File.getAttribute('name'))
        # Importing Redo List
        redoList = xmlData.getElementsByTagName('redoList')
        for item in redoList:
            for File in item.getElementsByTagName('File'):
                self.redoActions.append(File.getAttribute('name'))



        #print(name1)

    def makeNewProject(self):
        self.emptyRedoStack()
        self.emptyUndoStack()
        if os.path.exists(self.historyPath):
            rmtree(self.historyPath)
        os.makedirs(self.historyPath)