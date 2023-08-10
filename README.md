
# Monte Carlo Simulator

## Metadata

- **Author:** Gwen Powers
- **Project:** Monte Carlo Simulator

## Synopsis
### Install
pip install /Users/gwenpowers/Desktop/ds5100_montecarlo/dist/ds5100_montecarlo-1.0.0.tar.gz

#### 1. Create Dice

from montecarlo import Die

###### Define symbols for the die
symbols = ['1', '2', '3', '4', '5', '6']

######  Create a new die
die = Die(symbols)

######  Change weight of a symbol
die.change_weight('1', 2.0)

######  Roll the die
outcomes = die.roll_die(10)

######  Get current die data
current_data_frame = die.current_die()

#### 2. Play a Game

from montecarlo import Die, Game

######  Create dice
symbols = ['1', '2', '3', '4', '5', '6']
die1 = Die(symbols)
die2 = Die(symbols)

######  Create a game with the dice
game = Game([die1, die2])

######  Play the game and get results
game.play(10)

######  Get play results in wide format
play_results_wide = game.play_results('wide')

######  Get play results in narrow format
play_results_narrow = game.play_results('narrow')


#### 3. Analyze a Game
from montecarlo import Die, Game, Analyzer

######  Create dice and a game
symbols = ['1', '2', '3', '4', '5', '6']
die1 = Die(symbols)
die2 = Die(symbols)
game = Game([die1, die2])

######  Play the game
game.play(10)

######  Analyze game results
analyzer = Analyzer(game)
jackpot_count = analyzer.jackpot()
face_counts_df = analyzer.face_counts_per_roll('1')
combo_counts_df = analyzer.combo_count()
perm_counts_df = analyzer.permutation_count()


## API Description

### Die

A class for simulating dice.

#### Methods:

- `__init__(symbols: List[str])`: Initialize a Die instance with a list of symbols.
- `change_weight(symbol: str, new_weight: float)`: Change the weight of a specific symbol.
- `roll_die(x: int = 1) -> List[str]`: Roll the die x times and return outcomes.
- `current_die() -> pd.DataFrame`: Return a copy of the die's data frame.

### Game

A class for simulating games.

#### Methods:

- `__init__(dice_list: List[Die])`: Initialize a Game instance with a list of dice.
- `play(x: int)`: Roll the dice x times and save the results.
- `play_results(df_width: str = 'wide') -> pd.DataFrame`: Return the game results in wide or narrow format.

### Analyzer

A class for analyzing game results.

#### Methods:

- `__init__(game: Game)`: Initialize an Analyzer instance with a Game object.
- `jackpot() -> int`: Compute the number of jackpots in the game.
- `face_counts_per_roll(face: str) -> pd.DataFrame`: Compute the face counts for a given face value.
- `combo_count() -> pd.DataFrame`: Compute distinct combinations of faces rolled and their counts.
- `permutation_count() -> pd.DataFrame`: Compute distinct permutations of faces rolled and their counts.
