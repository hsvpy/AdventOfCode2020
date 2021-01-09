from typing import Deque, DefaultDict, List, Tuple
from collections import defaultdict, deque
from copy import deepcopy
from enum import Enum


class GameState(Enum):
    RUNNING = 1
    COMPLETE = 2
    INF = 3


class Game(object):
    next_id = 1

    def __init__(self):
        self.decks = defaultdict(deque)
        self.hashes_seen = []
        self.state = GameState.RUNNING
        self.id = type(self).next_id
        type(self).increment_next_id()

    @classmethod
    def increment_next_id(cls):
        cls.next_id += 1

    def get_score(self, winner=None) -> int:
        winning_deck = None
        if winner is None:
            for deck in self.decks.values():
                if len(deck):
                    winning_deck = deck
        else:
            winning_deck = self.decks[winner].values()
        winning_deck.reverse()
        return sum(list(map(lambda t: (t[0] + 1) * t[1], enumerate(winning_deck))))

    def start_game(self, recursive: bool) -> int:
        the_round = 1
        while True:
            winner = self.play_round(recursive)
            the_round += 1
            print(f"Game {self.id} / Round: {the_round} won by Player {winner + 1}")
            if self.state != GameState.RUNNING:
                break
        if self.state == GameState.INF:
            winner = 0
        print(f"Score of game: {self.get_score()}")
        return winner

    def play_round(self, recurse: bool) -> int:
        current_cards = deque([x.popleft() for x in self.decks.values()])
        if not self.infinite_game_detection():
            print(f"Player 1's deck: {str(list(self.decks[0]))}")
            print(f"Player 2's deck: {str(list(self.decks[1]))}")
            print(f"Player 1 plays: {current_cards[0]}")
            print(f"Player 2 plays: {current_cards[1]}")
            winner = current_cards.index(max(current_cards))
            if recurse:
                able_to_recurse = [current_cards[k] <= len(v) for k, v in self.decks.items()]
                if all(able_to_recurse):
                    recursive_game = Game()
                    recursive_game.decks = deepcopy(self.decks)
                    [[v.pop()] for k, v in recursive_game.decks.items() for _ in range(len(v) - current_cards[k])]
                    winner = recursive_game.start_game(recurse)
            if winner:
                current_cards.rotate(1)
            print(f"Player {winner+1} wins!")
            self.decks[winner].extend(current_cards)
            done = [len(x) == 0 for x in self.decks.values()]
            self.state = GameState.COMPLETE if any(done) else GameState.RUNNING
        else:
            winner = 0
        return winner

    def infinite_game_detection(self) -> bool:
        def get_hash() -> str:
            the_hash = ""
            for _, player_deck in self.decks.items():
                for card in player_deck:
                    the_hash += f"{str(card)},"
                the_hash += '|'
            return the_hash

        current_hash = get_hash()
        if current_hash in self.hashes_seen:
            print(f"Infinite game detected with hash of {current_hash}!")
            self.state = GameState.INF
            return True
        else:
            self.hashes_seen.append(current_hash)
            return False


def parse_input(filename: str) -> Game:
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line != '\n']

    player = 0
    game = Game()
    for line in lines:
        if 'Player' in line:
            player += 1
        else:
            game.decks[player-1].append(int(line))
    return game





part1 = parse_input('input.txt')
print(f"Part 1: {part1.start_game(False)}")
# memoization would speed this up considerably
part2 = parse_input('input.txt')
print(f"Part 2: {part2.start_game(True)}")

