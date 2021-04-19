import sys
import time

def is_prime(num):

    if num <= 1:
        return False
    elif num == 2:
        return True
    elif num%2 == 0:
        return False
    else:
        cap = int(num**(1/2))

        for candidate in range(3, cap+1, 2):
            if num%candidate == 0:
                return False

        return True

def static_board_evaultion(last_move, taken_tokens, next_possible_moves, is_max_turn):

    result = 0
    
    if len(next_possible_moves) == 0:
        result = -1
    # case 1: if token 1 not taken, return 0
    elif not taken_tokens[1]:
        result = 0
    # case 2: if last move is 1, count legal moves, if odd return 0.5 otherwise -0.5
    elif last_move == 1:
        result = 0.5 if len(next_possible_moves)%2 != 0 else -0.5
    else:
        # case 3: if last move is prime, count multiples of that prime, if odd return 0.7 otherwise -0.7
        if is_prime(last_move):
            result = 0.7 if len(next_possible_moves)%2 != 0 else -0.7
        else:
            #case 4: if last move composite, find largest prime that divides last move, count multiples, if odd return 0.6 otherwise -0.6

            candidate = last_move/2

            count = 0

            while candidate > 0:
                if last_move%candidate == 0:
                    if is_prime(candidate):
                        for num in next_possible_moves:
                            if num%candidate == 0:
                                count += 1
                        # Here we have largest prime that divides last move
                        break
                candidate -=1
            result = 0.6 if count%2 != 0 else -0.6

    # Here, we negate the result if it is not max turn.
    return result if is_max_turn else -result

def possibleMoves(n_tokens, n_taken_tokens, taken_tokens, last_move):
   
    # At first move, player must choose odd-numbered token (strictly less than n/2)
    if n_taken_tokens == 0:
        return [i for i in range(1, (n_tokens+1)//2, 2)]

    # List to save the result
    possible_moves = []

    # geting factors and making sure it is not already taken
    cap = int(last_move**(1/2))
    for candidate in range(1, cap+1):
        if last_move % candidate == 0:
            factor1 = candidate
            factor2 = last_move//candidate

            # If the first factor (factor1) is not already taken, insert it in possible_moves list
            if not taken_tokens[factor1]:
                possible_moves.append(factor1)
            
            # If the factor2 is not already taken, insert it in possible_moves list (and not equal to factor1)
            if factor1 != factor2 and not taken_tokens[factor2]:
                possible_moves.append(factor2)
    
    # getting multiples and making sure it is not already taken
    for i in range(last_move*2, n_tokens+1, last_move):
        if not taken_tokens[i]:
            possible_moves.append(i)
    

    return possible_moves

# Class Stat that saves info of the Alpha-Beta pruning algorithm
class Stat:
    def __init__(self):
        self.nodes_visted = 0
        self.nodes_evaluated = 0
        self.maxDepth_reached = 0

        # store the time this object has been created to calculate execution time
        self.__start_time = time.time()
    
    def get_stats(self):
        # avg_branching_factor = (nodes_visited - 1) / (nodes_visited - nodes_evaluated) = avg num of branches per parent node
        avg_branching_factor = (self.nodes_visted - 1) / (self.nodes_visted - self.nodes_evaluated)
        execution_time = time.time() - self.__start_time

        return self.nodes_visted, self.nodes_evaluated, self.maxDepth_reached, avg_branching_factor, execution_time
    
    def increment_nodes_visted (self):
        self.nodes_visted += 1
    
    def increment_nodes_evaluated(self):
        self.nodes_evaluated += 1
    
    def set_maxDepth_reached(self, depth):
        self.maxDepth_reached = max(self.maxDepth_reached, depth)

def alpha_beta(n_tokens, n_taken_tokens, taken_tokens, last_move, max_depth):
    
    value, best_move = None, None

    stats = Stat()

    is_max_turn = (n_taken_tokens%2 == 0)
    if is_max_turn:
        value, best_move = max_value(n_tokens, n_taken_tokens, taken_tokens, last_move, 0, max_depth, float('-inf'), float('inf'), stats)
    else:
        value, best_move = min_value(n_tokens, n_taken_tokens, taken_tokens, last_move, 0, max_depth, float('-inf'), float('inf'), stats)

    return best_move, value, *stats.get_stats()

def max_value(n_tokens, n_taken_tokens, taken_tokens, last_move, depth, max_depth, alpha, beta, stats):
    stats.set_maxDepth_reached(depth)
    stats.increment_nodes_visted ()
    
    next_possible_moves = possibleMoves(n_tokens, n_taken_tokens, taken_tokens, last_move)
    if len(next_possible_moves) == 0 or (max_depth != 0 and depth == max_depth):
        stats.increment_nodes_evaluated()
        return static_board_evaultion(last_move, taken_tokens, next_possible_moves, True), None
    
    v = float('-inf')
    best_move = None

    total_branches_visited = 0

    for move in next_possible_moves:
        taken_tokens[move] = True

        v2, move2 = min_value(n_tokens, n_taken_tokens + 1, taken_tokens, move, depth + 1, max_depth, alpha, beta, stats)

        total_branches_visited += 1

        if (v2 > v) or (v2 == v and (best_move is None or move < best_move)):
            v, best_move = v2, move
            alpha = max(alpha, v)

        # backtrack
        taken_tokens[move] = False

        if v >= beta:
            break

    return v, best_move


def min_value(n_tokens, n_taken_tokens, taken_tokens, last_move, depth, max_depth, alpha, beta, stats):
    stats.set_maxDepth_reached(depth)
    stats.increment_nodes_visted ()
    
    next_possible_moves = possibleMoves(n_tokens, n_taken_tokens, taken_tokens, last_move)
    if len(next_possible_moves) == 0 or (max_depth != 0 and depth == max_depth):
        # if terminal state or we reached max_depth
        stats.increment_nodes_evaluated()
        return static_board_evaultion(last_move, taken_tokens, next_possible_moves, False), None
    
    v = float('inf')
    best_move = None

    total_branches_visited = 0

    for move in next_possible_moves:
        taken_tokens[move] = True
        
        v2, move2 = max_value(n_tokens, n_taken_tokens + 1, taken_tokens, move, depth + 1, max_depth, alpha, beta, stats)

        total_branches_visited += 1

        if (v2 < v) or (v2 == v and (best_move is None or move < best_move)):
            v, best_move = v2, move
            beta = min(beta, v)

        # backtrack
        taken_tokens[move] = False

        if v <= alpha:
            break
    
    return v, best_move

if __name__ == '__main__':
    n_tokens = int(sys.argv[1])
    n_taken_tokens = int(sys.argv[2])

    taken_tokens = [False]*(n_tokens+1)
    for i in range(n_taken_tokens):
        taken_tokens[int(sys.argv[3+i])] = True
    
    depth = int(sys.argv[-1])

    last_move = None if n_taken_tokens == 0 else int(sys.argv[-2])

    # Perform minimax with alpha-beta pruning to find best move
    best_move, value, nodes_visted , num_nodes_evaluated, max_depth_reached, avg_branching_factor, execution_time \
        = alpha_beta(n_tokens, n_taken_tokens, taken_tokens, last_move, depth)

    
# Output 
print()
print()
print()
print('Move: {}'.format(best_move))
print('Value: {:.1f}'.format(value))
print('Number of Nodes Visited: {}'.format(nodes_visted ))
print('Number of Nodes Evaluated: {}'.format(num_nodes_evaluated))
print('Max Depth Reached: {}'.format(max_depth_reached))
print('Avg Effective Branching Factor: {:.1f}'.format(avg_branching_factor))
print()
print()
print('Execution time: {} s'.format(execution_time))
print()
