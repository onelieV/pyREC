# -*- coding: utf-8 -*-
"""
Created by: Veloci
Created on: 2020/11/18
"""
import warnings
from rec2_algorithm import REC2  # selector alias
from Handler.runfs import go_FS

warnings.filterwarnings('ignore')

DATASETS = [
    'Wine',
    # 'Zoo',
    # 'German',
    # 'Ionosphere',
    # 'Spectf',
    # 'Sonar',
    #############################
    # 'HillValley',
    # 'Musk1',
    # 'Madelon',
    # 'Isolet5',
    # ##############################
    # 'Yale',
    # 'Colon',
    # 'Lung',
    # 'Prostate_GE',
    # 'Leukemia',
    # 'Arcene',
    ##############################
]

if __name__ == '__main__':
    for ds in DATASETS:
        go_FS(REC2, ds, repeated=[20, 21, 22])  # 台式计算机上运行
