<link rel="stylesheet" type="text/css" href="<..//..//style.css>">

# Learning and Planning in Average-Reward Markov Decision Processes

## Abstract

> We introduce learning and planning algorithms for average-reward MDPs, including
>
> 1. The first general proven-convergent off-policy model-free control algorithm without reference states.  
> 2. The first proven-convergent off-policy model-free prediction algorithm.
> 3. The first off-policy learning algorithm that converges to the actual value function rather than to the value function plus an offset. 
>
> All of our algorithms are based on using the temporal-difference error rather than the conventional error when updating the estimate of the average reward. Our proof techniques are a slight generalization of those by xxx(2001). In experiments with an Access-Control Queuing Task, we show some of the difficulties that can arise when using methods that rely on reference states and argue that our new algorithms can be significantly easier to use.

## 0. 背景知识 (Discounted Reinforcement Learning Is Not an Optimization Problem)

### Introduction

Reinforcement learning (RL) is a paradigm in which an agent learns to interact with an environment in order to maximize reward [Sutton and Barto, 2018]. Many interesting RL problems concern continuing tasks in which the agent lives and learns over a single lifetime, rather than experiencing a sequence of distinct episodes. Some examples of continuing tasks include routing internet packets, managing the inventory in a warehouse, and controlling the temperature in a data center.

In continuing tasks, it is common practice to value immediate rewards more highly than rewards further in the future — this is called temporal discounting. One reason is that the sum of future rewards (which is finite for episodic tasks) can grow to infinity as the agent and environment continually interact. With discounting the sum of the infinitely many future rewards remains bounded even when the length of the interaction does not. In this paper, we take the position that this common practice has serious conceptual flaws and should be carefully reconsidered.



**Q. 什么是平均收益?**
A. 

**Q. 为什么在持续性任务中放弃折扣回报,转而使用平均收益?**
A. 

**Q. Discounted Reinforcement Learning Is Not an Optimization Problem (why?)**
A. Discounted reinforcement learning is fundamentally incompatible with function approximation for control in continuing tasks. *It is not an optimization problem in its usual formulation, so when using function approximation there is no optimal policy*. We substantiate these claims, then go on to address some misconceptions about discounting and its connection to the average reward formulation. We encourage researchers to adopt rigorous optimization approaches, such as maximizing average reward, for reinforcement learning in continuing tasks.

## 1. Average-Reward Learning and Planning

In the average-reward setting, experience is continuing (not broken up into episodes) and the agent seeks to maximize the average reward per step, or reward rate, with equal weight given to immediate and delayed rewards.

In addition to this *control* problem, there is also the *Prediction* problem of estimating the value function and the reward rate for a given *target policy*.
Solution methods for these problems can be divided into,

1. *learning* algorithms, driven by experiential data.
2. *planning* algorithms (**规划**指任何以环境模型为输入,并生成或改进与它进行交互的策略的计算过程), driven by a model of MDP.
3. combined *learning* and *planning* methods, that first learn a model and then plan with it.

> 基于模型的方法将**规划**作为其主要组成部分, 而无模型的方法则主要依赖于**学习**. 这两类方法的核心都是价值函数的计算. 此外, 所有的方法都基于对未来事件的展望, 来计算一个回溯价值, 然后使用它作为目标来更新一个近似价值函数. 强化学习中，初始的环境是未知的，智能体与环境进行交互，然后智能体提升自身的策略；而规划方法中，环境的模型是已知的，智能体不需与环境进行交互，只需根据其模型来做计算，然后提升策略.

> **RVI Q-learning:** relative value iteration (RVI) Q-learning.

> **reference function (引用函数):** RVI Q-learning is actually a family of off-policy algorithms, a particular member of which is determined by *specifying a function that references the estimated values of specific state–action pairs and produces an estimate of the reward rate*.

> **unchain:** We assume that under the target policy there is only one possible limiting distribution for the resulting Markov chain, independent of the start state. This is known as the Markov chain being *unichain*.

**创新点:**

1. Our first contribution is to introduce such a learning control algorithm without a reference function.
    - Our Differential Q-learning algorithm is convergent for general MDPs, which we prove by slightly generalizing the theory of RVI Q-learning (Abounadi et al. 2001). Unlike RVI Q-learning, Differential Q-learning does not involve reference states. Instead, it maintains an explicit estimate of the reward rate (as in Schwartz 1993, Singh 1994).

2. Our second contribution is *Differential TD-learning*, the first off-policy model-free prediction learning algorithm proved convergent to the reward rate and differential value function of the target policy.
    - There are a number of algorithms that estimate the reward rate (e.g., Wen et al. 2020, Liu et al. 2018, Tang et al. 2019, Mousavi et al. 2020, Zhang et al. 2020a,b), but none that estimate the value function. These algorithms also differ from Differential TD-learning in that are not online algorithms; they operate on a fixed batch of data. Finally, they differ in that they *estimate the ratio of the steady-state occupancy distributions* under the target and behavior policies, whereas Differential TD-learning does not.

3. Our final contribution is to extend our off-policy algorithms to centered versions that converge to the actual value function without an <font color=Red>offest</font>.

## 2. Learning and Planning for Control

**Communicating Assumption:** For every pair of states, there exists a policy that transitions from one to the other in a finite number of steps with non-zero probability. (状态之间可以以非零概率转移)

Under the communicating assumption, there exists a unique optimal reward rate $r^{*}$ that does not depend on the start state.  We seek a learning algorithm which achieves $r^{*}$.

To define $r^{*}$, we will need the reward rate for an arbitrary policy π and a given start state s:
$$r(\pi, s) \doteq \lim _{n \rightarrow \infty} \frac{1}{n} \sum_{t=1}^{n} \mathbb{E}\left[R_{t} \mid S_{0}=s, A_{0: t-1} \sim \pi\right] \tag{1}$$

> $\bar{R}_{t}$: 给定 $\pi_t$ 时, 在时刻 t 对平均收益 $r(\pi)$ 的估计.

> I{...}: 指示函数,事件的指标函数是一个随机变量，当事件发生时取值为 1，当事件不发生时取值为 0

## 3. Empirical Results for Control
![fig1](https://pdf.cdn.readpaper.com/parsed/fetch_target/522a86da182392db5e9ba9f951ad8aa1_3_Figure_1.png)
Access-Control Queuing task ***(see: B3, Example 10.2)***

## 4. Learning and Planning for Prediction

$$\begin{aligned}
r(\pi) & \doteq \lim _{h \rightarrow \infty} \frac{1}{h} \sum_{t=1}^{h} \mathbb{E}\left[R_{t} \mid A_{0: t-1} \sim \pi\right] \\
&=\lim _{t \rightarrow \infty} \mathbb{E}\left[R_{t} \mid A_{0: t-1} \sim \pi\right], \\
&=\sum_{s} \mu_{\pi}(s) \sum_{a} \pi(a \mid s) \sum_{s^{\prime}, r} p\left(s^{\prime}, r \mid s, a\right) r
\end{aligned}$$

This inner term is the expected reward in a state under policy $\pi$. The outer sum takes the expectation over how frequently the policy is in that state. Together, we get the expected reward across states. In other words, the average reward for a policy.

## 5. Empirical Results for Prediction

![fig2](https://pdf.cdn.readpaper.com/parsed/fetch_target/522a86da182392db5e9ba9f951ad8aa1_4_Figure_2.png)

## 6. Estimating the Actual Differential Value Function

## 7. Discussion and Future Work

![fig3](https://pdf.cdn.readpaper.com/parsed/fetch_target/522a86da182392db5e9ba9f951ad8aa1_6_Figure_3.png)

> 我们必须指定一个状态的分布 $\mu(s) \geqslant 0, \quad \sum_{s} \mu(s)=1$ 来表示我们对于每个状态 $s$ 的误差的重视程度. 通常情况下, 我们将在状态 $s$ 上消耗的计算时间的比例定为$\mu(s)$ ***(see: B3, Chapter 9.2)***
> 在同轨策略中称其为*同轨策略分布*,在持续性任务中,同轨策略分布是$\pi$下的平稳分布.

## Appendix

---

**RMSVE (TVR)**: ***(see: A4-Sup.1, Chapter C.4, 3.rd paragraph)***
