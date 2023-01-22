#!/usr/bin/env python3
'''
Parse the <Notes and Highlights> from Kindle exported HTML.
Write data to the provided Notion page.
'''
import argparse
from kindle_parser import Book
from notion_writer import NotionWriter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--kindle_file', help='Path of the file to transcript')
    parser.add_argument('-c', '--credentials', help='Path of the credentials for Notion')
    parser.add_argument('-p', '--page_id', help='Notion page id where to write the notes')

    # Read input files
    args = parser.parse_args()

    # Parse html of the notes
    print("Parsing notes...")
    book = Book()
    book.parse_kindle_html(args.kindle_file)
    print("Done")

    # Writing them to Notion
    print("Writing notes...")
    writer = NotionWriter()
    writer._load_credentials_from_json(args.credentials)
    writer.write_book_notes(book, args.page_id)
    print("Done")