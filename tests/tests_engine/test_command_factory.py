import pytest
from engine.game.commands.command_factory import CommandFactory
from engine.game.entities.resource_type import ResourceType


def test_create_roll_dice():
    cmd = CommandFactory.create("roll_dice")
    from engine.game.commands.roll_dice import RollDiceCommand

    assert isinstance(cmd, RollDiceCommand)


def test_create_place_road():
    cmd = CommandFactory.create("place_road", a=(0, 0), b=(1, 1))
    from engine.game.commands.place_road import PlaceRoadCommand

    assert isinstance(cmd, PlaceRoadCommand)
    assert cmd.a == (0, 0) and cmd.b == (1, 1)


def test_create_end_turn():
    dummy_game = object()
    cmd = CommandFactory.create("end_turn", game=dummy_game)
    from engine.game.commands.end_turn import EndTurnCommand

    assert isinstance(cmd, EndTurnCommand)
    assert hasattr(cmd, "game")


def test_create_trade_with_bank():
    cmd = CommandFactory.create("trade_with_bank", give="wood", receive="brick", rate=4)
    from engine.game.commands.trade_with_bank import TradeWithBankCommand

    assert isinstance(cmd, TradeWithBankCommand)
    assert cmd.give == ResourceType.WOOD
    assert cmd.receive == ResourceType.BRICK
    assert cmd.rate == 4


def test_create_start_and_exit_commands():
    assert CommandFactory.create("start_trade_with_bank")
    assert CommandFactory.create("exit_trade_with_bank")
    assert CommandFactory.create("start_place_settlement")
    assert CommandFactory.create("exit_place_settlement")
    assert CommandFactory.create("start_place_road")
    assert CommandFactory.create("exit_place_road")


def test_create_place_settlement():
    cmd = CommandFactory.create("place_settlement", position=(2, 3))
    from engine.game.commands.place_settlement import PlaceSettlementCommand

    assert isinstance(cmd, PlaceSettlementCommand)
    assert cmd.node_position == (2, 3)


def test_create_invalid_command():
    with pytest.raises(ValueError):
        CommandFactory.create("not_a_command")
