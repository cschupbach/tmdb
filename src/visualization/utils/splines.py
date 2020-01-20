import numpy as np


def M_splines_basis(x, M, K):
    dof = K + M
    xi = np.linspace(np.min(x), np.max(x), K+2)[1:-1]
    H = np.zeros((len(x), dof))
    for j in range(M):
        H[:,j] = np.power(x, j)
    for k in range(K):
        H[:,M+k] = np.where((x - xi[k]) > 0, np.power(x - xi[k], M-1), 0)

    return H


def M_splines(x, M=4, K=8):
    H = splines_basis(x, M, K)
    bhat = np.linalg.inv(H.T@H)@(H.T@y)
    yhat = H@bhat

    return yhat


def plot_mean_function(x, y, yhat):
    plt.figure(figsize=(10,6))
    plt.scatter(x, y, s=20, label='Mean sample signal')
    plt.plot(x, yhat, c='red', alpha=0.7, label='Estimated mean function')
    plt.xlabel(r'$x$')
    plt.ylabel(r'$y$')
    plt.legend(fontsize=14)
    plt.show()

    return None
