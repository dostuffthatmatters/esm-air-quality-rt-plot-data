# Real-Time Data Feed from Python to Firebase RT DB

## Prepare Environment & Dependencies

Dependency management with poetry: https://python-poetry.org/docs/#installation

1. Inside your desired python environment (`^3.9`) run:

    ```bash
    pip install poetry  # install the poetry package manager
    poetry install      # use poetry to install dependencies
    ```

2. Place the `.env` file in the projects root directory (same level as `run.py`). The `.env` file should look like this:

    ```bash
    SUPABASE_URL='...'
    SUPABASE_SECRET='...'
    ```

3. Run scripts only from `run.py` with:

    ```bash
    python run.py
    ```
