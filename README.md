# Definitely not Google

Definitely not Google is a simple information retrieval system that I did for
CS429: Information Retrieval individual project.

## Installation

1. Clone this project to your local machine.

```
$ git clone https://github.com/b72u68/dfng
```

2. Install all dependencies and set up virtual environment for the system.

```
$ cd dfng && sudo make
```

## Running the system

Run the crawler and parser to install and parse texts from the HTML files.

```
$ make crawl
```

Run the indexer to build a Scikit-learn based TF-IDF index from crawled corpus.

```
$ make index
```

Run the processor to handle free text queries and start the website at
`127.0.0.1:5000`.

```
$ make web
```

To run all components in one command, run the following script:

```
$ make all
```

## Clean

Clean all the HTML files and document corpus from running the crawler.

```
$ make clean_crawl
```

Clean inverted index.

```
$ make clean_index
```

Remove virtual environment.

```
$ make clean
```
