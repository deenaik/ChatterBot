"""
Test ChatterBot's statement comparison algorithms.
"""

from unittest import TestCase
from chatterbot.conversation import Statement
from chatterbot import comparisons


class LevenshteinDistanceTestCase(TestCase):

    def test_levenshtein_distance_statement_false(self):
        """
        Falsy values should match by zero.
        """
        statement = Statement(text='')
        other_statement = Statement(text='Hello')

        value = comparisons.levenshtein_distance(statement, other_statement)

        self.assertEqual(value, 0)

    def test_levenshtein_distance_other_statement_false(self):
        """
        Falsy values should match by zero.
        """
        statement = Statement(text='Hello')
        other_statement = Statement(text='')

        value = comparisons.levenshtein_distance(statement, other_statement)

        self.assertEqual(value, 0)

    def test_levenshtein_distance_statement_integer(self):
        """
        Test that an exception is not raised if a statement is initialized
        with an integer value as its text attribute.
        """
        statement = Statement(text=2)
        other_statement = Statement(text='Hello')

        value = comparisons.levenshtein_distance(statement, other_statement)

        self.assertEqual(value, 0)

    def test_exact_match_different_capitalization(self):
        """
        Test that text capitalization is ignored.
        """
        statement = Statement(text='Hi HoW ArE yOu?')
        other_statement = Statement(text='hI hOw are YoU?')

        value = comparisons.levenshtein_distance(statement, other_statement)

        self.assertEqual(value, 1)


class SynsetDistanceTestCase(TestCase):

    def test_get_initialization_functions(self):
        """
        Test that the initialization functions are returned.
        """
        functions = comparisons.synset_distance.get_initialization_functions()

        self.assertIn('initialize_nltk_wordnet', functions)

    def test_exact_match_different_capitalization(self):
        """
        Test that text capitalization is ignored.
        """
        statement = Statement(text='Hi HoW ArE yOu?')
        other_statement = Statement(text='hI hOw are YoU?')

        value = comparisons.synset_distance(statement, other_statement)

        self.assertEqual(value, 1)


class SentimentComparisonTestCase(TestCase):

    def test_get_initialization_functions(self):
        """
        Test that the initialization functions are returned.
        """
        functions = comparisons.sentiment_comparison.get_initialization_functions()

        self.assertIn('initialize_nltk_vader_lexicon', functions)

    def test_exact_match_different_capitalization(self):
        """
        Test that text capitalization is ignored.
        """
        statement = Statement(text='Hi HoW ArE yOu?')
        other_statement = Statement(text='hI hOw are YoU?')

        # Prepare to do the comparison
        functions = comparisons.sentiment_comparison.get_initialization_functions()
        for function in functions.values():
            function()

        value = comparisons.sentiment_comparison(statement, other_statement)

        self.assertEqual(value, 1)


class JaccardSimilarityTestCase(TestCase):

    def setUp(self):
        super().setUp()

        # Initialize the comparison function
        functions = comparisons.jaccard_similarity.get_initialization_functions()
        for _, function in functions.items():
            function()

    def test_get_initialization_functions(self):
        """
        Test that the initialization functions are returned.
        """
        functions = comparisons.jaccard_similarity.get_initialization_functions()

        self.assertIn('initialize_nltk_wordnet', functions)
        self.assertIn('initialize_nltk_averaged_perceptron_tagger', functions)

    def test_exact_match_different_capitalization(self):
        """
        Test that text capitalization is ignored.
        """
        statement = Statement(text='Hi HoW ArE yOu?')
        other_statement = Statement(text='hI hOw are YoU?')

        value = comparisons.jaccard_similarity(statement, other_statement)

        self.assertEqual(value, 1)
