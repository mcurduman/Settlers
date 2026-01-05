from app.game.commands.command import Command
from app.game.dice import Dice


class RollDiceCommand(Command):
    def execute(self, game, player):
        dice_value = Dice.roll()
        game.handle_dice_roll(dice_value)
        return dice_value
