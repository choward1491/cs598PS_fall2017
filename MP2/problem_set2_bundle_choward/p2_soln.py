# Author : Christian Howard
# Purpose: To tackle Problem 2 in Homework 2

# import useful libraries/modules
import myml.factorizations      as myfac
import myml.images              as myimg
import numpy                    as np
import scipy.io                 as sio
import matplotlib.pyplot        as plot
import sklearn.decomposition    as skd


if __name__ == '__main__':

    # load image dataset
    digits_mat = sio.loadmat('digits.mat')

    # get the image dataset
    D = digits_mat['d']
    (d, num_images) = D.shape

    # define the number of features for this problem
    num_features = 36

    # compute mean of images
    mu_i = np.matmul(D, np.ones((num_images, 1)) / num_images)

    # subtract mean from data
    Dn = D - mu_i

    # Perform PCA from zero-mean form of data
    (W1, W1pi, sv) = myfac.pca(Dn, num_features)

    # compute lower dimensional measurements
    Z = np.matmul(W1, Dn)

    # Perform ICA on lower dimensional measurements
    useLibraryICA = True
    if useLibraryICA:
        ica_obj = skd.FastICA(random_state=17)
        ica_obj.fit(Z.T)
        W2 = np.matmul(ica_obj.components_, W1)
    else:
        (Minv, M) = myfac.ica(Z, random_seed=17, eps=1e-8)
        W2 = np.matmul(Minv, W1)
    W2pi = np.linalg.pinv(W2)

    # Perform NMF from zero-mean form of data
    nmf_obj = skd.NMF(n_components=num_features, random_state=17)
    H = nmf_obj.fit_transform(np.abs(Dn).T).T
    W3 = nmf_obj.components_.T


    # plot the feature sets for each of the methods
    fg1 = plot.figure()
    ax1 = fg1.add_subplot(111)
    img_set1 = myimg.plotImageFeatures(W1pi, (28, 28), (6, 6))
    im  = ax1.imshow(img_set1)
    fg1.colorbar(im)
    fg1.savefig('p2/pca_features_digits.png')

    fg2 = plot.figure()
    ax2 = fg2.add_subplot(111)
    img_set2 = myimg.plotImageFeatures(W2pi, (28, 28), (6, 6))
    im  = ax2.imshow(img_set2)
    fg2.colorbar(im)
    fg2.savefig('p2/ica_features_digits.png')


    fg3 = plot.figure()
    ax3 = fg3.add_subplot(111)
    img_set3 = myimg.plotImageFeatures(W3, (28, 28), (6, 6))
    im  = ax3.imshow(img_set3)
    fg3.colorbar(im)
    fg3.savefig('p2/nmf_features_digits.png')


    #plot.show()