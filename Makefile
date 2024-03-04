all : commands

## commands    : show all commands.
@PHONY: commands
commands :
	@grep -E '^##' Makefile | sed -e 's/## //g'

## readme      : render the various README.qmd files to README.md in the repo
@PHONY: readme
readme:
	quarto render ./README.qmd
	quarto render ./data/README.qmd
	quarto render ./quarto-dashboard/README.qmd
	quarto render ./quarto-dashboard-param/README.qmd
	quarto render ./quarto-dashboard-theme/README.qmd
	quarto render ./shiny-express-app/README.qmd

## dashboards  : render the dashboards
@PHONY: dashboards
dashboards:
	quarto render quarto-dashboard/bikeshare-dashboard.qmd
	quarto render quarto-dashboard-param/bikeshare-param.qmd
	quarto render quarto-dashboard-theme/bikeshare-theme.qmd

## shiny       : run the shiny application in this repository
@PHONY: shiny
shiny:
	shiny run --reload --launch-browser shiny-express-app/app.py

## setup       : create a new python venv named learn-media-2024 and install packages
@PHONY: setup
setup:
	rm -rf venv; \
	python -m venv venv; \
	. venv/bin/activate; \
	venv/bin/python3 -m pip install -r requirements.txt; \
	echo "\n\nActivate the venv with: source venv/bin/activate\n\n";
