# Countdown Number Solver

Like my code? [![donate](https://img.shields.io/badge/%24-Buy%20me%20a%20coffee-ef864e.svg)](https://www.buymeacoffee.com/exitexit) or consider donating to my Ether wallet: 0x3c2f57171FBc82D1F54de74f20Ce174ca4874298

A Python3 function for solving the numbers problems in the British game show Countdown.
If you are interested in learning about the game, check out [here](https://en.wikipedia.org/wiki/Countdown_(game_show)#Numbers_round).
Episodes of the game show can be found on YouTube.

## Content

##### countdown_number_solver.py
The file contains a set of utilities for exploring the solution space of a given numbers problem and optimizing the output in a human readable format. The code is written mostly in procedural format for ease of comprehension.

## Sample Usage
Example: `numbers = [ 100, 25, 8, 3, 1, 1 ]` and `target = 984`.
```
>>> import countdown_number_solver
>>> countdown_number_solver.solve([ 100, 25, 8, 3, 1, 1 ], 984)
( 100 + 25 + 1 - 3 ) x 8
( 100 + 25 - 1 - 1 ) x 8
( 100 + 1 ) x ( 8 + 1 ) + 25 x 3
( ( 100 - 1 ) / 3 + 8 ) x ( 25 - 1 )
Total: 4 solutions.
```
