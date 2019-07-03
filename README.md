## About

**Note:** This project is very much a work in progress. Feel free to try it out
and even contribute if you like, but know it's only in the very early stages
and will likely continue to change substantially.

The purpose of the project is to provide an **interactive utility for exploring
and transforming CSV-based datasets.**

Most systems, if they allow you to export data, allow you to do so as CSV
files. I have frequently found myself needing to transform data exported from
one system as CSV into some other form for use in another or to create reports,
etc. A few years ago I discovered the wonderful
[Agate](https://github.com/wireservice/agate) library. You could also use
something like [Pandas](https://pandas.pydata.org) for analyzing CSV files, but
I found Pandas to be overkill for the kind of work I generally needed to do,
which were simple transformations and analysis on not very huge datasets.

Agate is awesome at what it does but I found myself writing a lot of the same
code over and over again. And needing to write a lot of _interim_ code in order
to understand the CSV files I was working with enough to create the final
output. For projects where I was working with similarly structured data more
than a few times, I did abstract some of the code a bit. Working with new
datasets still required a decent amount of Python knowledge. For a while now
I've wanted a more general purpose tool that was easy to use by folks
unfamiliar with Python. 

### Goals

- Built for Python 3+.
- Functional for a wide range of CSV-based datasets.
- Usable by folks unfamiliar with programming.
- Showcase good software engineering skills. Be pythonic.

## Installation

- Make sure you have Python 3 installed. 
- Clone repository.
- Run `pip install requirements.txt`.

## TODO

There is so much to do on this project. 

The meta stuff includes:

- Add tests. _(IN PROGRESS, using unittest)_.
- Add documentation.
- Add mypy type hinting. _(IN PROGRESS)_
- Set up linting and make sure following PEP8.
- Refactor using asyncio?
- ~~Decide on and add a license.~~ _(DONE, MIT)_

Smaller tasks on the near horizon include (e.g. next tasks I'm working on):

- ~~Extend Agate to have describe table methods that load column info into easily
  accesible data structure.~~
- Add 'Show' command to show table's column names and their types.
- Add 'Sample' and 'Distinct' commands for use on specific columns.
- Further seperate out processing and display logic from prompt_toolkit handlers.
- Refactor tests to reduce redundant code. (e.g. use SetUp().)
- Explore using templating library?

Larger features that are planned include:

- Add interactive row viewer.
- Add mechanism for configuring and applying transformations.
- Add mechanism for saving configurations for later application.
- Add ablity to tail log file in application window.

