from flask import render_template
from flask import Markup
from app import app
from github import Github
import base64
import os


@app.route("/")
def index():
    #fileContent = getFileGetContent(os.environ.get('GITSPEAKER_GH_REPOSITORYNAME'), 'MarkNotUsedObejctsInFunction.py')
    fileContent = """
        import sublime, sublime_plugin, pprint
        import re

        class MarkNotUsedObejctsInFunction(sublime_plugin.TextCommand):

            def run(self, edit):
            print(self.view.size())
        """
    fileContentb = """
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
.reveal h1, .reveal h2, .reveal h3, .reveal h4, .reveal h5, .reveal h6 {
  margin: 0 0 20px 0;
  color: #eee;
  font-family: 'League Gothic', Impact, sans-serif;
  font-weight: normal;
  line-height: 1.2;
  letter-spacing: normal;
  text-transform: uppercase;
  text-shadow: 0px 0px 6px rgba(0, 0, 0, 0.2);
  word-wrap: break-word; }

.reveal h1 {
  font-size: 3.77em; }

    """

    formatedContent = formatFileContent('MarkNotUsedObejctsInFunction.py', fileContent)

    return render_template('index.html', content = Markup( formatedContent ))



def getFileGetContent(repositoryName, filename):
    github = Github(os.environ.get('GITSPEAKER_GH_USERNAME'), os.environ.get('GITSPEAKER_GH_PASSWORD'))
    user = github.get_user()
    repository = user.get_repo( repositoryName )
    gitFile = repository.get_contents( filename )
    return base64.b64decode(gitFile.content)



def groupRows( rows, rowsNumber, contentRowsNumber):
    groups = []
    group = ''

    if contentRowsNumber <= rowsNumber:
        contentRange = [0]
    else:
        contentRange = range(0, rowsNumber)

    for time in contentRange:
        for row in rows[ time : time + rowsNumber]:
            group += row + '\n'
        groups.append(group)
        group = ''
    
    return groups




def formatFileContent(filename, content):
    extension = filename.split('.')[1]
    if(extension == 'md'):
        pattern = getFormatPatterByFileExtension(extension)
        contentGroups = groupRows(content.splitlines(), 10, content.count('\n'))
        formatedContent = createSection(contentGroups, pattern)
    else:
        pattern = getFormatPatterByFileExtension(extension)
        contentGroups = groupRows(content.splitlines(), 19, content.count('\n'))
        formatedContent = createSection(contentGroups, pattern)
    return formatedContent


def getFormatPatterByFileExtension( fileExtension ):
    markdown = "<section data-markdown>%s</section>"
    code = "<section><pre><code>%s</code></pre></section>"
    if fileExtension == 'md':
        return markdown
    else:
        return code

def createSection(content, sectionPattner):
    html = ''
    print(type(content))
    print(len(content))

    for slide in content:
        html += sectionPattner % slide
        

    if len(content) > 1:
        html = "<section>%s</section>" % html

    print(html)
    return html
