# -*- coding: utf-8 -*-
"""
Created by: Veloci
Created on: 2021/3/29
"""
import ray
import math
import random
from sklearn.model_selection import cross_val_score


def envelope(X, y, clf, cv):
    # envelope an evaluator to distribute in the cluster
    def evaluate(subset):
        # subset must be list form with the indices for example [0,2,4,10,11]
        if not subset:  # this case won't happen
            eva = 0
        else:
            scores = cross_val_score(clf, X[:, subset], y, cv=cv)  # 注意cv一定要关键字给出
            eva = scores.mean().round(5)
        return eva

    return evaluate


class Snake(object):
    def __init__(self, record_name='default'):
        self.ReName = record_name
        self.records = []
        self.gross_counter = 0
        self.net_counter = 0
        self.best_ = (0, 0, 0)
        with open(self.ReName, 'w') as f:  # 生成一个文件记录评估过程，用于后续分析
            f.write('')

    def eat(self, ls):
        head = ls.pop()  # 弹出末尾子集本身
        better = []
        while ls:
            eva_subset = ls.pop()
            self.gross_counter += 1

            if eva_subset[0] >= head[0]:
                better.append(eva_subset)
            if eva_subset not in self.records:
                self.net_counter += 1
                self.records.append(eva_subset)
                with open(self.ReName, 'a') as f:
                    f.write("{:>4d}, ".format(self.gross_counter))  # 评价序号
                    f.write("{:>4d}, ".format(self.net_counter))  # 净评价个数
                    f.write("({:>8.5f}, ".format(eva_subset[0]))  # 评估值  # cv_
                    f.write("{:>4d}), ".format(len(eva_subset[1])))  # 子集大小
                    # f.write("{}".format(subset))  # 子集
                    f.write("\n")

                self.best_ = max(self.best_, (eva_subset[0], len(eva_subset[1]), self.gross_counter),
                                 key=lambda t: (t[0], -t[1], -t[2]))

                print('\r', self.net_counter, '/', self.gross_counter, eva_subset[0], len(eva_subset[1]), end='')
                print(" optimizing objectives", self.best_, end='')

        better.sort(key=lambda t: (t[0], -len(t[1])))
        # better = better[int(math.floor(len(better) / 2)):]
        better = better[-2:]
        return better


@ray.remote
def RECurrent(e0, S0, evaluate):  # 向下搜索子集的起点, evaluate是一个评估函数，将由本地推送到远程，从而就近调用
    L = []  # 子集列表
    gap = math.sqrt(len(S0)) if len(S0) > 100 else 2

    def randBisectElim(S, E):
        if len(E) < gap:
            return
        else:
            random.shuffle(E)
            E_left, E_right = E[:int(0.5 * len(E))], E[int(0.5 * len(E)):]  # randomly bisect E
            S_left, S_right = ([f for f in S if f not in EE] for EE in (E_left, E_right))
            eva_L, eva_R = [evaluate(S) for S in (S_left, S_right)]
            L.extend([(eva_L, S_left), (eva_R, S_right)])
            e_t, S_t, E_t = max((eva_L, S_left, E_left), (eva_R, S_right, E_right),
                                key=lambda t: (t[0], -len(t[1])))
            randBisectElim(S.copy(), E_t.copy())
            return

    randBisectElim(S0.copy(), S0.copy())
    L.append((e0, S0))  # 把自己加在末尾
    return L  # 比S0更好的子集列表，本次总共产生的子集个数


class DiREC(object):
    def __init__(self, X, y, clf, cv, outpath='dataset', **kwargs):
        self.X, self.y, self.clf, self.cv = X, y, clf, cv
        self.snake = Snake(record_name=outpath)
        self.maxEva = max(3000, 100 * int(X.shape[1] ** 0.5))
        print("\n最大评估次数：", self.maxEva)

        self.n_processor = kwargs.get('n_processor', 1)

    def fit(self):
        evar = envelope(self.X, self.y, self.clf, self.cv)  # 封装评估函数
        A = list(range(self.X.shape[1]))  # Full特征索引列表
        e_A = evar(A)  # 评估Full特征的目标值
        p = (e_A, A)
        T = []  # 任务队列 item=(eva, subset)
        R = []  # worker返回的结果Refs队列

        ray.init()  # ray初始化, 单机运行时用
        evar_ref = ray.put(evar)  # 将评估函数封装好并放入ObjectStore中，方便远程调用
        n_p = ray.available_resources()['CPU']  # n_p
        print('Available CPU:', n_p)
        print('Required processor:', self.n_processor)
        n_p = min(n_p, self.n_processor)
        print('Real run using processors:', n_p)

        self.snake.eat([p, p])  # 把第0次评估也记录进去
        period = 0  # 定期重新以当前最优为起点进行搜索
        while self.snake.gross_counter < self.maxEva:
            if not T:
                T.append((e_A, A))

            while len(R) < n_p and T:
                R.append(RECurrent.remote(*T.pop(), evar_ref))
            finished, R = ray.wait(R, num_returns=1)  # 等待完成一个远程任务的返回
            reached_subsets = ray.get(finished)[0]  # 取出这次任务访问过的子集，注意finished是个列表，取索引为0的这个
            better_subs = self.snake.eat(reached_subsets)  #
            T += better_subs
            T.sort(key=lambda t: (t[0], -len(t[1])))  # sort is needed in distributed version

            if better_subs:
                p = max(p, *better_subs, key=lambda t: (t[0], -len(t[1])))

            ################################################################
            # if self.snake.gross_counter // 100 == period:
            #     pass
            # else:
            #     period += 1
            #     T.append(p)
            ################################################################

        ray.shutdown()  # 关闭ray服务
        return p


if __name__ == '__main__':
    import sys
    import time
    import warnings
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.model_selection import StratifiedKFold
    from Handler.loadDS import load_ds_name

    warnings.filterwarnings('ignore')
    sys.path.insert(0, '..')  # 使得在命令行运行时可以找到自己的模块(设置工作路径)

    dataset_name = 'Arcene'
    X, y = load_ds_name(dataset_name)
    clf = KNeighborsClassifier(n_neighbors=5)
    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

    start_time = time.time()

    slctr = DiREC(X, y, clf, cv, dataset_name)
    opt = slctr.fit()

    print(" 最优子集：{}".format(opt))
    print(' 运行时长{:.3f}秒'.format(time.time() - start_time))
    print(slctr.snake.gross_counter, slctr.snake.net_counter)
