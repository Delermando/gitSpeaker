import os
import glob


class Tools(object):

    def getEnviromentVar(self):
        enviromentsVar = {
            'GITSPEAKER_GH_ENVIRONMENT':'',
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

        return enviromentsVar

            
    def getFileExtension(self, filename):
        return filename.split('.')[1]

    def getLocalContent( self, urlPath ):
        return open(urlPath).read().decode('utf-8')

    def getLocalFileList(self, path, operator):
        return sorted(glob.glob('app/mock/'+path + operator))