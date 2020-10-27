import unittest
from time import sleep
from ozone.taxonomy import WordnetTaxonomy, TaxonomyPuzzleGenerator
from nltk.corpus import wordnet as wn


class TestTaxonomy(unittest.TestCase):
    
    def setUp(self):
        self.taxonomy = WordnetTaxonomy('apple.n.1')    
     
    def test_get_vocab(self):
        expected = {'apple': 0, 'baldwin': 1, "bramley's seedling": 2, 
                    'cooking apple': 3, 'cortland': 4, 
                    "cox's orange pippin": 5, 'crab apple': 6, 'crabapple': 7, 
                    'delicious': 8, 'dessert apple': 9, 'eating apple': 10, 
                    'empire': 11, 'golden delicious': 12, 'granny smith': 13, 
                    "grimes' golden": 14, 'jonathan': 15, 
                    "lane's prince albert": 16, 'macoun': 17, 
                    'mcintosh': 18, 'newtown wonder': 19, 'northern spy': 20, 
                    'pearmain': 21, 'pippin': 22, 'prima': 23, 
                    'red delicious': 24, 'rome beauty': 25, 'stayman': 26, 
                    'stayman winesap': 27, 'winesap': 28, 
                    'yellow delicious': 29}  
        assert self.taxonomy.get_vocab() == expected

    def test_get_root_node(self):
        expected = "apple.n.01"        
        assert self.taxonomy.get_root_node() == expected
        
    def test_random_node(self):
        assert self.taxonomy.random_node(18,20) == 'eating_apple.n.01'
        assert self.taxonomy.random_node(5,5) == 'cooking_apple.n.01'
        assert self.taxonomy.random_node(6,21) != None
        
    def test_random_descendants(self):
        
        expected = set(["lane's_prince_albert.n.01",
                        "bramley's_seedling.n.01",
                        'newtown_wonder.n.01',
                        'rome_beauty.n.01'])
        result = set(self.taxonomy.random_descendants('cooking_apple.n.01', 4))
        assert result == expected

    def test_get_children(self):
        expected = set ([
            "cooking_apple.n.01",
            "crab_apple.n.03",
            "eating_apple.n.01"
        ])
        result = set([x for x in self.taxonomy.get_children("apple.n.01")])
        #print(result)
        assert result == expected
        
    def test_random_non_descendant(self):
        non_eating_apples = ["bramley's_seedling.n.01",
                             'cooking_apple.n.01',
                             'crab_apple.n.01',
                             'crabapple.n.01',
                             'crab_apple.n.03',
                             "lane's_prince_albert.n.01",
                             'newtown_wonder.n.01',
                             'rome_beauty.n.01',
                             'cooking_apple.n.01']
        for _ in range(10):
            non_descendant = self.taxonomy.random_non_descendant('eating_apple.n.01')
            assert non_descendant in non_eating_apples

    def test_wu_palmer_similarity(self):
        sim1 = self.taxonomy.wu_palmer_similarity(("cooking_apple.n.01"),
                                                  ("crab_apple.n.01"))
        assert sim1 == 0.25
        sim2 = self.taxonomy.wu_palmer_similarity(("red_delicious.n.01"),
                                                  ("granny_smith.n.01"))
        assert sim2 == 0.88
            
    def test_puzzle_gen(self):
        cooking_apples = set(["lane's_prince_albert.n.01",
                              "bramley's_seedling.n.01",
                              'cooking_apple.n.01',
                              'newtown_wonder.n.01',
                              'rome_beauty.n.01'])
        puzzgen = TaxonomyPuzzleGenerator(self.taxonomy, 4)
        puzzgen.specificity_lb = 5
        puzzgen.specificity_ub = 5
        for i in range(100):
            (choices, oddman) = puzzgen.generate()
            assert len(set(choices)) == len(choices)
            for i, choice in enumerate(choices):
                if i == oddman:
                    assert choice not in cooking_apples
                else:
                    assert choice in cooking_apples
                
if __name__ == "__main__":
	unittest.main()
