import numpy as np


def m_splines_basis(x, M, K):
    """Return the basis matrix for order-M splines."""
    dof = K + M
    xi = np.linspace(np.min(x), np.max(x), K+2)[1:-1]
    H = np.zeros((len(x), dof))
    for j in range(M):
        H[:,j] = np.power(x, j)
    for k in range(K):
        H[:,M+k] = np.where((x - xi[k]) > 0, np.power(x - xi[k], M-1), 0)

    return H


def m_splines(x, M=4, K=8):
    H = m_splines_basis(x, M, K)
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


def tau_knot_sequence(x, K, M):
    a = np.min(x)
    b = np.max(x)+1e-8
    t_inner = np.linspace(a, b, K+2)[1:-1]
    t_left = np.array([a]*M)
    t_right = np.array([b]*M)
    tau = np.append(t_left, t_inner)
    tau = np.append(tau, t_right)
    return tau


def b_basis(x, t, m, j):
    if m == 0:
        return 1 if t[j] <= x < t[j+1] else 0
    if t[j+m] == t[j]:
        a = 0.0
    else:
        a = (x-t[j])/(t[j+m]-t[j]) * b_basis(x, t, m-1, j)
    if t[j+m+1] == t[j+1]:
        b = 0.0
    else:
        b = (t[j+m+1] - x)/(t[j+m+1] - t[j+1]) * b_basis(x, t, m-1, j+1)
    return a + b


def b_splines_basis(x, t, m):
    n = len(t)-m
    return [b_basis(x, t, m, j) for j in range(n-1)]
