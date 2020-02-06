import gym
import numpy as np
from keras.models import Model
from keras.layers import Input, Dense

def naive_sum_reward_agent(env, num_episodes=500):
    # this is the table that will hold our summated rewards for
    # each action in each state
    r_table = np.zeros((5, 2))
    for g in range(num_episodes):
        s = env.reset()
        done = False
        while not done:
            if np.sum(r_table[s, :]) == 0:
                # make a random selection of actions
                a = np.random.randint(0, 2)
            else:
                # select the action with highest cummulative reward
                a = np.argmax(r_table[s, :])
            new_s, r, done, _ = env.step(a)
            r_table[s, a] += r
            s = new_s
    return r_table

def q_learning_with_table(env, num_episodes=500, q=None):
    q_table = q if q is not None else np.zeros((5, 2))
    y = 0.95
    lr = 0.8
    for i in range(num_episodes):
        s = env.reset()
        done = False
        while not done:
            if np.sum(q_table[s,:]) == 0:
                # make a random selection of actions
                a = np.random.randint(0, 2)
            else:
                # select the action with largest q value in state s
                a = np.argmax(q_table[s, :])
            new_s, r, done, _ = env.step(a)
            q_table[s, a] += r + lr*(y*np.max(q_table[new_s, :]) - q_table[s, a])
            s = new_s
    return q_table

def run_game(table, env):
    s = env.reset()
    tot_reward = 0
    done = False
    while not done:
        a = np.argmax(table[s, :])
        s, r, done, _ = env.step(a)
        tot_reward += r
    return tot_reward

def keras_q(model, env):
    y = 0.95
    eps = 0.5
    decay_factor = 0.999
    r_avg_list = []
    for i in range(num_episodes):
        s = env.reset()
        eps *= decay_factor
        if i % 100 == 0:
            print("Episode {} of {}".format(i + 1, num_episodes))
	done = False
	r_sum = 0
	while not done:
	    if np.random.random() < eps:
	        a = np.random.randint(0, 2)
	    else:
		a = np.argmax(model.predict(np.identity(5)[s:s + 1]))
		new_s, r, done, _ = env.step(a)
		target = r + y * np.max(model.predict(np.identity(5)[new_s:new_s + 1]))
		target_vec = model.predict(np.identity(5)[s:s + 1])[0]
		target_vec[a] = target
		model.fit(np.identity(5)[s:s + 1], target_vec.reshape(-1, 2), epochs=1, verbose=0)
		s = new_s
		r_sum += r
	r_avg_list.append(r_sum / 1000)
    return model

if __name__ == "__main__":
    env = gym.make("NChain-v0")
    env.reset()
    qt = q_learning_with_table(env, num_episodes=10)
    R = run_game(qt, env)
    print(R)
    for i in range(100):
        qt = q_learning_with_table(env, 10, qt)
        R = run_game(qt, env)
        print(R)

    a = Input(shape=(1,5))
    b = Dense(10, activation="sigmoid")(a)
    c = Dense(2, activation="linear")(b)
    model = Model(inputs=a, outputs=c)
    model.compile(loss='mse', optimizer='adam', metrics=['mae'])
    
    model = keras_q(model, env)

