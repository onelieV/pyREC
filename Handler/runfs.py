# -*- coding: utf-8 -*-
"""
Created by: Veloci
Created on: 2020/11/18
"""
import os, shutil
import time
from sklearn.base import clone
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import StratifiedKFold, train_test_split
from Handler.loadDS import load_ds_name

DATASETS = [
    # 'Wine',
    # 'Zoo',
    # 'German',
    # 'Ionosphere',
    # 'Spectf',
    # 'Sonar',
    # ###########
    # 'HillValley',
    # 'Musk1',
    # 'Madelon',
    # 'Isolet5',
    # ##########
    # 'Yale',
    # 'Lung',
    # 'Prostate_GE',
    # 'Arcene',
]


def go_FS(slctr, ds, method_name=None, repeated=None, **kwargs):  # repeated=None

    record_dict = {
        'no.': None,
        'accuracy': None,
        'size': None,
        'time': None,
        'gross': None,
        'net': None,
        'arise': None,
        'subset': None,
    }

    if not repeated:
        repeated = [r for r in range(20)]
    elif not isinstance(repeated, list):
        print("'repeated' must be a list/tuple with the independent run serial number!")
        raise ValueError

    print("Start the process of {} on {}".format(slctr.__name__, ds).center(100, '*'))
    X, y = load_ds_name(ds)
    result_path = "../XResult/{}/{}".format(slctr.__name__, ds)
    if method_name:
        result_path = "../XResult/{}/{}".format(method_name, ds)
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    if kwargs.get('anew'):  # 如果要完全重新运行，删除之前的结果数据
        shutil.rmtree(result_path)
        os.makedirs(result_path)

    result_meta = result_path + "/{}_meta".format(ds)

    # X = MinMaxScaler().fit_transform(X)
    clf = KNeighborsClassifier(n_neighbors=5)
    # clf = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
    CV = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)

    for r in repeated:
        selector = slctr(X, y, clone(clf), CV, outpath=result_path + "/{}_{}".format(ds, r),
                         n_processor=kwargs.get('n_processor', 1))
        t_begin = time.time()
        p = selector.fit()
        t_done = time.time()
        print("  {}_{} completed!".format(ds, r), "用时：{:.0f}s".format(t_done - t_begin))

        record_dict['no.'] = r
        record_dict['accuracy'], record_dict['subset'] = p
        record_dict['size'] = len(p[1])
        record_dict['gross'] = selector.snake.gross_counter
        record_dict['net'] = selector.snake.net_counter
        record_dict['arise'] = selector.snake.best_[2]
        record_dict['time'] = round(t_done - t_begin, 4)

        with open(result_meta, 'a') as f:
            f.write(str(record_dict))
            f.write("\n")

    print("End the process of {} on {}".format(slctr.__name__, ds).center(100, '='))
    print("\n")
