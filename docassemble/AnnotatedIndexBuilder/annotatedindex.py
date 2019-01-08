from docassemble.base.core import DAObject, DAList, DAFile, DAStaticFile
from docassemble.base.util import pdf_concatenate, path_and_mimetype
from docassemble.base.functions import space_to_underscore
import pycountry
import pdfkit
import csv, sys


def countries():
    return sorted([country.name for country in pycountry.countries])

def protected_class():
    return [
        'Race',
        'Color',
        'National Origin',
        'Religion',
        'Sex',
        'Familial Status (i.e. children)',
        'Disability',
        'Source of Income (e.g. a Section 8 voucher)',
        'Sexual Orientation',
        'Gender Identity',
        'Age',
        'Marital Status',
        'Veteran or Active Military Status',
        'Genetic Information'
    ]

def document_type():
    return [
        'news',
        'treatise/law overview',
        'study/report',
        'decision',
        'memorandum',
        'sample'
    ]

def location():
    return [
        'Boston',
        'Worcester',
        'Lowell',
        'Lawrence',
        'Springfield',
        'Northampton',
        'Fall River'
    ]

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

class CSVSearcher(AISearcher):
    """Allows you to use a basic CSV file with a list of files stored in the Docassemble Static folder as basis of AI Searcher"""
    def init(self, *pargs, **kwargs):
        super(CSVSearcher, self).init(*pargs, **kwargs)
        if hasattr(self, 'csv_file'):
            self.inflate(self.csv_file)
        
    def inflate(self,csv_file):
        """Load a CSV file that has a list of filenames that exist in the '/static' subfolder of the DA Package"""
        # We should strip out unicode characters in the fields
        file_list = load_from_csv(csv_file)
        for pdf in file_list:
            article = self.appendObject()
            article.title = pdf['Title']
            article.file = DAStaticFile(filename=pdf['File'])
            article.annotation = pdf['Excerpt']
            article.date = pdf['Date']
            article.citation = pdf['Citation']
            article.document_type = pdf['Document Type']
            self.append(article)
        self.gathered = True

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
        self.categories = set()

    def as_pdf(self):
        """Returns a concatenated PDF that represents the completed annotated index"""
        return pdf_concatenate([article.file  for article in self])

    def toc(self):
        """Returns a Microsoft Word Document with a table of contents for the index"""
        pass

    def append(self, item):
        super(AnnotatedIndex,self).append(item)
        if hasattr(item,'document_type'):
            self.categories.add(item.document_type)

class AIWebArticle(DAObject):
    def init(self, *pargs, **kwargs):
        super(AIWebArticle, self).init(*pargs, **kwargs)
        self.file = DAFile()
    def save_pdf(self):
        # self.file = DAFile()
        self.file.initialize(filename=space_to_underscore(self.title + '.pdf'))
        pdfkit.from_url(self.url, self.file.path())

class AIWebArticleList(DAList):
  def init(self, *pargs, **kwargs):                  
    super(AIWebArticleList, self).init(*pargs, **kwargs)         
    self.object_type = AIWebArticle

def load_from_csv(relative_path):
  """ Return a list containing a dictionary for each line of the CSV file at relative_path. Uses Docassemble path_and_mimetype to locate the path."""
  path = path_and_mimetype(relative_path)[0]
  reader = csv.DictReader(open(path,'r'))
  myList = []
  for line in reader:
    myList.append(line)
  del reader
  return myList    