# Kindle \<Notes and Highlights> to Notion

> Parser that writes the \<Notes and Highlights> from Kindle exported HTMLs into a Notion page.

### Motivation

I have a terrible memory, so I've developed a habit of constantly highlighting passages and taking notes while reading on Kindle. However, simply highlighting and taking notes is not sufficient for me to retain the information. I've found that unless I rewrite the passages using my own words and intuition, I struggle to remember anything.

To ensure I truly comprehend and remember the content, I transcribe my Kindle notes into Notion and then write detailed summaries by myself. While transcribing the highlights may seem like a simple task, it can actually be quite tedious, even with the copy and paste functionality of Kindle.

To streamline this process and save time, I have created a small script that automates the transcription of my Kindle highlights into Notion. This script eliminates the need for manual copying and pasting, allowing me to focus more on the actual content and analysis.

## Installation

```bash
$ pip install git+https://github.com/eReverter/kindlenotionsync.git
```

## Usage

The following code will simply append the highlights and notes from the kindle export into the specified page from Notion:

```bash
$ python3 -m kindlenotionsync [-h] [-f KINDLE_FILE] [-c CREDENTIALS] [-p PAGE_ID]
```

First, you will need to store your credentials in the `credentials.json` file, as exemplified in the [credentials.json](credentials.json) example file in the repository.

Second, you need to fetch the desired page.
