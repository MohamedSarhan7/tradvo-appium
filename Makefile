# Makefile for Django project

# Variables
PYTHON = python3
DJANGO = $(PYTHON) manage.py

# Targets
.PHONY: help install run migrate makemigrations test lint shell collectstatic

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  help            - Show this help message"
	@echo "  install         - Install the required packages"
	@echo "  run             - Run the Django development server"
	@echo "  migrate         - Apply database migrations"
	@echo "  makemigrations  - Create new database migrations"
	@echo "  test            - Run tests"
	@echo "  lint            - Run linting checks"
	@echo "  shell           - Open the Django shell"
	@echo "  collectstatic   - Collect static files"

install:
	pip install -r requirements.txt

run:
	$(DJANGO) runserver

migrate:
	$(DJANGO) migrate

makemigrations:
	$(DJANGO) makemigrations

test:
	$(DJANGO) test

lint:
	flake8

shell:
	$(DJANGO) shell

collectstatic:
	$(DJANGO) collectstatic --noinput
	
makemessages:
	django-admin makemessages -all

compilemessages:
	django-admin compilemessages