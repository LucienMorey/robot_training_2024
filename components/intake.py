class IntakeComponent:
    def __init__(self) -> None:
        """
        Runs on robot initialisation
        Sets up info relevant hardware for running the component
            - encoder
            - motor
        sets up any persisting data for the thing
            - deployed state
            - pid profiles
        """
        pass

    def deploy(self) -> None:
        """set the desired position for the intake motor to be deployed"""
        pass

    def retract(self) -> None:
        """set the desired position for the intake motor to be retracted"""
        pass

    def execute(self) -> None:
        """
        Class update method
        this is scheduled to run every 20 ms as per robotpy specification
        This will be used to ensure
            - the right setpoints are being tracked
            - check for erroneous state to fix it
            - recalculate voltage applied to motors
        """
        pass
