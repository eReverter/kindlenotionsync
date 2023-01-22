#!/usr/bin/env python3
'''

'''
import json
import requests
import time
from tqdm import tqdm
import warnings

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

        if response.test != 200:
            warnings.warn(f"Something failed while appending blocks: {response.text}")
            
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