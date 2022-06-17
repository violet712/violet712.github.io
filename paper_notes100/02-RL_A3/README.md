<link rel="stylesheet" type="text/css" href="<../../style.css>">

# Average-Reward Off-Policy Policy Evaluation with Function Approximation

## Abstract

> We consider off-policy policy evaluation with function approximation (FA) in average-reward MDPs, where the goal is to estimate both the reward rate and the differential value function. For this problem, bootstrapping is necessary and, along with off-policy learning and FA, results in the deadly triad (Sutton & Barto, 2018). To address the deadly triad, we propose two novel algorithms, reproducing the celebrated success of Gradient TD algorithms in the average-reward setting. In terms of estimating the differential value function, the algorithms are the first convergent off-policy linear function approximation algorithms. In terms of estimating the reward rate, the algorithms are the first convergent off-policy linear function approximation algorithms that do not require estimating the density ratio. We demonstrate empirically the advantage of the proposed algorithms, as well as their nonlinear variants, over a competitive density-ratio-based approach, in a simple domain as well as challenging robot simulation tasks.

我们考虑在平均奖励MDPs中使用函数逼近(FA)进行异策策略评估，其目标是同时估计奖励率和微分价值函数。对于这个问题，自举是必要的，加上异策学习和函数逼近，导致了致命三要素(deadly triad)。为了解决这一致命的问题，我们提出了两种新颖的算法，在平均奖励环境中再现了梯度TD算法的成功。在估计微分价值函数方面，该算法是第一个收敛的非策略线性函数逼近算法。在估计奖励率方面，该算法是不需要估计密度比的第一个收敛的异策线性函数逼近算法。在简单的领域以及具有挑战性的机器人模拟任务中，我们通过经验证明了所提出的算法及其非线性变体的优势，优于有竞争力的基于密度比的方法。

### 0. 前置知识

**Average-reward MDP:**
与折扣设定一样,平均收益 ***(see: B3, Chapter 10.3)*** 也适用于持续性问题,即智能体与环境之间的交互一直持续而没有对应的终止或开始状态.然而,与"折扣"设定不同的是,这里不考虑任何折扣,智能体对于延迟收益的重视程度与即时收益相同.折扣设定对函数逼近来说是有问题的,因此需要用平均收益设定来替换它. ***(see: B3, Chapter 10.4)***
> In the average-reward setting, the quality of a policy $\pi$ is defined as the average rate of reward, or simply average reward, while following that policy, which we denote as $r(\pi)$:

**The Deadly Triad:** The danger of instability and divergence arises whenever we combine all of the following three elements. ***(see: B3, Chapter 11.3)***

1. Function approximation:
2. Bootstrapping: Using current target estimation value to update to attain new target estimation value. *the estimated values must be updated towards targets that include existing estimated values instead of actual returns.*
3. Off-policy training:

## 1. Introduction

### 1.1. Problem

A fundamental problem in average-reward Markov Decision Processes $<\mathcal{S, A, P, R, \gamma}>$ is *policy evaluation* --- for a given policy, estimating the *reward rate* and the *differential value function*.

1. Reward rate -- The reward rate of a policy is the average reward per step and thus measures the policy's long term performances.
2. Differential value function -- The differential value function summarizes the expected cumulative future excess rewards, which are the differences between received rewards and the reward rate.

### 1.2. Main Contributions

1. The two algorithms we propose are the first provably convergent methods for learning the differential value function via off-policy linear function approximation.
2. The two algorithms we propose are the first provably convergent differential-valuebased methods for reward rate estimation via off-policy linear function approximation.

> All existing methods for estimating reward rate in off-policy function approximation setting require learning the density ratio, i.e., the ratio between the stationary distribution of the target policy and the sampling distribution.

density ratio:

## 2. Background

$\|\cdot\|_{M}$ to denote the vector norm induced by the positive definite matrix $M$. 由正定矩阵导出的向量范数

When it does not confuse, we use a function and a vector interchangeably. For example, if $f$ is a function from $\mathcal{X}$ to $\mathbb{R}$, we also use $f$ to denote the corresponding vector in $\mathbb{R}^{|\mathcal{X}|}$.

The reward rate of policy $\pi$ is defind as
$$r_{\pi} \doteq C-\lim_{t \rightarrow \infty} \mathbb{E}\left[r\left(S_{t}, A_{t}\right) \mid \pi, S_{0}\right] \tag{1}$$
where $C-\lim _{T \rightarrow \infty} z_{T} \doteq \lim _{T \rightarrow \infty} \frac{1}{T+1} \sum_{i=0}^{T} z_{i}$ is the Cesaro limit. The Cesaro limit in (1) is assumed to exist and is independent of $S_{0}$.
> **Cesaro limit:**  Cesaro limits are employed when analysing sequences which do not converge (in the sense of having a limit). They are a weaker concept than limits (but stronger than Banach limits).
> For example, the sequence 0,1,0,1,... (which has no limit!) has Cesaro limit 1/2. This is particularly satisfying, as it seems like the right number.

为了保证Cesaro收敛,做出如下假设:
**Assumption 2.1. Policy $\pi$ induces a unichain**

```
1. w.r.t.   ------- with respect to 常用于求导，或者满足一定条件之类的情况
2. s.t.     ------- subject to  约束与
3. r.v.     ------- random variable 随机变量
4. i.f.f.      ------- if and only if
5. i.i.d.  ------- independently and identically distributed 独立同分布
```
 
