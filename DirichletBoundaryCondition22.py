# Poisson Equation with the dirichlet boundary condition
from scipy import sparse
from scipy.sparse.linalg import spsolve
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm


def rhs(x, y):
    # Element-wise multiplication
    return 20 * np.multiply(np.cos(3*np.pi*x), np.sin(2*np.pi*y))


def bc_dirichlet(x, y, m):
    bc = np.zeros((m+1, m+1))
    bc[:, 0] = y[:, 0]**2
    bc[:, m] = np.ones((m+1, 1)).ravel()
    bc[0, :] = x[0, :]**3
    bc[m, :] = np.ones((1, m+1)).ravel()
    return bc


def generate_sparse_matrix(m):

    main_diag = 2 * np.ones((m - 1, 1)).ravel()
    off_diag = -1 * np.ones((m - 2, 1)).ravel()

    diagonals = [main_diag, off_diag, off_diag]

    b1 = sparse.diags(diagonals, [0, -1, 1], shape=(m - 1, m - 1)).toarray()
    sB = sparse.csc_matrix(b1) # compress sparse column matrix

    I = sparse.eye(m - 1, format= "csr").toarray() # create an array with one on the main diagonal and zero elsewhwere
    sI = sparse.csc_matrix(I)

    a1 = sparse.kron(sI, sB).toarray()
    a2 = sparse.kron(sB, sI).toarray()
    mat = sparse.csc_matrix(a1 + a2)

    return mat


M = 50
a = 0.0
b = 1.0

h = (b - a)/M
x1 = np.linspace(a, b, M+1)

X, Y = np.meshgrid(x1, x1)



#----- Right hand side
f = rhs(X, Y)
f = np.array(f.T)[1:M, 1:M].reshape(((M-1)*(M-1), 1))

#----- Boundary conditions
G = bc_dirichlet(X, Y, M)

#----- Rearranges matrix G into an array
g = np.zeros(((M-1)**2, 1))
g[0:M-1, 0] = G[1:M, 0]
g[(M-1)**2-M+1:M**2, 0] = G[1:M, M]
g[0:M**2:M-1, 0] = g[0:M**2:M-1, 0] + G[0, 1:M]
g[M-2:M**2:M-1, 0] = g[M-2:M**2:M-1, 0] + G[M, 1:M]

A = generate_sparse_matrix(M)

#----- Solve A*x=b --> x=A\b
U = spsolve(A, f*(h**2)+g)
U = U.reshape((M-1, M-1)).T

G[1:M, 1:M] = U

fig = plt.figure()
ax = fig.gca(projection='3d')

surf = ax.plot_surface(X, Y, G, cmap=cm.coolwarm, linewidth=0, antialiased=False)

#----- Static image
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('G')
plt.tight_layout()
ax.view_init(20, -106)
plt.show()

# #----- Rotate the axes and update
# for angle in range(0, 360):
#    ax.view_init(20, angle)
#    plt.draw()
#    plt.pause(.001)
