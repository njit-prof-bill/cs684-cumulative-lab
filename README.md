# cs684-cumulative-lab

Repo for ongoing in-class labs

This course uses a cumulative artifact that evolves over the semester. At times,
the instructor will publish a fresh baseline version so everyone starts from the
same code state during in-class work.

## Getting Started

This lab uses python and pytest. It is recommended to setup a python virtual environment and install pytest into it. You can do this by running the `setup.sh` bash command like this:

```
bash setup.sh
```

Alternatively you can run individual commands like this:

```
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install pytest
pytest -q
```

This assumes you are running linux, MacOS, or WSL. If you are running Windows, you can edit the bash script to uncomment the Powershell commands, then comment out the Linux commands. _Note_ this has not been tested with Windows and Powershell.

---

Where is the spec?

The informal requirement/specification remains in requirement.md (from last week).
We are not rewriting the requirement this week.

This week’s focus is test data selection: identifying which regions of the input
space are exercised by the current tests and adding a small number of strategically
chosen tests that reduce risk (boundaries, invalid inputs, messy identifiers, etc.).

You can run the ledger code with:

```
python ledger.py
```

You can run your tests with:

```
pytest -v
```
