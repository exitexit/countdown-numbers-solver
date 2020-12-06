# Countdown Numbers Solver

Like my code? [![donate](https://img.shields.io/badge/%24-Buy%20me%20a%20coffee-ef864e.svg)](https://www.buymeacoffee.com/exitexit) or consider donating to my Ether wallet: 0x3c2f57171FBc82D1F54de74f20Ce174ca4874298

A Python function for solving the numbers game problems in the British game show Countdown. The program is written in Python 3.
If you are interested in learning about the game, check out [here](https://en.wikipedia.org/wiki/Countdown_(game_show)#Numbers_round).
Episodes of the game show can be found on YouTube.

## Content

##### countdown_numbers_solver.py
The file contains a set of utilities for exploring the solution space of a given numbers problem and optimizing the output in a human readable format. The code is written mostly in procedural format for ease of comprehension.

## Sample Usage
Example: `numbers = [ 100, 25, 8, 3, 1, 1 ]` and `target = 984`.<br/>
By default, the results were properly de-duplicated to eliminate the trivial variations of the same solutions.
```
>>> import countdown_numbers_solver
>>> countdown_numbers_solver.solve([ 100, 25, 8, 3, 1, 1 ], 984)
( 100 + 25 + 1 - 3 ) x 8
( 100 + 25 - 1 - 1 ) x 8
( 100 + 1 ) x ( 8 + 1 ) + 25 x 3
( ( 100 - 1 ) / 3 + 8 ) x ( 25 - 1 )
Total: 4 solutions.
```
To turn off de-duplication, set `countdown_numbers_solver.OPTIMIZE = 0`.<br/>
For example:
```
>>> countdown_numbers_solver.OPTIMIZE = 0
>>> countdown_numbers_solver.solve([ 100, 25, 8, 3, 1, 1 ], 984)
( 100 + 25 - ( 3 - 1 ) ) x 8
( 100 + 25 - 3 + 1 ) x 8
( 100 + 25 - ( 1 + 1 ) ) x 8
( 100 + 25 + 1 - 3 ) x 8
( 100 + 25 - 1 - 1 ) x 8
( 100 - ( 3 - 1 ) + 25 ) x 8
( 100 - 3 + 25 + 1 ) x 8
( 100 - 3 + 1 + 25 ) x 8
( 100 - ( 1 + 1 ) + 25 ) x 8
( 100 + 1 + 25 - 3 ) x 8
( 100 + 1 ) x ( 8 + 1 ) + 25 x 3
( 100 + 1 - 3 + 25 ) x 8
( 100 - 1 + 25 - 1 ) x 8
( ( 100 - 1 ) / 3 + 8 ) x ( 25 - 1 )
( 100 - 1 - 1 + 25 ) x 8
Total: 15 solutions.
```
