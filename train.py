from environment import Environment
from Qlearn import Qlearn
import tkinter as tk

num_training = 50

if __name__ == "__main__":
    env = Environment()
    QL = Qlearn(env)
    for i in range(num_training):
        initial_state = env.restart()
        print("Training Sequence: ", i)
        while True:
            env.render()
            action = QL.action(initial_state) 
            next_state, reward, done = env.step(action)
            QL.alternate_train([initial_state, action, reward, next_state])
            initial_state = next_state
            if done:
                break
    policy = (QL.extract_policy(env.restart()))
    print(policy['policy'])
    print("Total Reward: ", policy['reward'])