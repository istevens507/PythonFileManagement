# Project Info

## On .vscode / settings.json
1. python.analysis.extraPaths is the specific setting name used by Pylance for its language analysis.
2. You can use "${workspaceFolder}" to specify paths relative to your project's root folder.

## Libraries - site-packages
* ${workspaceFolder}/.venv/lib/python3.11/site-packages"

## Create virtual environment
* py -m venv .venv

## Activate a virtual environment
* .venv\Scripts\activate

## Business Jobs directory
1. This directory will contain scripts that performs business tasks
    * For example: take a *.txt file, extract some information and create *.pdf files