"""
Planner for Yahtzee/variable dice amount
"""

def list_powerset(lst):
    '''
    generates all sublists of a list
    '''
    return reduce(lambda result, x: result + [subset + [x] for subset in result],
                  lst, [[]])

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
        
    
    return answer_set

def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.
    hand: full yahtzee hand
    Returns an integer score 
    """
    totals_found = []
    for indx, dummy_val in enumerate(hand):
        curr_val = hand[indx]
        while indx + 1 < len(hand) and hand[indx + 1] == hand[indx]:
            curr_val += hand[indx]
            indx += 1
        totals_found.append(curr_val)
        
    return max(totals_found)

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    #assert len(held_dice) + num_free_dice is 5, "Not yatzee dice amount: %d" % (len(held_dice) + num_free_dice)
    face_list = []
    for face_value in range(num_die_sides): 
        face_list.append(face_value + 1)
    all_scores = []
    rolled_seqs = gen_all_sequences(face_list, num_free_dice)
    for seq in rolled_seqs:
        seq += held_dice
        full_hand = []
        for die in seq:
            full_hand.append(die)
        full_hand.sort()
        #print full_hand
        #print score(full_hand)
        all_scores.append(score(full_hand))
    
    exp_val = float(sum(all_scores))/float(len(all_scores))
    return exp_val

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.
    hand: full yahtzee hand
    Returns a set of tuples, where each tuple is dice to hold
    """
    holds = list_powerset(hand)
    all_holds = set()
    for hold in holds:
        temper = tuple(hold)
        all_holds.add(temper)
    return all_holds

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    highest_exp_val = 0
    best_hold = ()
    for hold in gen_all_holds(hand):
        curr_hold_val = expected_value(hold, num_die_sides, len(hand) - len(hold))
        if curr_hold_val > highest_exp_val:
            highest_exp_val = curr_hold_val
            best_hold = hold
            
    return (highest_exp_val, best_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (3,3,1,2,5)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "\nis to hold", hold, "\nwith expected score", hand_score
    
    

                                       
    
    
    



