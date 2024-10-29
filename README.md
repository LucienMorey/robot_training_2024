# robot_training_2024
Presentation for software masterclass at the drop bears 2024

## UV

```bash
uv sync
```

```bash
uv run python -m ensurepip
```

```bash
uv run robotpy sync --no-install
```

## Talking Points

### Create Repo

- Go over Github as a thing again quickly
- Create repo for drop bears account
  - Naming convention of pygamename
  - We will call this pytrainingday2024
- Make sure to create with gitignore and readme to make cloning possible

### Repository Configure

- Create Pre-commit file
  - Copy straight from repo
  - Explain the importance of what it does in enforcing standardisation across the repo
  - Run install to trigger the hooks from now on
  - Commit
- Create PDM elements
  - pyproject.toml can be copied from an older repo as a starting point to save time on config
  - Run the appropriate download and install commands to get the lock file generated
  - Commit
- Create empty robotpy files and directories
  - robot.py in root of repository
  - components folder with `__init__.py`
  - controllers folder with `__init__.py`

### Fill in Robot.py scaffold

- Create empty main for execution of robot