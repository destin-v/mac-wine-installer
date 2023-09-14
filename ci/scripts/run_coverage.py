"""This file should be placed in your ./src directory.  When ready to run coverage simply run this script."""
from os import system

# Run coverage using pytest, then record results to docs.
system("coverage run -m pytest")
system("coverage html -d 'save/coverage'")
system("coverage report -m")
