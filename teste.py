from app import *

content="""class Tools(object):
    def getEnviromentVar(self):

        enviromentsVar = {
            'GITSPEAKER_GH_MARKDOWNLINESNUMBER':'',
            'GITSPEAKER_GH_CODELINESNUMBER':'',
            'GITSPEAKER_GH_USERNAME':'',
            'GITSPEAKER_GH_PASSWORD':'',
            'GITSPEAKER_GH_REPOSITORYNAME':'', 
            'GITSPEAKER_GH_FIRSTFILENAME':'',
            'GITSPEAKER_GH_FILECONTENT':'',
        }
    
        for key, value in enviromentsVar.items():
            enviromentsVar[key] = os.environ.get(key)

        for key, value in enviromentsVar.items():
            enviromentsVar[key] = os.environ.get(key)
        return enviromentsVar
              
    def getFileExtension(self, filename):
        return filename.split('.')[1]"""

rows = content.splitlines()
content=Content.rows(rows, 20, len(rows))
print(content[0])
print(len(content[0].splitlines()))