#!/bin/bash

source /app/venv/bin/activate

python main.py

pdflatex -output-directory=./output ./example_output.tex
