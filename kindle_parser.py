#!/usr/bin/env python3
'''

'''
from bs4 import BeautifulSoup
from collections import OrderedDict
from functools import total_ordering
import json
import re
import requests
import time
from tqdm import tqdm
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
            # element_text = format_text(element.get_text().strip().replace(u' \xa0', ''))

            if element_class == 'noteHeading':
                try:
                    self._handle_noteHeading(element, element_text, location_field)
                except Exception as e:
                    warnings.warn(f"Well, something failed: {e}")

            elif element_class == 'noteText':
                element_text = element_text.split('Highlight')[0] # Kindle error. noteText has two divs. Only the first is relevant.
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
        raw_text = element.get_text(strip=True)
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

        # Create the current Highlight
        if self.current_highlight is None:
            self.current_highlight = Highlight(loc=location, metadata=header)
            self.chapters[current_chapter].append(self.current_highlight)

class NotionWriter():
    def __init__(self, token=''):
        self.token = token
        self._update_headers()
    
    # Util methods

    def _load_credentials_from_json(self, file='credentials.json'):
        with open(file) as fp:
            credentials = json.load(fp)
            self.token = credentials['credentials']['token']
        self._update_headers()

    def _update_headers(self):
        self.headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    # Main method

    def write_book_notes(self, book, page_id):

        for chapter in tqdm(book.chapters):
            header = self._format_header(content=chapter, type='3')
            _ = self._append_block(header, parent_id=page_id)
            toggle = self._format_toggle(content='Book Notes')
            response = self._append_block(toggle, parent_id=page_id)
            current_toggle_id = json.loads(response.text)['results'][0]['id']
            for note in tqdm(book.chapters[chapter], leave=False):
                highlight = self._format_paragraph(note.text)
                _ = self._append_block(highlight, parent_id=current_toggle_id)

                if note.note:
                    note = self._format_paragraph(note.note, color='yellow_background')
                    _ = self._append_block(note, parent_id=current_toggle_id)

                time.sleep(.5)


    # Set of blocks that can be generated for Notion. Could be 
    # contained in one function but having one for each type 
    # seems easier to maintain

    def _append_block(self, data, parent_id):
        url = f'https://api.notion.com/v1/blocks/{parent_id}/children'
        response = requests.patch(url, data=json.dumps(data), headers=self.headers)

        return response

    def _format_header(self, content, type='3'):
        data = {
            "children": [{
                f"heading_{type}": {
                    "rich_text": [{
                        "text": {
                            "content": f"{content}"
                        }
                    }]
                }
            }]
        }
        return data

    def _format_toggle(self, content):
        data = {
            "children": [{
                "toggle": {
                    "rich_text": [{
                        "text": {
                            "content": f"{content}"
                        }
                    }]
                }
            }]
        }
        return data

    def _format_paragraph(self, content, color='default'):
        data = {
            "children": [{
                "paragraph": {
                    "rich_text": [{
                        "text": {
                            "content": f"{content}"
                        }
                    }],
                    "color": f"{color}" # yellow_background for notes
                }
            }]
        }
        return data

    # In case the books data needs to be retrieved for something

    def get_books_table(self, db_id):
        pass