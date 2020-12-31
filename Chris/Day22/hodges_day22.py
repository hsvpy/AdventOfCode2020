from typing import Deque, DefaultDict
from collections import defaultdict, deque

PlayerDecks = DefaultDict[int, Deque[int]]


def parse_input(filename: str) -> PlayerDecks:
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line != '\n']
    player = 0
    all_players = defaultdict(deque)
    for line in lines:
        if 'Player' in line:
            player += 1
        else:
            all_players[player-1].append(int(line))
    return all_players


def play_round(decks: PlayerDecks) -> bool:
    current_cards = deque([x.popleft() for x in decks.values()])
    winner = current_cards.index(max(current_cards))
    if winner:
        current_cards.rotate(1)
    decks[winner].extend(current_cards)
    done = [len(x) == 0 for x in decks.values()]
    return not any(done)


def get_score(decks: PlayerDecks) -> int:
    for deck in decks.values():
        if len(deck):
            deck.reverse()
            return sum(list(map(lambda t: (t[0]+1)*t[1], enumerate(deck))))


players_decks: PlayerDecks = parse_input('input.txt')
the_round = 1
while play_round(players_decks):
    print(f"Round: {the_round}")
    the_round += 1

print(f"Part 1: {get_score(players_decks)}")
