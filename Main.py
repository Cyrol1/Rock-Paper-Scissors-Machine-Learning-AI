import random
import pickle


valid_moves = ['rock', 'paper', 'scissors']


try:
    with open("qtable.pickle", "rb") as f:
        Q = pickle.load(f)
except FileNotFoundError:
    Q = {}
    for i in valid_moves:
        for j in valid_moves:
            Q[(i, j)] = [0, 0, 0]


alpha = 10  
gamma = 900
epsilon = 0.05  

pattern_memory = {}

def get_pattern(state):
  state_str = str(state)

  if not isinstance(state, tuple):
    return None

  if state_str in pattern_memory:
    return pattern_memory[state_str]

  return None


def add_pattern(state, pattern):
  state_str = str(state)

  pattern_memory[state_str] = pattern

  if pattern not in Q:
    Q[(state, pattern)] = [0, 0, 0]


def choose_next_move(state):
  pattern = get_pattern(state)
  if pattern is not None and pattern in Q:
    q_values = Q[(state, pattern)]
  else:
    q_values = Q[state]

  if random.random() < epsilon:
    return random.choice(valid_moves)

  max_q_value = max(q_values)
  if q_values.count(max_q_value) > 1:
    best_moves = [
      i for i in range(len(valid_moves)) if q_values[i] == max_q_value
    ]
    return valid_moves[random.choice(best_moves)]
  else:
    return valid_moves[q_values.index(max_q_value)]

num_rounds = int(input("How many rounds do you want to play? "))

for round_num in range(1, num_rounds + 1):
    print(f"Round {round_num}:")
    
    state = ('rock', 'rock')
    
    for t in range(100):
        move = choose_next_move(state)
        
        computer_move = random.choice(valid_moves)
        
        reward = 0
        if move == computer_move:
            reward = 1
        elif move == 'rock' and computer_move == 'scissors' or move == 'paper' and computer_move == 'rock' or move == 'scissors' and computer_move == 'paper':
            reward = 5000000
        else:
            reward = -100000000
        next_state = (move, computer_move)
        Q[state][valid_moves.index(move)] += alpha * (reward + gamma * max(Q[next_state]) - Q[state][valid_moves.index(move)])
        
        state = next_state

    user_move = input("Enter your move (rock, paper, scissors): ").lower()

    while user_move not in valid_moves:
        print("Invalid move, please try again.")
        user_move = input("Enter your move (rock, paper, scissors): ").lower()

    computer_move = choose_next_move((user_move, random.choice(valid_moves)))

    print("You chose:", user_move)
    print("Computer chose:", computer_move)

    if user_move == computer_move:
        print("It's a tie!")
    elif user_move == 'rock' and computer_move == 'scissors' or user_move == 'paper' and computer_move == 'rock' or user_move == 'scissors' and computer_move == 'paper':
        print("You win!")
    else:
        print("Computer wins!")
        
with open("qtable.pickle", "wb") as f:
    pickle.dump(Q, f)
