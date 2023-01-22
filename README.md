# Kindle \<Notes and Highlights> to Notion

> Parser that writes the \<Notes and Highlights> from Kindle exported HTMLs into a Notion page.

### Motivation

My memory is terrible, for which I constanly highlight passages and take notes in Kindle. But that is not enough, so unless I rewrite them with my own words and intuition I will not remember anything. Thus, I always transcript the notes in Notion, and then write the summaries by myself. Transcribing the highlights is a tedious task, even if it only requires to copy and paste from Kindle. For that, I have programmed this small script to automate it.

## Installation

```bash
$ pip install git+https://github.com/eReverter/kindlenotionsync.git
```

## Usage

```bash
$ python3 -m kindlenotionsync [-h] [-f KINDLE_FILE] [-c CREDENTIALS] [-p PAGE_ID]
```