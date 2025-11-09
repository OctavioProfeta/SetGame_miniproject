import itertools
from dataclasses import dataclass
import string

# 4 features with 3 variants each
numbers = ['1','2','3']
shapes = ['diamond','squiggle','oval']
shadings = ['solid','striped','open']
colors = ['red','green','purple']

all_features_dict = {'number': numbers, 'shape': shapes, 'shading': shadings, 'color': colors}

@dataclass(frozen=True)
class Card:
    """
    A class used to represent a Set! card

    Attributes
    ----------
    number: string 
        Number of objects on card ('1', '2' or '3')
    shape: string
        Shape of the objects on card ('diamond', 'squiggle' or 'oval')
    shading: string
        Shading of the objects on card ('solid', 'striped' or 'open')
    color: string
        Color of the objects on card ('red', 'green' or 'purple')
    """
    number: string # since we are not performing arithmetics with this attribute, it can be a string instead of an int
    shape: string
    shading: string
    color: string

    # init an instance using a tuple ('number', 'shape', 'shading', 'color')
    def __init__(self, tuple):
        if len(tuple) != 4:
            raise ValueError("Tuple must have exactly 4 elements (one for each feature)!\n('number', 'shape', 'shading', 'color')")
        
        if tuple[0] not in numbers:
            raise ValueError("Number must be '1', '2' or '3' !")
        else:
            # we need to use __setattr__ to be able to add a Card to a set
            object.__setattr__(self, 'number', tuple[0])

        if tuple[1] not in shapes:
            raise ValueError("Shape must be 'diamond', 'squiggle' or 'oval' !")
        else:
            object.__setattr__(self, 'shape', tuple[1])

        if tuple[2] not in shadings:
            raise ValueError("Shading must be 'solid', 'striped' or 'open' !")
        else:
            object.__setattr__(self, 'shading', tuple[2])

        if tuple[3] not in colors:
            raise ValueError("Color must be 'red', 'green' or 'purple' !")
        else:
            object.__setattr__(self, 'color', tuple[3])

    # simple print output
    def __repr__(self):
        return "({}, {}, {}, {})".format(self.number, self.shape, self.shading, self.color)
    
def generate_combinations(groups: list[list[Card]]) -> list:
    """Given 3 groups containing cards classified by 1 feature (1 group for each variant),
    looks for all combinations of 3 cards with a different feature OR all with the same feature

    Parameters
    ----------
    groups: list[list[Card]]
        A list containing the 3 groups of cards

    Returns
    -------
    list
        A list of all possible combinations, in the form of tuples
    """
    all_combinations = []

    # within each variant (the 3 cards have the same variant)
    for group in groups:
        if len(group) >= 3:
            all_combinations.extend(itertools.combinations(group, 3))

    # between variants (the 3 cards have all different variants)
    all_combinations.extend(list(itertools.product(*groups)))

    return all_combinations

def add_card_to_group(card: Card, feature: string, groups: list) -> None:
    """Sorts a card in 1 of 3 groups depending on its variant of a specific feature

    Parameters
    ----------
    card : Card
        A Set! card
    feature: string
        The feature that we are sorting by
    groups: list
        A list of 3 groups representing the 3 variants of the feature we are sorting by
    """

    card_feature = getattr(card, feature)

    index = all_features_dict[feature].index(card_feature)
    # add to the corresponding group
    if index is not None:
        groups[index].append(card)

def find_sets(cards_in_round: list[Card]) -> list[tuple[Card]]:
    """Finds all sets within a list of cards

    Parameters
    ----------
    cards_in_round: list[Card]
        A list containing all the cards that we are playing with

    Returns
    -------
    list[tuple[Card]]
        A list of all possible sets, in the form of tuples each containing the three cards forming a set
    """

    # all groups (3 variants for each of the 4 features)
    list_of_lists = [[[] for _ in range(3)] for _ in range(4)]

    for card in cards_in_round:
        # for each feature we group the cards by that feature
        for feature, l in zip(list(all_features_dict.keys()),list_of_lists):
            add_card_to_group(card, feature, l)

    number_combinations = generate_combinations(list_of_lists[0])
    shape_combinations = generate_combinations(list_of_lists[1])
    shading_combinations = generate_combinations(list_of_lists[2])
    color_combinations = generate_combinations(list_of_lists[3])

    # we look for the combinations that appear for all features since the combinations contain either similar variants or 3 different variants for each feature
    common_combinations = set.intersection(set(number_combinations), set(shape_combinations), set(shading_combinations), set(color_combinations))

    return list(common_combinations)
