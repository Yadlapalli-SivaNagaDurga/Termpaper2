# train_q_learning.py
import numpy as np
import random
import pickle

states = ['low', 'medium', 'high']
actions = ['deploy', 'block']
q_table = np.zeros((len(states), len(actions)))

alpha = 0.1
gamma = 0.9
epsilon = 0.1

def get_reward(state, action):
    if state == 'high' and action == 'deploy':
        return -10
    elif state == 'medium' and action == 'deploy':
        return 5
    elif state == 'low' and action == 'deploy':
        return 10
    elif action == 'block':
        return 2
    return 0

state_index = {s: i for i, s in enumerate(states)}

for episode in range(1000):
    state = random.choice(states)
    s_idx = state_index[state]

    if random.uniform(0, 1) < epsilon:
        a_idx = random.randint(0, 1)
    else:
        a_idx = np.argmax(q_table[s_idx])

    action = actions[a_idx]
    reward = get_reward(state, action)

    next_state = random.choice(states)
    next_s_idx = state_index[next_state]

    q_table[s_idx][a_idx] = (1 - alpha) * q_table[s_idx][a_idx] + alpha * (reward + gamma * np.max(q_table[next_s_idx]))

pickle.dump(q_table, open("q_table.pkl", "wb"))
print("✅ Q-learning trained and saved as q_table.pkl")
