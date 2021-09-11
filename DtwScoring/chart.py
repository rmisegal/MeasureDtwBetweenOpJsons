import matplotlib.pyplot as plt
import numpy as np

def compare_tow_line(X, Y, filePath):
    plt.figure(figsize=(6, 2))
    plt.plot(X, c='k', label='$Expert$')
    plt.plot(Y, c='b', label='$Patient$')
    plt.legend()
    plt.tight_layout()
    plt.title('Two line compare')
    plt.savefig(filePath)

def optimal_path(P, D, fileDir):
    plt.subplot(1, 2, 2)
    plt.imshow(D, cmap='gray_r', origin='lower', aspect='equal')
    plt.plot(P[:, 1], P[:, 0], marker='o', color='r')
    plt.clim([0, np.max(D)])
    plt.colorbar()
    plt.title('Optimal warping path')
    plt.xlabel('Patient')
    plt.ylabel('Expert') 
    plt.tight_layout()
    plt.savefig(fileDir)