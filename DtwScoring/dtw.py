import numpy as np
import scipy.spatial
from numba import jit
import matplotlib.pyplot as plt


def compute_cost_matrix(X, Y, metric='euclidean'):
    """Compute the cost matrix of two feature sequences
    Args:
        X: Sequence 1
        Y: Sequence 2
        metric: Cost metric, a valid strings for scipy.spatial.distance.cdist
    Returns:
        C: Cost matrix
    """
    X, Y = np.atleast_2d(X, Y)
    C = scipy.spatial.distance.cdist(X.T, Y.T, metric=metric)
    return C

@jit(nopython=True)
def compute_accumulated_cost_matrix(C):
    """Compute the accumulated cost matrix given the cost matrix

    Notebook: C3/C3S2_DTWbasic.ipynb

    Args:
        C: cost matrix

    Returns:
        D: Accumulated cost matrix
    """
    N = C.shape[0]
    M = C.shape[1]
    D = np.zeros((N, M))
    D[0, 0] = C[0, 0]
    for n in range(1, N):
        D[n, 0] = D[n-1, 0] + C[n, 0]
    for m in range(1, M):
        D[0, m] = D[0, m-1] + C[0, m]
    for n in range(1, N):
        for m in range(1, M):
            D[n, m] = C[n, m] + min(D[n-1, m], D[n, m-1], D[n-1, m-1])
    return D


@jit(nopython=True)
def compute_optimal_warping_path(D):
    """Compute the warping path given an accumulated cost matrix
    Args:
        D: Accumulated cost matrix

    Returns
        P: Warping path (list of index pairs)
    """
    N = D.shape[0]
    M = D.shape[1]
    n = N - 1
    m = M - 1
    P = [(n, m)]
    while n > 0 or m > 0:
        if n == 0:
            cell = (0, m - 1)
        elif m == 0:
            cell = (n - 1, 0)
        else:
            val = min(D[n - 1, m - 1], D[n - 1, m], D[n, m - 1])
            if val == D[n - 1, m - 1]:
                cell = (n - 1, m - 1)
            elif val == D[n - 1, m]:
                cell = (n - 1, m)
            else:
                cell = (n, m - 1)
        P.append(cell)
        (n, m) = cell
    P.reverse()
    return np.array(P)




# P = np.array(P)
# plt.figure(figsize=(9, 3))
# plt.subplot(1, 2, 1)
# plt.imshow(C, cmap='gray_r', origin='lower', aspect='equal')
# plt.plot(P[:, 1], P[:, 0], marker='o', color='r')
# plt.clim([0, np.max(C)])
# plt.colorbar()
# plt.title('$C$ with optimal warping path')
# plt.xlabel('Sequence Y')
# plt.ylabel('Sequence X')
#
# plt.subplot(1, 2, 2)
# plt.imshow(D, cmap='gray_r', origin='lower', aspect='equal')
# plt.plot(P[:, 1], P[:, 0], marker='o', color='r')
# plt.clim([0, np.max(D)])
# plt.colorbar()
# plt.title('$D$ with optimal warping path')
# plt.xlabel('Sequence Y')
# plt.ylabel('Sequence X')
#
# plt.tight_layout()