# from an empty directory
python -m venv .venv

# mac/linux
source .venv/bin/activate

# windows (powershell)
# .\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install pytest

# run tests
pytest -q