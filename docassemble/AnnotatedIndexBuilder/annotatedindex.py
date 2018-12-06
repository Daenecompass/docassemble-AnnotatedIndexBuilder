from docassemble.base.core import DAObject, DAList
import pycountry

def countries():
    return [country.name for country in pycountry.countries]

def personal_characteristics():
    return [
        'religious persecution',
        'sexual orientation',
        'domestic violence',
        'ethnic persecution',
        'gang violence'
    ]

class AISearcher(DAObject):
    """An abstract interface that allows you to retrieve articles for creating an annotated index. 
    Initial version should work with SharePoint Online"""
    def init(self, *pargs, **kwargs):
        super(AISearcher, self).init(*pargs, **kwargs)
    def matches(date_after=None,date_before=None,characteristics=None,country=None,any=False):
        """Return a list of articles that match any or all of the specified filters"""
        pass

class AIArticle(DAObject):
    """A single item (article) used to document an asylee's claim"""

    def as_pdf(self):
        """Returns a DAFile that represents the article in PDF format, regardless of source format"""
        pass

class AnnotatedIndex(DAList):
    """A collection of articles and other documents to support an asylee's claim"""
    def init(self, *pargs, **kwargs):
        super(AnnotatedIndex, self).init(*pargs, **kwargs) 
        self.object_type = AIArticle

    def as_pdf(self):
        """Returns a concatenated PDF that represents the completed index"""
        pass

    def toc(self):
        """Returns a Microsoft Word Document with a table of contents for the index"""
        pass