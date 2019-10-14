from .sample_player import Player, PlayerDirection, PlayerAction


def gm_generator(size):
    return [[None for _ in range(size)] for _ in range(size)]


def get_player(direction: PlayerDirection = PlayerDirection.UP):
    p = Player()
    p.direction = direction
    return p


class TestSamplePlayer:

    def test_next_step_regular(self):
        gm = gm_generator(3)
        assert get_player(PlayerDirection.UP).next_step(gm, (1, 1)) == PlayerAction.STRAIGHT.value

    def test_next_step_corner(self):
        gm = gm_generator(3)

        assert get_player(PlayerDirection.UP).next_step(gm, (0, 0)) == PlayerAction.RIGHT.value
        assert get_player(PlayerDirection.LEFT).next_step(gm, (0, 0)) == PlayerAction.LEFT.value

        assert get_player(PlayerDirection.UP).next_step(gm, (0, 2)) == PlayerAction.LEFT.value
        assert get_player(PlayerDirection.RIGHT).next_step(gm, (0, 2)) == PlayerAction.RIGHT.value

        assert get_player(PlayerDirection.DOWN).next_step(gm, (2, 2)) == PlayerAction.RIGHT.value
        assert get_player(PlayerDirection.RIGHT).next_step(gm, (2, 2)) == PlayerAction.LEFT.value

        assert get_player(PlayerDirection.DOWN).next_step(gm, (2, 0)) == PlayerAction.LEFT.value
        assert get_player(PlayerDirection.LEFT).next_step(gm, (2, 0)) == PlayerAction.RIGHT.value

    def test_next_step_edge(self):
        gm = gm_generator(3)

        assert get_player(PlayerDirection.UP).next_step(gm, (0, 1)) == (
                PlayerAction.RIGHT.value or PlayerAction.LEFT.value)

        assert get_player(PlayerDirection.DOWN).next_step(gm, (2, 1)) == (
                PlayerAction.RIGHT.value or PlayerAction.LEFT.value)

        assert get_player(PlayerDirection.RIGHT).next_step(gm, (1, 2)) == (
            PlayerAction.RIGHT.value or PlayerAction.LEFT.value)

        assert get_player(PlayerDirection.LEFT).next_step(gm, (1, 0)) == (
            PlayerAction.RIGHT.value or PlayerAction.LEFT.value)
