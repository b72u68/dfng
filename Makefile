VENV := venv

.PHONY: setup crawl index web all

# install virtualenv and dependencies.
# only run when requirements.txt changes.
setup: requirements.txt
ifeq (, $(shell which python3))
	@echo "[error] missing dependencies: missing python3"
	@echo "installing python3"
	@sudo apt-get install python3
else
	@echo "python3 found"
endif

ifeq (, $(shell which pip3))
	@echo "[error] missing dependencies: missing pip3"
	@echo "installing python3-pip"
	@sudo apt-get install python3-pip
else
	@echo "pip3 found"
endif

	@pip3 show -q virtualenv; \
		if [ $$? -ne 0 ]; \
		then \
			echo "[error] missing dependencies: missing virtualenv"; \
			echo "installing virtualenv"; \
			pip3 install virtualenv; \
		fi
	python3 -m venv $(VENV)
	@echo "installing required libraries."
	./$(VENV)/bin/pip install -Ur requirements.txt
	@echo "running settings script."
	./$(VENV)/bin/python3 settings.py

# download and parse html files.
crawl: crawler/crawler.py crawler/parser.py
	@echo "running crawler/crawler.py"
	./$(VENV)/bin/python3 crawler/crawler.py
	@echo "\nrunning crawler/parser.py"
	./$(VENV)/bin/python3 crawler/parser.py

# construct inverted index from corpus and write to disk.
index: indexer/indexer.py
	@echo "running indexer/indexer.py"
	./$(VENV)/bin/python3 indexer

# start flask webserver.
web: processor/website.py
	@echo "running webserver processor/website.py"
	./$(VENV)/bin/python3 processor/website.py

# clean crawled data
clean_crawl:
	rm -rf data/html/*
	rm -rf data/docs/*
	rm -rf data/corpus.json

# clean index file
clean_index:
	rm -rf index/index.pickle
	touch index/index.pickle

# clean virtualenv and build.
clean:
	rm -rf venv
	rm -rf __pycache__

all: crawl index web
	make crawl
	make index
	make web
