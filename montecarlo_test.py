import unittest
import pandas as pd
import numpy as np
from montecarlo import Die, Game, Analyzer
from itertools import combinations_with_replacement, product

class TestDieMethods(unittest.TestCase):

    def test_init(self):
        symbols = ['1', '2', '3', '4', '5', '6']
        die = Die(symbols)
        self.assertEqual(die.symbols, symbols)
        self.assertEqual(die.weights.tolist(), [1.0] * 6)

    def test_change_weight(self):
        symbols = ['1', '2', '3', '4', '5', '6']
        die = Die(symbols)
        die.change_weight('1', 2.0)
        self.assertEqual(die.weights.tolist(), [2.0, 1.0, 1.0, 1.0, 1.0, 1.0])

    def test_roll_die(self):
        symbols = ['1', '2', '3', '4', '5', '6']
        die = Die(symbols)
        outcomes = die.roll_die(100)
        self.assertEqual(len(outcomes), 100)

    
    def test_current_die(self):
        symbols = ['1', '2', '3', '4', '5', '6']
        die = Die(symbols)
        current_data_frame = die.current_die()
        self.assertEqual(current_data_frame.shape[0], 6)
        
class TestGameMethods(unittest.TestCase):

    def test_init(self):
        die1 = Die(['1', '2', '3', '4', '5', '6'])
        die2 = Die(['A', 'B', 'C', 'D', 'E', 'F'])
        game = Game([die1, die2])
        self.assertEqual(len(game.dice), 2)

    def test_play(self):
        die1 = Die(['1', '2', '3', '4', '5', '6'])
        die2 = Die(['A', 'B', 'C', 'D', 'E', 'F'])
        game = Game([die1, die2])
        game.play(10)
        self.assertEqual(game.play_data.shape, (10, 2))
        
    def test_play_results(self):
        die1 = Die(['1', '2', '3', '4', '5', '6'])
        die2 = Die(['A', 'B', 'C', 'D', 'E', 'F'])
        game = Game([die1, die2])
        game.play(10)
        
        play_results_wide = game.play_results('wide')
        play_results_narrow = game.play_results('narrow')
        
        self.assertIsInstance(play_results_wide, pd.DataFrame)
        self.assertIsInstance(play_results_narrow, pd.DataFrame)
        self.assertEqual(play_results_wide.shape, (10, 2))
        
        self.assertEqual(play_results_narrow.index.names, ['Roll', 'Die'])



class TestAnalyzerMethods(unittest.TestCase):

    def test_init(self):
        die1 = Die(['1', '2', '3', '4', '5', '6'])
        die2 = Die(['A', 'B', 'C', 'D', 'E', 'F'])
        game = Game([die1, die2])
        game.play(10)
        self.analyzer = Analyzer(game)

    def test_jackpot(self):
        self.test_init()  # Call your custom initialization method
        jackpot_count = self.analyzer.jackpot()
        self.assertIsInstance(jackpot_count, int)

    def test_face_counts_per_roll(self):
        self.test_init()  # Call your custom initialization method
        face = '1'
        face_counts_df = self.analyzer.face_counts_per_roll(face)
        self.assertIsInstance(face_counts_df, pd.DataFrame)

    def test_combo_count(self):
        self.test_init()  # Call your custom initialization method
        combo_counts_df = self.analyzer.combo_count()
        self.assertIsInstance(combo_counts_df, pd.DataFrame)

    def test_permutation_count(self):
        self.test_init()  # Call your custom initialization method
        perm_counts_df = self.analyzer.permutation_count()
        self.assertIsInstance(perm_counts_df, pd.DataFrame)
  
        
if __name__ == '__main__':
    unittest.main()
