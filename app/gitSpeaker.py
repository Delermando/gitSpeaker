from flask import Markup
import base64
from app import *

class GitSpeaker(object):

    
    def getFileContents(self,files):
        var = Tools.getEnviromentVar()
        response = ''
        for gitFl in files:
            response += Markup(self.formatFileContent(gitFl.name, base64.b64decode(gitFl.content).decode('utf-8')))
        return response

    def getLocalFileContents(self,files):
        var = Tools.getEnviromentVar()
        response = ''
        for gitFl in files:
            response += Markup(self.formatFileContent(gitFl['name'], gitFl['contents']))

        return Markup(response)

    def getWrapperFileContents(self,files):
        var = Tools.getEnviromentVar()
        response = ''
        for gitFl in files:
            response += Markup(self.formatFileContentWrapper(gitFl.name, base64.b64decode(gitFl.content), int(var['GITSPEAKER_GH_MARKDOWNLINESNUMBER']), int(var['GITSPEAKER_GH_CODELINESNUMBER']) ).decode('utf-8'))
    
        return response

    def formatFileContent(self, filename, content):
        extension = Tools.getFileExtension(filename)
        return Markup(Section.set(content, Section.getPattern(extension)))


    def getWrapperLocalFileContents(self,files, numbMarkDownLines, numberCodeLines):
        response = ''
        if len(files) > 1:
            for gitFl in files:
                response += Markup(self.formatFileContentWrapper(gitFl['name'], gitFl['contents'], numbMarkDownLines, numberCodeLines ))
        else:
            response = Markup(self.formatFileContentWrapper(files[0]['name'], files[0]['contents'], numbMarkDownLines, numberCodeLines ))
        return response


    def formatFileContentWrapper(self,filename, content, markdownLinesNumber, codeLinesNumber):
        extension = Tools.getFileExtension(filename)
        rows = content.splitlines()
        rowsLen = len(rows)
        if(extension == 'md'):
            contentGroups = Content.rowsMdFiles(rows, markdownLinesNumber, rowsLen)
        else:
            contentGroups = Content.rowsCodeFiles(rows, codeLinesNumber, rowsLen)
        return Section.setWrapper(contentGroups, Section.getPattern(extension))
