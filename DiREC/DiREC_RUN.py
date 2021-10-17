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
    ##############################
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
        # 必须要手动建立集群之后才能运行
        go_FS(DiREC, ds, method_name="DiREC8", n_processor=8)  # 使用8个逻辑核
        go_FS(DiREC, ds, method_name="DiREC16", n_processor=16)  # 使用16个逻辑核
        go_FS(DiREC, ds, method_name="DiREC24", n_processor=24)  # 使用24个逻辑核
