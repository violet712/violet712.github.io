import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import random
import time
import gymnasium as gym
from gymnasium.utils.save_video import save_video

# env = gym.make("FrozenLake-v1", render_mode="rgb_array_list")
# _ = env.reset()
# step_starting_index = 0
# episode_index = 0
# for step_index in range(10): 
#    action = env.action_space.sample()
#    _, _, terminated, truncated, _ = env.step(action)

#    if terminated or truncated:
#       save_video(
#          env.render(),
#          "videos",
#          fps=env.metadata["render_fps"],
#          step_starting_index=step_starting_index,
#          episode_index=episode_index
#       )
#       step_starting_index = 0
#       episode_index += 1
#       env.reset()
#       break
# env.close()


class DynaQ:
    def __init__(self, num_state, num_action, epsilon, alpha, gamma, n_planning) -> None:
        self.Q_table = np.zeros([num_state, num_action])
        self.num_action = num_action
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.n_planning = n_planning
        self.model = dict()
        
    def take_action(self, state, explore=True):  # 选取下一步的操作
        # print(self.Q_table[state])
        if np.random.random() < self.epsilon and explore == True:
            action = np.random.randint(self.num_action) # exploration
        else:
            action = np.argmax(self.Q_table[state]) # exploitation
        return action
    
    def q_learning(self, state, action, reward, next_state):
        td_error = reward + self.gamma * self.Q_table[next_state].max() - self.Q_table[state, action]
        self.Q_table[state, action] += self.alpha * td_error

    def update(self, state, action, reward, next_state):
        self.q_learning(state, action, reward, next_state)
        self.model[(state, action)] = reward, next_state  # 将数据添加到模型中
        for _ in range(self.n_planning):  # Q-planning循环
            # 随机选择曾经遇到过的状态动作对
            (state, action), (reward, next_state) = random.choice(list(self.model.items()))
            self.q_learning(state, action, reward, next_state)    


def train(env, n_planning, epsilon = 0.01, alpha=0.1, gamma=0.9):
    _ = env.reset()
    num_state = env.observation_space.n
    num_action = env.action_space.n
    agent = DynaQ(num_state, num_action, epsilon, alpha, gamma, n_planning)
    num_episodes = 300
    return_list = []
    
    for i in range(10):
        with tqdm(total=int(num_episodes / 10), desc='Iteration %d' % i) as pbar:
            for i_episode in range(int(num_episodes / 10)):
                episode_return = 0
                state, _ = env.reset()
                terminated, truncated = False, False
                while not (terminated or truncated):
                    action = agent.take_action(state, explore=True)
                    next_state, reward, terminated, truncated, _ = env.step(action)
                    episode_return += reward
                    agent.update(state, action, reward, next_state)
                    state = next_state
                return_list.append(episode_return)
                if (i_episode + 1) % 10 == 0:  # 每10条序列打印一下这10条序列的平均回报
                    pbar.set_postfix({
                        'episode':
                        '%d' % (num_episodes / 10 * i + i_episode + 1),
                        'return':
                        '%.3f' % np.mean(return_list[-10:])
                    })
                pbar.update(1)
    return return_list, agent





# env = gym.make("FrozenLake-v1", render_mode="rgb_array_list")
def show_video(agent):
   state, _ = env.reset()
   step_starting_index = 0
   episode_index = 0
   for step_index in range(100): 
      action = agent.take_action(state, explore=False)
      next_state, _, terminated, truncated, _ = env.step(action)
      state = next_state

      if terminated or truncated:
         save_video(
            env.render(),
            "videos/" + str(env.spec.id) + time.strftime("_%Y-%m-%d %H:%M:%S"),
            fps=env.metadata["render_fps"],
            step_starting_index=step_starting_index,
            episode_index=episode_index
         )
         step_starting_index = step_index + 1
         episode_index += 1
         env.reset()
         break
   env.close()

if __name__ == '__main__':
    # env = gym.make("FrozenLake-v1", render_mode="rgb_array_list")
    env = gym.make("CliffWalking-v0", render_mode="rgb_array_list")
    # state, _ = env.reset()
    # print(state)
    # a = env.action_space.sample()
    # state, _, _, _, _ = env.step(a)
    # print(state, a)
    # print(env.action_space.n)
    # print(env.observation_space.n)
    epsilon = 0.01
    alpha = 0.1
    gamma = 0.9
    #n_planning_list = [0, 2 , 20]
    n_planning_list = [20]

    for n_planning in n_planning_list:
        print('Q-planning步数为：%d' % n_planning)
        time.sleep(0.5)
        return_list, agent = train(env, n_planning)
        show_video(agent)
        episodes_list = list(range(len(return_list)))
        plt.plot(episodes_list,
                return_list,
                label=str(n_planning) + ' planning steps')
    plt.legend()
    plt.xlabel('Episodes')
    plt.ylabel('Returns')
    plt.title('Dyna-Q on {}'.format('Cliff Walking'))
    plt.show() 
