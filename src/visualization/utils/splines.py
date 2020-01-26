import numpy as np
import matplotlib.pyplot as plt


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


def differentiate(B):
    dB = np.zeros(np.shape(B))
    dB[1:,:] = B[1:,:]-B[:-1,:]
    dB[0,:] = dB[1,:]
    return dB


def lambda_selection(B, y, lambdas):
    B1 = differentiate(B)
    B2 = differentiate(B1)
    RSS = np.zeros(len(lambdas))
    dof = np.zeros(len(lambdas))
    for i in range(len(lambdas)):
        S = B@np.linalg.inv(B.T@B + lambdas[i]*(B2.T@B2))@B.T
        yhat = S@y
        RSS[i] = np.sum(np.power(yhat-y,2))
        dof[i] = np.trace(S.dot(S))
    return RSS, dof


def plot_lambda_curves(B, y):
    fig = plt.figure(figsize=(16,4))
    ax = [plt.subplot(1,3,i+1) for i in range(3)]
    n = 100
    min_lam, max_lam = 0, 1
    for i in range(len(ax)):
        lambdas = np.linspace(min_lam, max_lam, n)
        RSS, dof = lambda_selection(B, y, lambdas)
        GCV = (RSS/n) / np.power((1 - (dof/n)), 2)
        lamhat = lambdas[np.argmin(GCV)]
        ax[i].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        ax[i].plot(lambdas, GCV)
        ax[i].scatter(lamhat, GCV[np.argmin(GCV)], c='r', s=20, label=r'$\hat{\lambda}$')
        if i == 0:
            ax[i].set_ylabel(r'GCV($\lambda$)')
        ax[i].set_xlabel(r'$\lambda$')
        ax[i].axvline(lamhat, c='k', ls='--', lw=1, alpha=0.8)
        ax[i].text(lamhat+(0.015*(10**-i)), np.max(GCV)-(np.max(GCV)-np.min(GCV))*0.05, '$\hat{\lambda}$')
        min_lam = lamhat-(0.05*(10**-i))
        max_lam = lamhat+(0.05*(10**-i))
    return lamhat


def gaussian_kernel(u, d=1):
    return np.power(2*np.pi,-d/2) * np.exp(-np.power(u,2))


def loocv_gaus_kernel_regression(x, y, lambdas):
    n = len(x)
    m = len(lambdas)
    mse = np.zeros(m)
    for j in range(m):
        Lambda = lambdas[j]
        err = np.zeros(n)
        for i in range(n):
            x_ = np.delete(x,i)
            y_ = np.delete(y,i)
            z = gaussian_kernel((x[i] - x_) / Lambda)
            yke = np.sum(z*y_)/np.sum(z)
            err[i] = y[i]-yke
        mse[j] = np.mean(np.power(err, 2))
    return mse


# additional splines if needed
