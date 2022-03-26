VENV := venv

# install virtualenv and dependencies.
# only run when requirements.txt changes.
install: requirements.txt
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
	./$(VENV)/bin/pip install -Ur requirements.txt
	@mkdir data
	@mkdir data/html
	@mkdir data/docs

# download and parse html files.
crawl: crawler/crawler.py crawler/parser.py
	@echo "running crawler/crawler.py"
	@./$(VENV)/bin/python3 crawler/crawler.py
	@echo "running crawler/parser.py"
	@./$(VENV)/bin/python3 crawler/parser.py

# start flask webserver.
web: processor/website.py processor/templates
	@echo "running webserver processor/website.py"
	@./$(VENV)/bin/python3 processor/website.py

clean_crawl:
	rm data/html/*
	rm data/docs/*
	rm data/corpus.json

# clean virtualenv and build.
clean:
	rm -rf venv
	rm -rf __pycache__
