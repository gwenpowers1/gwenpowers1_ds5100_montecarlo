import pandas as pd
import numpy as np
from itertools import combinations_with_replacement, product

class Die:
    '''creates a Die with N sides and W weight that can be rolled to select a face, each of which has a unique symbol that is alphabetic or numeric. W defaults to 1.0 but can be changed after the Die is created. '''
    
    def __init__(self, symbols):
        '''
        Takes a list of symbols as an argument and internally initializes the weights to 1.0 for each symbol.
        Saves both symbols and weights in a private data frame with symbols in the index.
        
        :param symbols: List of symbols for the die sides.
        '''
        if not isinstance(symbols, list):
            raise TypeError("Input must be a list of symbols")
        
        if len(symbols) != len(set(symbols)):
            raise ValueError("Symbols must be unique")
        
        if all(isinstance(s, str) and (s.isnumeric() or s.isalpha()) for s in symbols):
            self.symbols = symbols
        else:
            raise ValueError("Symbols must be all alphabetic or all numeric")
        
        self.weights = np.ones(len(symbols))  # Initializing weights to 1.0 for each symbol
        self._data_frame = pd.DataFrame({"Weights": self.weights}, index=self.symbols)
    
    def change_weight(self, symbol, new_weight):
        '''
        A method to change the weight of a single side.
        
        Takes two arguments: the symbol to be changed and the new weight.
        
        :param symbol: The symbol to be changed.
        :param new_weight: The new weight to be assigned.
        '''
        if symbol not in self.symbols:
            raise IndexError("Invalid symbol")
        
        if not isinstance(new_weight, (int, float)):
            raise TypeError("Weight must be numeric")
        
        self.weights[self.symbols.index(symbol)] = new_weight
        self._data_frame.loc[symbol, "Weights"] = new_weight
    
    def roll_die(self, x=1):
        '''
        Rolls the die x times, x defaults to 1, while applying its N and W attributes, returns a list of outcomes but does not store these internally.
        
        :param x: Number of times to roll the die.
        :return: List of outcomes from rolling the die x times.
        '''
        outcomes = np.random.choice(self.symbols, size=x, p=self.weights / np.sum(self.weights))
        return outcomes.tolist()
    
    def current_die(self):
        '''
        Returns a copy of the private die data frame.
        '''
        return self._data_frame.copy()


    
    
class Game:
    '''Creates a Game consisting of inputing one or more Die objects (dice), with the same number of sides and associated faces, but possibly different weights. This class rolls all of the Die in a Game a given number of times and only keeps the most recent play.'''
    
    def __init__(self, dice_list):
        '''
        Takes a list of instantiated similar Die.
        
        :param dice_list: List of Die objects.
        '''
        self.dice = dice_list
        self.play_data = pd.DataFrame()
    
    def play(self, x):
        '''
        Takes an integer value of how many times the Die should be rolled and save the result to a private, wide dataframe.
        
        :param x: Number of times to roll the dice.
        '''
        play_results = {}
        
        for roll_num in range(1, x+1):
            roll_outcomes = {}
            for die_idx, die in enumerate(self.dice):
                outcome = die.roll_die(1)[0]
                roll_outcomes[f"Die_{die_idx}"] = outcome
            
            play_results[roll_num] = roll_outcomes
        
        self.play_data = pd.DataFrame.from_dict(play_results, orient='index')
    
    
    def play_results(self, df_width='wide'):
        '''
        Returns results of the most recent play, takes parameter to determine whether this should be a wide or narrow dataframe (defaults to wide), and raises a ValueError if invalid option for df_width (not narrow or wide) is given.
    
        :param df_width: Option to return the data frame in 'narrow' or 'wide' form (defaults to 'wide').
        :return: Copy of the private play data frame.
        '''
        if df_width == 'wide':
            return self.play_data.copy()
        elif df_width == 'narrow':
            narrow_data = []
            for roll_num, outcomes in self.play_data.iterrows():
                for die_num, outcome in outcomes.items():
                    narrow_data.append([roll_num, f"Die_{die_num}", outcome])
            narrow_df = pd.DataFrame(narrow_data, columns=['Roll', 'Die', 'Outcome'])
            narrow_df.set_index(['Roll', 'Die'], inplace=True)  # Set index with a list of column names as strings
            return narrow_df
        else:
            raise ValueError("Invalid option for df_width. Use 'narrow' or 'wide'.")



    
     
class Analyzer:   
    '''Creates an Analyzer which takes the results of a single game and computes various statistical properties about it.'''

    def __init__(self, game):
        '''
        Takes a Game object, throws an error if input is not a Game.
        
        :param game: Game object.
        '''
        if not isinstance(game, Game):
            raise ValueError("Input must be a Game object.")
        self.game = game
        self.results = game.play_data
    
    def jackpot(self):
        '''
        Computes and returns as an integer how many times the game resulted in a jackpot, when all faces are the same.
        
        :return: Number of jackpots.
        '''
        jackpot_count = 0
        for _, outcomes in self.results.iterrows():
            if all(outcome == outcomes[0] for outcome in outcomes):
                jackpot_count += 1
        return jackpot_count
    def face_counts_per_roll(self, face):
        '''
        Computes how many times a given face is rolled in each event and returns a dataframe of results.
    
        :param face: Face value to compute counts for.
        :return: Data frame with counts for the given face value.
        '''
        face_counts = {}
        for roll_num, outcomes in self.results.iterrows():
            face_count = outcomes.tolist().count(face)
            face_counts[roll_num] = face_count
    
        return pd.DataFrame({f'Face_{face}_Count': face_counts})
     
    
    def combo_count(self):
        '''
        Computes the distinct combinations of faces rolled and their counts and returns a dataframe of results. These are order-independent and may contain repetitions.
        
        :return: Data frame with distinct combinations and their counts.
        '''
        combo_counts = {}
        for _, outcomes in self.results.iterrows():
            unique_combinations = set(combinations_with_replacement(outcomes, len(self.game.dice)))
            for combo in unique_combinations:
                combo_counts.setdefault(combo, 0)
                combo_counts[combo] += 1
        
        combo_df = pd.DataFrame(combo_counts.items(), columns=['Combo', 'Count'])
        combo_df['Combo'] = combo_df['Combo'].apply(lambda x: tuple(sorted(x)))
        combo_df = combo_df.groupby('Combo')['Count'].sum().reset_index()
        
        return combo_df.set_index('Combo')
    
    def permutation_count(self):
        '''
        Computes the distinct permutations of faces rolled and their counts and returns a dataframe of results. These are order-dependent and may contain repetitions
        
        :return: Data frame with distinct permutations and their counts.
        '''
        perm_counts = {}
        for _, outcomes in self.results.iterrows():
            unique_permutations = set(product(outcomes, repeat=len(self.game.dice)))
            for perm in unique_permutations:
                perm_counts.setdefault(perm, 0)
                perm_counts[perm] += 1
        
        perm_df = pd.DataFrame(perm_counts.items(), columns=['Permutation', 'Count'])
        perm_df['Permutation'] = perm_df['Permutation'].apply(lambda x: tuple(x))
        perm_df = perm_df.groupby('Permutation')['Count'].sum().reset_index()
        
        perm_df['Permutation'] = pd.MultiIndex.from_tuples(perm_df['Permutation'])
        perm_df.set_index('Permutation', inplace=True)
        
        return perm_df




