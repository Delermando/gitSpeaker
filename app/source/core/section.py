
class Section(object):
    def setWrapper(self, content, sectionPattner):
        html = ''
        for slide in content:
            html += sectionPattner % slide        

        if len(content) > 1:
            html = "<section>%s</section>" % html

        return html

    def set(self, content, sectionPattner):
        return sectionPattner % content

    def getPattern( self, fileExtension ):
        markdown = "<section data-markdown>%s</section>"
        code = "<section><pre><code>%s</code></pre></section>"
        if fileExtension == 'md':
            return markdown
        else:
            return code

    