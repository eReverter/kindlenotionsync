#!/usr/bin/env python3
'''
Parser for HTML files exported from Kindle <Notes and Highlights>.
Transcripts all highlights and notes into a Book object.
A Book is a dictonary, where each key is a chapter, and the values are the hihglights and notes of said chapter.
'''
from bs4 import BeautifulSoup
from collections import OrderedDict
from functools import total_ordering
import re
from utils import format_text
import warnings

@total_ordering
class Highlight:
    def __init__(self, loc=-1, metadata=''):
        self.text = ''
        self.note = '' # Personal note
        self.loc = loc # Location of the highlight
        self.metadata = metadata # Additional info in the text header

    def __eq__(self, other):
        return self.loc == other.loc

    def __lt__(self, other):
        return self.loc < other.loc

class Book:
    def __init__(self):
        self.title = ''
        self.author = ''
        self.chapters = OrderedDict()
        self.ignored_elements = set() # To check if new elements are added to kindle exports

        self.current_highlight = None # Create highlight and check if it is highlight/note
        self.type_of_last_highlight = None # To check if a note needs to be stored in highlight

    def parse_kindle_html(self, html_file, location_field='location'):
        with open(html_file, 'r', encoding='utf8') as f:
            html = f.read()
        
        # Kindle html is slightly broken, so we get all elements. 
        # Track current highlight in case it has an incoming note.
        soup = BeautifulSoup(html, 'html.parser')
        elements = soup.select('[class]')

        for element in elements:
            element_class = element['class'][0]
            element_text = self._get_element_text(element)

            if element_class == 'noteHeading':
                try:
                    self._handle_noteHeading(element, element_text, location_field)
                except Exception as e:
                    warnings.warn(f"Well, something failed: {e}")

            elif element_class == 'noteText':
                element_text = element_text.split('\n')[0] # Kindle error. noteText has two divs. Only the first is relevant.
                if self.type_of_last_highlight == 'Highlight':
                    self.current_highlight.text = element_text

                elif self.type_of_last_highlight == 'Note':
                    self.current_highlight.note = element_text
            
            elif element_class == 'sectionHeading':
                self.chapters[element_text] = []

            elif element_class == 'authors':
                self.author = element_text
            
            elif element_class == 'bookTitle':
                self.title = element_text

            else:
                self.ignored_elements.add(element_class)

    def _get_element_text(self, element):
        raw_text = element.get_text().strip()
        if raw_text:
            element_text = format_text(raw_text)
        else:
            element_text = None
        return element_text

    def _handle_noteHeading(self, element, element_text, location_field):
        # Get the metadata (header) of the element and get the text from it
        header = ' '.join(element.stripped_strings)
        location_match = re.search(rf"\b{location_field}\b[^0-9]+(\d+)", header.lower())

        # If location is not found, something is failing
        if location_match:
            location = int(location_match.group(1)) # First number after "location"
        else:
            warnings.warn(f"Header without 'location'. Empty header, different 'location' naming? : {header}")
            return

        self.type_of_last_highlight = header.split()[0]
        current_chapter = next(reversed(self.chapters))
        self.current_highlight = None

        # There is something wrong if type is not one of the following
        current_chapter_has_highlights = len(self.chapters[current_chapter])
        if self.type_of_last_highlight not in ['Highlight', 'Note']:
            warnings.warn(f"Type of last highlight does not match Highlight/Note: {header}")

        # If it is a note, store it to the highlight it corresponds, the last one
        elif self.type_of_last_highlight == 'Note' and current_chapter_has_highlights:
            self.current_highlight = self.chapters[current_chapter][-1]
                
        elif self.type_of_last_highlight == 'Note' and not current_chapter_has_highlights:
            warnings.warn(f"Note '{element_text}' in location '{location}' before any highlight in the chapter.")

        # Create the current Highlight even if type is not Highlight
        if self.current_highlight is None:
            self.current_highlight = Highlight(loc=location, metadata=header)
            self.chapters[current_chapter].append(self.current_highlight)