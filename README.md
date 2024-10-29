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
- Create empty robot class scaffold
  - Note that we are importing libraries for this
  - Mention this is a subclass of magicrobot so it inherits a special set of methods used to standardise the setup of robots
- Create objects function to describe all of the things that will be present in a robot
  - Create controller as example
  - Point of dependency injection for other classes
- Mention Different modes of robot (disabled, test, telep and auto)
  - One init function called once at the beginning to set things up and guarantee state
  - Periodic method run every 20ms (50Hz) to realise desired robot behaviour safely
    - this is called ticking - most robot systems are not event based like someone would expect

### Create Intake.py Scaffold

- class file
- requires at the very least an init and execute method
  - init is used for object creation and ensuring the correct default state of a robot component also the entrypoint for dependency injection
  - execute method is the main control point for a robot component where the current intended state of any actuators is dispatched and the current state of any sensors is read
  - this will create a fully self contained and autonomous component but this is an unlikely use case because we will always need to interact with these things
- other helper methods to set state of a component so that it can be dispatched synchronously during the execute step
- Very important to only be setting state in helper methods instead of dispatching calls directly or you start breaking down the intended layers of abstraction and use case for controllers and autonomous modes
- in this case we will have an init method, execute method and drive method
  - init will instantiate motor, sensors and PID profiles
  - deploy will be the entry point for setting the deployed position setpoint for dispatch in execute
  - retract will be the entry point for setting the retracted position setpoint for dispatch in execute
  - execute will compute the appropriate PID things and send voltage commands to the motors
