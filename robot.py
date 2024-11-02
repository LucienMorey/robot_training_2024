import magicbot
import wpilib
from components.intake import IntakeComponent


class TrainingBot(magicbot.MagicRobot):
    intake_component: IntakeComponent

    def createObjects(self) -> None:
        self.xbox_controller = wpilib.XboxController(0)

    def teleopInit(self) -> None:
        pass

    def teleopPeriodic(self):
        if self.xbox_controller.getAButton():
            self.intake_component.deploy()
        if self.xbox_controller.getYButton():
            self.intake_component.retract()


if __name__ == "__main__":
    wpilib.run(TrainingBot)
