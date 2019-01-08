from docassemble.base.core import DAObject, DAList, DAFile
from docassemble.base.util import pdf_concatenate
import pycountry

def countries():
    return sorted([country.name for country in pycountry.countries])

def grounds():
    return [
        'Race',
        'Political Opinion',
        'Religion',
        'Nationality',
        'Particular Social Group'
    ]

def subgrounds():
    return [
        'gender',
        'DV status',
        'children',
        'gang-related violence',
        'membership in a family/social group'
    ]

def harms():
    return [
        'physical violence',
        'torture',
        'genocide',
        'slavery',
        'threats of harm',
        'unlawful detention',
        'infliction of mental, emotional, or psychological harm',
        'substantial economic discrimination or harm',
        'other discrimination or harassment',
        'other violations of human rights'
    ]

class AISearcher(DAList):
    """An abstract interface that allows you to retrieve articles for creating an annotated index. 
    Initial version should work with SharePoint Online"""
    def init(self, *pargs, **kwargs):
        super(AISearcher, self).init(*pargs, **kwargs)
        #self.elements = list()
    def matches(self,date_after=None,date_before=None,characteristics=None,country=None,any=False):
        """Return a list of articles that match any or all of the specified filters"""
        pass
    #def append(self,item):
    #    self.elements.append(item)

    #def list_all(self):
    #    return self.elements

class AIArticle(DAObject):
    """A single item (article) used to document an asylee's claim"""
    def date_range(self):
        return (self.start_date,self.end_date)
    def characteristics(self):
        return self._characteristics
    def country(self):
        return self._country
    def set(self,file):
        """Set the file object"""
        if isinstance(file,DAFile):
            self.file = file
    def get(self):
        return self.file
    def as_pdf(self):
        """Returns a DAFile that represents the article in PDF format, regardless of source format"""
        if isinstance(self.file,DAFile):
            return self.file
        else:
            return self.file
    def  __unicode__(self):
        return self.title

    def __str__(self):
        return self.__unicode__()

class AnnotatedIndex(DAList):
    """A collection of articles and other documents to support an asylee's claim (dossier or annotated index)"""
    def init(self, *pargs, **kwargs):
        super(AnnotatedIndex, self).init(*pargs, **kwargs) 
        self.object_type = AIArticle

    def as_pdf(self):
        """Returns a concatenated PDF that represents the completed annotated index"""
        return pdf_concatenate([article.file  for article in self])

    def toc(self):
        """Returns a Microsoft Word Document with a table of contents for the index"""
        pass        