import math
import time
from wpimath.trajectory import TrapezoidProfile
from wpimath.controller import ArmFeedforward

from rev import CANSparkMax


class IntakeComponent:

    DEPLOY_GEAR_RATIO = (1 / 5) * (1 / 3) * (24 / 72)
    MOTOR_REV_TO_SHAFT_RADIANS = DEPLOY_GEAR_RATIO * math.tau
    MOTOR_RPM_TO_SHAFT_RAD_PER_SEC = MOTOR_REV_TO_SHAFT_RADIANS / 60

    SHAFT_REV_RETRACT_HARD_LIMIT = 1.778579
    SHAFT_REV_DEPLOY_HARD_LIMIT = 0.0
    SHAFT_REV_HOVER_POINT = SHAFT_REV_DEPLOY_HARD_LIMIT + math.radians(15)

    RETRACTED_STATE = TrapezoidProfile.State(SHAFT_REV_RETRACT_HARD_LIMIT, 0.0)
    DEPLOYED_STATE = TrapezoidProfile.State(SHAFT_REV_DEPLOY_HARD_LIMIT, 0.0)

    DEPLOY_L_ID = 4
    DEPLOY_R_ID = 5

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

        # Initialise Motors
        self.deploy_motor_l = CANSparkMax(
            self.DEPLOY_L_ID, CANSparkMax.MotorType.kBrushless
        )
        self.deploy_motor_r = CANSparkMax(
            self.DEPLOY_R_ID, CANSparkMax.MotorType.kBrushless
        )
        self.deploy_motor_l.setIdleMode(CANSparkMax.IdleMode.kBrake)
        self.deploy_motor_r.setIdleMode(CANSparkMax.IdleMode.kBrake)

        self.deploy_motor_l.setInverted(False)
        self.deploy_motor_r.follow(self.deploy_motor_l, True)
        self.target_deployment_state = self.RETRACTED_STATE

        # Initialise Encoder
        self.deploy_encoder = self.deploy_motor_l.getEncoder()
        self.deploy_encoder.setVelocityConversionFactor(
            self.MOTOR_RPM_TO_SHAFT_RAD_PER_SEC
        )
        self.deploy_encoder.setPositionConversionFactor(self.MOTOR_REV_TO_SHAFT_RADIANS)
        self.deploy_encoder.setPosition(self.target_deployment_state.position)

        self.last_setpoint_update_time = time.monotonic()

        # Initialise PID things
        arm_constraints = TrapezoidProfile.Constraints(
            maxVelocity=6.0, maxAcceleration=math.pi
        )

        self.arm_profile = TrapezoidProfile(arm_constraints)
        self.feed_forward_calculator = ArmFeedforward(kS=0.0, kG=0.16, kV=1.17, kA=0.02)
        self.pid_controller = self.deploy_motor_l.getPIDController()

        # Retract PID Controller
        self.retract_pid_slot = 0
        self.pid_controller.setFF(
            1 / (5700.0 * self.MOTOR_RPM_TO_SHAFT_RAD_PER_SEC), self.retract_pid_slot
        )
        self.pid_controller.setP(0.2, self.retract_pid_slot)
        self.pid_controller.setI(0, self.retract_pid_slot)
        self.pid_controller.setD(0.4, self.retract_pid_slot)
        self.pid_controller.setOutputRange(-1, 1, self.retract_pid_slot)

        # Deploy PID Controller
        self.deploy_pid_slot = 1
        self.pid_controller.setFF(
            1 / (5700.0 * self.MOTOR_RPM_TO_SHAFT_RAD_PER_SEC), self.deploy_pid_slot
        )
        self.pid_controller.setP(0.6, self.deploy_pid_slot)
        self.pid_controller.setI(0, self.deploy_pid_slot)
        self.pid_controller.setD(0.6, self.deploy_pid_slot)
        self.pid_controller.setOutputRange(-1, 1, self.deploy_pid_slot)

        self.pid_slot = self.retract_pid_slot

    def deploy(self) -> None:
        """set the desired position for the intake motor to be deployed"""
        if self.target_deployment_state is not self.DEPLOYED_STATE:
            self.last_setpoint_update_time = time.monotonic()
            self.target_deployment_state = self.DEPLOYED_STATE
            self.pid_slot = self.deploy_pid_slot

    def retract(self) -> None:
        """set the desired position for the intake motor to be retracted"""
        if self.target_deployment_state is not self.RETRACTED_STATE:
            self.last_setpoint_update_time = time.monotonic()
            self.target_deployment_state = self.RETRACTED_STATE
            self.pid_slot = self.retract_pid_slot

    def execute(self) -> None:
        """
        Class update method
        this is scheduled to run every 20 ms as per robotpy specification
        This will be used to ensure
            - the right setpoints are being tracked
            - check for erroneous state to fix it
            - recalculate voltage applied to motors
        """
        desired_state = self.arm_profile.calculate(
            time.monotonic() - self.last_setpoint_update_time,
            TrapezoidProfile.State(
                self.deploy_encoder.getPosition(), self.deploy_encoder.getVelocity()
            ),
            self.target_deployment_state,
        )

        if self.target_deployment_state is self.RETRACTED_STATE:
            ff = self.feed_forward_calculator.calculate(
                desired_state.position, desired_state.velocity
            )
        else:
            ff = 0.0

        self.pid_controller.setReference(
            desired_state.position,
            CANSparkMax.ControlType.kPosition,
            pidSlot=self.pid_slot,
            arbFeedforward=ff,
        )
