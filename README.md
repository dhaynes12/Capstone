# Capstone
Capstone chess AI project

# Goal
Create a chess program that displays a chess board and allows for interaction through clicking the chess pieces. Human vs. human, human vs. ai, and ai vs. ai will be possible. The ai will be reasonably smart, and the user can decide how many moves the ai could look ahead.

# AI Types
0 - Basic. Considers total piece value and maximizing possible moves
1 - Hash. Like 0, but stores nextMoves in dictionary
2 - Basic Sort. Like 0, but sorts nextMoves by highest weight
3 - NegaMax
4 - Hash Sort. Unfinished.
5 - NegaMax Position. Like NegaMax, but uses positional values
6 - Basic Sort Position. Like Basic Sort, but uses positional values
7 - Hash Sort Position. Like Hash Sort, but uses positional values. Unfinished
Other - Moves randomly selected.

# Attribution
All chess symbols by Cburnett is licensed under [CC BY-SA3.0](https://creativecommons.org/licenses/by-sa/3.0/deed.en). The symbols used are:
* [Chess klt45.svg](https://en.wikipedia.org/wiki/File:Chess_klt45.svg)
* [Chess qlt45.svg](https://en.wikipedia.org/wiki/File:Chess_qlt45.svg)
* [Chess rlt45.svg](https://en.wikipedia.org/wiki/File:Chess_rlt45.svg)
* [Chess blt45.svg](https://en.wikipedia.org/wiki/File:Chess_blt45.svg)
* [Chess nlt45.svg](https://en.wikipedia.org/wiki/File:Chess_nlt45.svg)
* [Chess plt45.svg](https://en.wikipedia.org/wiki/File:Chess_plt45.svg)
* [Chess kdt45.svg](https://en.wikipedia.org/wiki/File:Chess_kdt45.svg)
* [Chess qdt45.svg](https://en.wikipedia.org/wiki/File:Chess_qdt45.svg)
* [Chess rdt45.svg](https://en.wikipedia.org/wiki/File:Chess_rdt45.svg)
* [Chess bdt45.svg](https://en.wikipedia.org/wiki/File:Chess_bdt45.svg)
* [Chess ndt45.svg](https://en.wikipedia.org/wiki/File:Chess_ndt45.svg)
* [Chess pdt45.svg](https://en.wikipedia.org/wiki/File:Chess_pdt45.svg)

# Citations
https://www.quora.com/What-are-some-heuristics-for-quickly-evaluating-chess-positions

# Times
## vs Random Black
### 0, Depth 3
Lowest think time: 0.99 seconds
Highest think time: 7.37 seconds
Average think time: 3.35 seconds

### 1, Depth 3
Lowest think time: 0.55 seconds
Highest think time: 16.80 seconds
Average think time: 4.06 seconds

### 2, Depth 3
Lowest think time: 0.54 seconds
Highest think time: 4.04 seconds
Average think time: 1.33 seconds

### 2, Depth 4
Lowest think time: 2.71 seconds
Highest think time: 60.50 seconds
Average think time: 23.98 seconds

### 3, Depth 4
Lowest think time: 1.99 seconds
Highest think time: 73.37 seconds
Average think time: 14.63 seconds
Stalemated

### 5, Depth 4
Lowest think time: 9.95 seconds
Highest think time: 97.61 seconds
Average think time: 39.72 seconds

### 6, Depth 3
Lowest think time: 2.86 seconds
Highest think time: 56.58 seconds
Average think time: 18.14 seconds

# AI vs AI
### 2 vs 6
2 White, 6 Black:
* Stalemate in 66 turns, 2 has piece advantage
* White Piece Val: 38
* Black Piece Val: 33.5
6 White, 2 Black:
* Stalemate in 61 turns, 1 has piece advantage
* White Piece Val: 28
* Black Piece Val: 27.5