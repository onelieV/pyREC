# -*- coding: utf-8 -*-
"""
Created by: Veloci
Created on: 2021/3/8
"""
import numpy as np
from scipy.io import loadmat

DATASETS = {
    'Arcene': 'load_Arcene',
    'Colon': 'load_Colon',
    'DLBCL': 'load_DLBCL',
    # 'Gait': 'load_Gait',  # From UCI archive
    'Leukemia': 'load_Leukemia',
    'Lung': 'load_Lung',
    'SRBCT': 'load_SRBCT',
    'Prostate_GE': 'load_ProGE',
    'TOX_171': 'load_TOX_171',
    'Yale': 'load_Yale',
    '11_Tumors': 'load_11_Tumors',
}


#############basic function################
def load_hdmat(path):
    m = loadmat(path)
    if 'data' in m:
        X, y = m['data'][:, 1:], m['data'][:, 0]
    else:
        X, Y = m['X'], m['Y']
        y = Y.ravel()
    return X, y


def load(dataset):
    if dataset in DATASETS:
        return eval(DATASETS[dataset])()
    else:
        print('dataset {} is invalid'.format(dataset))


#################load_DataSet()#################
def load_Arcene():
    name = 'Arcene'
    path = '../ASUdataset/DataMat/arcene.mat'
    X, y = load_hdmat(path)
    print("数据集 " + name, "样本*维度 ", X.shape, "类别：数量", {l: y.tolist().count(l) for l in np.unique(y)})
    return X, y


def load_Colon():
    name = 'Colon'
    path = '../ASUdataset/DataMat/colon.mat'
    X, y = load_hdmat(path)
    print("数据集 " + name, "样本*维度 ", X.shape, "类别：数量", {l: y.tolist().count(l) for l in np.unique(y)})
    return X, y


def load_DLBCL():
    name = 'DLBCL'
    path = '../ASUdataset/DataMat/DLBCL.mat'
    X, y = load_hdmat(path)
    print("数据集 " + name, "样本*维度 ", X.shape, "类别：数量", {l: y.tolist().count(l) for l in np.unique(y)})
    return X, y


# def load_Gait():
#     name = 'Gait'
#     path = '../ASUdataset/DataMat/PersonGaitDataSet.mat'
#     X, y = load_hdmat(path)
#     print("数据集 " + name, "样本*维度 ", X.shape, "类别：数量", {l: y.tolist().count(l) for l in np.unique(y)})
#     return X, y


def load_Leukemia():
    name = 'Leukemia'
    path = '../ASUdataset/DataMat/leukemia.mat'
    X, y = load_hdmat(path)
    print("数据集 " + name, "样本*维度 ", X.shape, "类别：数量", {l: y.tolist().count(l) for l in np.unique(y)})
    return X, y


def load_Lung():
    name = 'Lung'
    path = '../ASUdataset/DataMat/lung.mat'
    X, y = load_hdmat(path)
    print("数据集 " + name, "样本*维度 ", X.shape, "类别：数量", {l: y.tolist().count(l) for l in np.unique(y)})
    return X, y


def load_ProGE():
    name = 'Prostate_GE'
    path = '../ASUdataset/DataMat/Prostate_GE.mat'
    X, y = load_hdmat(path)
    print("数据集 " + name, "样本*维度 ", X.shape, "类别：数量", {l: y.tolist().count(l) for l in np.unique(y)})
    return X, y


def load_SRBCT():
    name = 'SRBCT'
    path = '../ASUdataset/DataMat/SRBCT.mat'
    X, y = load_hdmat(path)
    print("数据集 " + name, "样本*维度 ", X.shape, "类别：数量", {l: y.tolist().count(l) for l in np.unique(y)})
    return X, y


def load_TOX_171():
    name = 'TOX_171'
    path = '../ASUdataset/DataMat/TOX_171.mat'
    X, y = load_hdmat(path)
    print("数据集 " + name, "样本*维度 ", X.shape, "类别：数量", {l: y.tolist().count(l) for l in np.unique(y)})
    return X, y


def load_Yale():
    name = 'Yale'
    path = '../ASUdataset/DataMat/Yale.mat'
    X, y = load_hdmat(path)
    print("数据集 " + name, "样本*维度 ", X.shape, "类别：数量", {l: y.tolist().count(l) for l in np.unique(y)})
    return X, y


def load_11_Tumors():
    name = '11_Tumors'
    path = '../ASUdataset/DataMat/11_Tumors.mat'
    X, y = load_hdmat(path)
    print("数据集 " + name, "样本*维度 ", X.shape, "类别：数量", {l: y.tolist().count(l) for l in np.unique(y)})
    return X, y


if __name__ == '__main__':
    # load_Yale()
    # load_Colon()
    # load_Lung()
    # load_ProGE()
    # load_Leukemia()
    # load_Arcene()

    # load_Gait()

    load('SRBCT')
    load('Colon')
