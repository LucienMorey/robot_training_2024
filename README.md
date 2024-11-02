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

### Begin Filling in Intake.py

- Copy constants into the profile
  - Mostly just math
  - IDs are things we have set ahead of time for this exercise
- Create motor objects
  - Note that there are 2 motors on the robot L & R
  - Both use a CANSparkMax
  - These are brushless motors and we must indicate this
  - Note the inversion for one motor and not the other we know what needs to happen after the gear train because we have used this
- Create Encoder object
  - Built directly into the motor for handling Brushless things
  - Set the appropriate unit conversions from Rotations and RPS to Rad/s
  - Initialise position to retracted position
- Create PID and Feed forward controllers
  - P - effort proportional to error so intuitively it is large when we are far from the setpoint
  - I - effort that builds over time by considering all past errors. This is used to deal with steady state error which can be thought of as constant error offset because we are close to the setpoint and dont have the strength to overpower it with just proportional effort
  - D - effort that is proportional to the rate of change of the system and is often used to damp things out to avoid overshoot
  - Feed forward - predictive effort based on how you understand the system to minimise lag and reject disturbances
  - magic numbers from our time at competition
  - We have two different controllers for deploy and retract because the dynamics of the system are different when we are assisted by gravity and fighting against it
- Create deploy and retract functions
  - we are using a trapezoidal profile for tracking here, position and velocity paramaterised by time
  - We need to make sure we only record the first time point of the command to calculate and track a single profile in this case
- Fill in execute method
  - calculate where we should be in the trapezoidal profile
  - calculate determine if we should use feed forward or not
  - dispatch desired setpoint and control information

### Add New Intake Component to Robot.py

- Import new component
- We can instantiate an instance of the object by type hinting a decleration in our robot class
  - This is not how python normally does things! This is a special part of magicbot in our usecase
- Add if statements in the teleop period for whether to deploy or retract
