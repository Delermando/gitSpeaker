from flask import render_template
from flask import Markup
from github import Github
import base64
from app import *

@app.route("/")
def index():
    var = Tools.getEnviromentVar()
    #fileContent = getFileGetContent(var['GITSPEAKER_GH_REPOSITORYNAME'], var['GITSPEAKER_GH_FIRSTFILENAME'])
    #    return base64.b64decode(gitFile.content)

    #user = Git.getGithubUser(var['GITSPEAKER_GH_USERNAME'], var['GITSPEAKER_GH_PASSWORD'])
    #repository = Git.getRepository(user, var['GITSPEAKER_GH_REPOSITORYNAME'])
    #dirContent = Git.getDirContentFromRepository(repository, '/')

    formatedContent = formatFileContent(
        'teste.css', 
        """
    @import url(../../lib/font/league-gothic/league-gothic.css);
    @import url(https://fonts.googleapis.com/css?family=Lato:400,700,400italic,700italic);
    /**
     * League theme for reveal.js.
     *
     * This was the default theme pre-3.0.0.
     *
     * Copyright (C) 2011-2012 Hakim El Hattab, http://hakim.se
     */
    /*********************************************
     * GLOBAL STYLES
     *********************************************/
    body {
      background: #1c1e20;
      background: -moz-radial-gradient(center, circle cover, #555a5f 0%, #1c1e20 100%);
      background: -webkit-gradient(radial, center center, 0px, center center, 100%, color-stop(0%, #555a5f), color-stop(100%, #1c1e20));
      background: -webkit-radial-gradient(center, circle cover, #555a5f 0%, #1c1e20 100%);
      background: -o-radial-gradient(center, circle cover, #555a5f 0%, #1c1e20 100%);
      background: -ms-radial-gradient(center, circle cover, #555a5f 0%, #1c1e20 100%);
      background: radial-gradient(center, circle cover, #555a5f 0%, #1c1e20 100%);
      background-color: #2b2b2b; }

    .reveal {
      font-family: 'Lato', sans-serif;
      font-size: 36px;
      font-weight: normal;
      color: #eee; }

    ::selection {
      color: #fff;
      background: #FF5E99;
      text-shadow: none; }

    .reveal .slides > section, .reveal .slides > section > section {
      line-height: 1.3;
      font-weight: inherit; }

    /*********************************************
     * HEADERS
     *********************************************/

    """, 
        10, 
        20,
        80
    )

    #formatedContent = formatFileContent(
    #    var['GITSPEAKER_GH_FIRSTFILENAME'], 
    #    var['GITSPEAKER_GH_FILECONTENT'], 
    #    var['GITSPEAKER_GH_MARKDOWNLINESNUMBER'], 
    #    var['GITSPEAKER_GH_CODELINESNUMBER'],
    #    var['GITSPEAKER_GH_CODECHARLIMIT']
    #)
    
    return render_template('index.html', content = Markup( formatedContent ))


def formatFileContent(filename, content, markdownLinesNumber, codeLinesNumber, charLimit):
    extension = Tools.getFileExtension(filename)
    if(extension == 'md'):
        numberOfLines = markdownLinesNumber 
    else:
        numberOfLines = codeLinesNumber
    
    contentGroups=Content.rows(content, numberOfLines, charLimit)

    return Section.set(contentGroups, Section.getPatter(extension))
    