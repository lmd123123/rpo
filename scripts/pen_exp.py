import numpy as np
import os
from rpo.algo import RPODDPG
from rpo.env import *
from rpo.utils.logger import Logger
import gym
import torch

np.random.seed(123)
torch.manual_seed(123)

def main():

    max_epochs = 20000

    name = "pen_ddpg"

    times = 5

    logger = Logger(("epoch", "reward", "max_ineq", "max_eq"), times=times, epochs=max_epochs, name=name)

    for _ in range(times):

        env = gym.make("SpringPendulum-v0")

        rpoagent = RPODDPG(env, "./test", name=name, logger=logger, batch_size=256, max_steps=10, warmup=0, lr_dual=0.01, corr_lr=2e-3,
                          eps=0.5, eps_start=0.5, corr_momentum=0.0,
                         eval_lr=2e-3, eval_steps=50, grad_eps=0.1, policy_fre=4, max_epochs=max_epochs,
                         capacity=20000, shared_param=False, value_type="add", clip_thres=0.2, embed_dim=128, hidden_dim=256)

        rpoagent.run()
        env.close()

    logger.save(os.path.join("./test", name))

if __name__ == "__main__":
    main()