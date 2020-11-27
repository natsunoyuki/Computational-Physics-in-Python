import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg
np.random.seed()

# This script explores several properties of random numbers and random matrices

def exp_sampler(lambd=1):
    """
    This function samples from the exponential distribution using only the
    random.random() random number generator
    """
    # note that random.random range: 0 <= r <= 1
    x = -1.0 / lambd * np.log(np.random.random() / lambd)
    # I use the inversion technique to obtain this equation which samples
    # correctly from the exponential distribution
    return x

def exp_hist(lambd=1, nruns=10000, nbins=100):
    """
    This function generates a histogram of multiple samples from the exponential
    distribution and plots the analytical solution on with the numeric solution
    """
    result = np.linspace(1, nruns, nruns)  # empty array of length nruns for results
    for i in range(nruns):
        result[i] = exp_sampler(lambd)
        
    # generate line plot of p(x)
    x = np.linspace(0, max(result), 1000)
    y = lambd * np.exp(-lambd * x)
    
    plt.figure(figsize=(10,5))
    plt.hist(result, nbins, facecolor='b', density=1)
    plt.plot(x, y, 'r')
    plt.show()

def expmu_hist(lambd=1, nruns=10000, nbins=100):
    """
    This function generates multple subplots of histograms of the mean of the
    independent random variables sampled from the exponenential distribution.
    The histograms are plotted together with the analytical solution
    to the central limit theorem
    """
    # number of samples:
    N = np.array([5, 10, 20])
    # create a vector to hold the results
    result = np.zeros([len(N), nruns])
    for a in range(nruns):
        for b in range(len(N)):
            for c in range(N[b]):
                result[b][a] = result[b][a] + exp_sampler(lambd)
            result[b][a] = result[b][a] / float(N[b])  # prevent integer division
            
    # Plotting of the analytical result:
    x = np.linspace(-result.min(), result.max(), 1000)
    # this allows linspace to scale the values of x according to the lambd value
    mu = lambd ** -1  # analytical mean
    p = np.zeros([len(N), len(x)])
    
    plt.figure(figsize=(10,5))
    for i in range(len(N)):
        sig2 = 1.0 / (N[i] * lambd ** 2)  # analytical variance which depends on N
        p[i, :] = ((2 * np.pi * sig2) ** -0.5) * np.exp(-(x - mu) ** 2 / 2.0 * sig2 ** -1)
        plt.subplot(len(N), 1, i + 1)
        plt.hist(result[i, :], nbins, density=1)
        plt.plot(x, p[i, :])
        
    plt.show()
    # comments: as N gets larger and larger, the distribution tends to a
    # Gaussian distribution with corresponding mean and variance. This is the
    # essence of the central limit theorem.
    
def goe_eigs(N=10):
    """
    This function generates the eigenvalues from the gaussian orthogonal ensemble
    random matrices:
    """
    A = np.random.randn(N, N)
    B = 2 ** -0.5 * (A + A.T)
    D = linalg.eigvals(B)  
    D = np.real(D)
    return D

def bernoulli_eigs(N=10):
    """
    This function generates the eigenvalues from the symmetric bernoulli ensemble
    random matrices:
    """
    B = np.zeros([N, N])
    # The following fills B[i][j] and B[j][i] with either 1 or -1 with
    # equal probabilities. The resulting matrix is symmetric
    for i in range(N):
        for j in range(N):
            if i >= j & i != j:
                x = np.random.random()
                if x <= 0.5:
                    B[i][j] = 1
                    B[j][i] = 1
                else:
                    B[i][j] = -1
                    B[j][i] = -1
    D = linalg.eigvals(B)  # D = eigenvalues vector
    D = np.real(D)
    return D

def gue_eigs(N=10):
    """
    This function generates the eigenvalues from the gaussian unitary ensemble
    random matrices:
    """
    A = np.random.randn(N, N) + 1j * np.random.randn(N, N) 
    B = (2 ** -1) * (A + np.conj(A.T)) 
    D = linalg.eigvals(B)  
    D = np.real(D)
    return D

def random_matrix_hist(N=10, fun=goe_eigs, nruns=1000, nbins=50):
    """
    This function generates the histogram for an arbitrary random matrix ensemble
    """
    b = np.zeros([nruns, N]) 
    for i in range(nruns):
        b[i, :] = fun(N)  # output vector is placed into one of the rows of the result matrix
    bnorm = b * N ** -0.5  # obtain the normalised eigenvalues
    # Before passing this matrix of eigenvalues into hist(), we need to
    # reshape it into a vector:
    breshape = bnorm.reshape(np.size(bnorm), 1)  # reshape into column vector

    # To obtain eig spacing:
    DELTA = np.sort(bnorm)  # sort works row-wise i.e. sorts elements in each row only
    DELTA = np.diff(DELTA)  # diff works on the elements on each row only
    DELTA = DELTA.reshape(1, np.size(DELTA))  # reshape into a row vector
    mDELTA = np.mean(DELTA)  # obtain mean of DELTA i.e. eig spacing
    # I realise mean works faster on row rather than column vectors
    DELTA = DELTA * (mDELTA ** -1)  # divide by the mean value
    DELTA = DELTA.reshape(np.size(DELTA), 1)  # reshape back to column vector
    # for some reason hist does not accept row vectors as input, hence the need
    # for column vectors in the input of hist (at least on my computer)
    
    # PLOTTING:
    plt.subplot(2, 1, 1)  # two plots - Wigner's Semicircle and Surmise
    plt.hist(breshape, nbins, density=1)
    x = np.linspace(-2, 2, 1000)
    pw = 1.0 * (2 * np.pi) ** -1 * (4 - x ** 2) ** 0.5  # Wigner Semi Circle Law
    plt.plot(x, pw, 'r')
    delta = np.linspace(0, 3, 1000)
    fw = np.pi * delta * 0.5 * np.exp((-np.pi * delta ** 2) * 0.25)  # Wigner Surmise
    # For the GUE ensemble, the following Surmise should be used instead:
    # c.f. Wigner surmise for mixed symmetry classes in random matrix theory
    # Sebastian Schierenberg, Falk Bruckmann, and Tilo Wettig
    # fw=32*pi**-2*delta**2*exp(-4*pi**-1*delta**2)
    plt.subplot(2, 1, 2)
    plt.hist(DELTA, nbins, density=1)
    plt.plot(delta, fw, 'r')
    plt.ylim([0, 1])
    plt.xlim([0, 5])
    plt.show()
