import numpy as np 



class Qlearn():
    def __init__(self, env):
        self.env = env
        self.num_states = env.num_states()
        self.num_actions = env.num_actions()
        self.discount_factor = 0.9
        self.learning_rate = 0.2
        self.epsilon = 0.01
        '''
        Q-table for state X action pairs.
        Each row represents a unique state in the grid
        Each row has 4 columns ergo, each corresponding to Q value for a particular action
        There are 4 actions : up, left, down and right
        qtable[s][0] corresponds to going up from state s
        qtable[s][1] corresponds to going left from state s
        qtable[s][2] corresponds to going down from state s
        qtable[s][3] corresponds to going right from state s
        '''
        self.qtable = np.zeros([self.num_states, self.num_actions])
    
    def action(self, state):

        ##Introduce randomness by trying to explore new paths
        if np.random.uniform() > self.epsilon:
            #print("State, State values: ",state, self.qtable[state])
            max_action_qvalue = np.amax(self.qtable[state])
            same_q_values = np.where(self.qtable[state] == max_action_qvalue)
            return np.random.choice(same_q_values[0])
        else:
            action_to_take = np.random.choice(self.num_actions)
            self.epsilon = 0 if self.epsilon < 0 else self.epsilon-0.001 
            return action_to_take
    
    def alternate_train(self, Qsa):
        curr_state, action, reward, next_state = Qsa[0], Qsa[1], Qsa[2], Qsa[3]
        next_state_transition_value = reward + self.discount_factor*np.amax(self.qtable[next_state])
        self.qtable[curr_state][action] = (1-self.learning_rate)*self.qtable[curr_state][action] + self.learning_rate*(next_state_transition_value)

    #args: state_action_seq
    ## Tuple consisting of current state, action to perform, immediate reward, next state
    #Q learning formula: Q[s][a] = Q[s][a] + alpha*(reward[s][a] + gamma*(max(newstate_Q[s][a])-Q[s][a]))
    def train(self, Qsa):
        curr_state, action, reward, next_state = Qsa[0], Qsa[1], Qsa[2], Qsa[3]
        max_next_state_value = np.amax(self.qtable[next_state])
        self.qtable[curr_state][action] += self.learning_rate*(reward + self.discount_factor*(max_next_state_value-self.qtable[curr_state][action]))
        
    def extract_policy(self):
        policy = []
        initial_state = self.env.initial_state
        return policy
