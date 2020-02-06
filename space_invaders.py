import gym
from keras.models import Model
from keras.layers import Input, Dense, Conv2D, MaxPool2D, Flatten

def build_model(input_shape, output_size=6):
    x = Input(shape=input_shape)
	h1 = Conv2D(64, [5, 5], 2, activation="relu")(x1)
	h2 = Conv2D(128, [3, 3], 1, activation="relu")(h1)
	h2 = MaxPool2D(2)(h2)
	h3 = Conv2D(256, [3, 3], 1, activation="relu")(h2)
    h3 = MaxPool2D()(h3)
	h4 = Conv2D(512, [3, 3], 1, activation="relu")(h3)
    h4 = MaxPool2D()(h4)
	h4 = Flatten()(h4)
	h5 = Dense(128, activation="sigmoid")(h4)
	y = Dense(output_size, activation="softmax")(h5)
	model = Model(inputs=x, outputs=y)
	return model


def train(env, num_ep=1000):
    y = 0.95
    eps = 0.05
    decay_factor = 0.999
	model = build_model(env.reset().shape)
    r_avg_list = []
    for i in range(num_ep):
        s = env.reset()
        eps *= decay_factor
        if i % 100 == 0:
            print("Episode {} of {}".format(i + 1, num_episodes))
		done = False
		r_sum = 0
		while not done:
	    	if np.random.random() < eps:
	        	a = np.random.randint(0, 6)
	    	else:
				a = np.argmax(model.predict(s))
			new_s, r, done, _ = env.step(a)
			target = r + y * np.max(model.predict(new_s))
			model.fit(s, target, epochs=1, verbose=0)
			s = new_s
			r_sum += r
		r_avg_list.append(r_sum / 1000)
    return model

def run(env=None, model=None):
    if env is None:
		env = gym.make("SpaceInvaders-v0")
    observation = env.reset()
    for _ in range(1000):
		env.render()
		if model is None:
	    	action = env.action_space.sample() # your agent here (this takes random actions)
		observation, reward, done, info = env.step(action)

    	if done:
			observation = env.reset()
    env.close()

if __name__ == "__main__":
	env = gym.make("SpaceInvaders-v0")
	model = train(env)
	run(env, model)
