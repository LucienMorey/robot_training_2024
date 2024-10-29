import magicbot
import wpilib


class TrainingBot(magicbot.MagicRobot):

    def createObjects(self) -> None:
        self.xbox_controller = wpilib.XboxController(0)

    def teleopInit(self) -> None:
        pass

    def teleopPeriodic(self):
        pass


if __name__ == "__main__":
    wpilib.run(TrainingBot)
