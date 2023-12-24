# Kindle \<Notes and Highlights> to Notion

> Parser that writes the \<Notes and Highlights> from Kindle exported HTMLs into a Notion page.

### Motivation

I have a terrible memory, so I've developed a habit of constantly highlighting passages and taking notes while reading on Kindle. However, simply highlighting and taking notes is not sufficient for me to retain the information. I've found that unless I rewrite the passages using my own words and intuition, I struggle to remember anything.

To ensure I truly comprehend and remember the content, I transcribe my Kindle notes into Notion and then write detailed summaries by myself. While transcribing the highlights may seem like a simple task, it can actually be quite tedious, even with the copy and paste functionality of Kindle.

To streamline this process and save time, I have created a small script that automates the transcription of my Kindle highlights into Notion. This script eliminates the need for manual copying and pasting, allowing me to focus more on the actual content and analysis.

## Installation

```bash
$ pip install git+https://github.com/ereverter/kindlenotionsync.git
```

## Usage

The following code will simply append the highlights and notes from the kindle export into the specified page from Notion:

```bash
$ python -m kindlenotionsync [-h] [-f KINDLE_FILE] [-c CREDENTIALS] [-p PAGE_ID]
```

To begin, you'll need to export your Kindle highlights. Start by downloading the Kindle app from Amazon and open one of your books. Look for a button located at the top right corner of the screen that allows you to export your highlighted content as an HTML file. This export will generate a file similar to the [export.html](export.html) file available in this repository.

Next, you'll need to store your credentials in the `credentials.json` file. You can refer to the example file [credentials.json](credentials.json) in this repository to see the required format. To obtain your API key, you'll first need to create an [integration](https://www.notion.so/my-integrations) in Notion.

In order to fetch the desired page link, you have a couple of options. You can either press `ctrl+L` while the block containing the page is selected, or click on the three dots at the top right corner of Notion and select the appropriate option from the drop-down menu. The link will always refer to the currently selected block. Make sure to copy the page ID, which is a long alphanumeric string and will look something like `https://www.notion.so/test-{page_id_here}?pvs=4`.

Finally, execute the code mentioned above. It will parse and load the exported file into Notion, resulting in the desired outcome as illustrated below:

<p align="center">
  <img src="notion.png" alt="Parsed Notes and Highlights in Notion">
</p>
