# cs684-cumulative-lab

Repo for ongoing in-class labs

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

You will find the requirement for the ledger in the file `requirement.md`.

You can run the ledger code with:

```
python ledger.py
```

You can run your tests with:

```
pytest -v
```
