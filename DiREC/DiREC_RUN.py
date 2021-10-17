# -*- coding: utf-8 -*-
"""
Created by: Veloci
Created on: 2020/11/18
"""
import warnings
from direc_algorithm import DiREC  # selector alias
from Handler.runfs import go_FS

warnings.filterwarnings('ignore')

DATASETS = [
    # 'Wine',
    # 'Zoo',
    # 'German',
    # 'Ionosphere',
    # 'Spectf',
    # 'Sonar',
    # ##############################
    # 'HillValley',
    # 'Musk1',
    'Madelon',
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
        # go_FS(DiREC, ds, method_name="DiREC4", n_processor=4)  # 使用笔记本4个逻辑处理器
        go_FS(DiREC, ds, method_name="DiREC8", n_processor=8)  # 使用笔记本8个逻辑处理器
        # go_FS(DiREC, ds, method_name="DiREC16",  n_processor=16)  # 使用笔记本16个逻辑处理器
