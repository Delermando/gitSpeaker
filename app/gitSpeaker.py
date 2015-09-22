from flask import Markup
import base64
from app import *

class GitSpeaker(object):

    def formatFileContent(self, filename, content):
        extension = Tools.getFileExtension(filename)
        return Section.setWrapper(content, Section.getPatter(extension))


    def getLocalFileContents(self,files, numbMarkDownLines, numberCodeLines):
        response = ''
        if len(files) > 1:
            for gitFl in files:
                print(gitFl['name'])
                response += Markup(self.formatFileContentWrapper(gitFl['name'], gitFl['contents'], numbMarkDownLines, numberCodeLines ).decode('utf-8'))
        else:
            response = Markup(self.formatFileContentWrapper(files[0]['name'], files[0]['contents'], numbMarkDownLines, numberCodeLines ).decode('utf-8'))
        return response

    def getFileContents(self,files):
        response = ''
        if files['type'] == 'tree':
            for gitFl in files['file']:
                response += Markup(GitSpeaker.formatFileContentWrapper(gitFl.name, base64.b64decode(gitFl.content), int(var['GITSPEAKER_GH_MARKDOWNLINESNUMBER']), int(var['GITSPEAKER_GH_CODELINESNUMBER']) ).decode('utf-8'))

        response = Markup(GitSpeaker.formatFileContentWrapper(files['file'].name, base64.b64decode(files['file'].content), int(var['GITSPEAKER_GH_MARKDOWNLINESNUMBER']), int(var['GITSPEAKER_GH_CODELINESNUMBER']) ).decode('utf-8'))
        return response

    def formatFileContentWrapper(self,filename, content, markdownLinesNumber, codeLinesNumber):
        extension = Tools.getFileExtension(filename)
        rows = content.splitlines()
        rowsLen = len(rows)
        if(extension == 'md'):
            contentGroups = Content.rowsMdFiles(rows, markdownLinesNumber, rowsLen)
        else:
            contentGroups = Content.rowsCodeFiles(rowsLen, codeLinesNumber, rowsLen)
        return Section.set(contentGroups, Section.getPatter(extension))

    def formatLocalFileContentWrapper(self):
        pass