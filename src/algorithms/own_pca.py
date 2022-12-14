import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as SLA
import itertools

data_path = '../data/processed/'

plt.rcParams["image.cmap"] = "tab20"
# Para cambiar el ciclo de color por defecto en Matplotlib
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.cm.tab20.colors)
#Set_ColorsIn(plt.cm.Set2.colors)
colors = plt.cm.tab20.colors

class OPCA():
    def __init__(self, 
                 data: np.array,
                 data_name: str):
        self.data = data
        self.data_name = data_name
        self.n_instances = data.shape[0] 
        self.n_features = data.shape[1]
        self.means = None
        self.cov_mat = None
        self.eigenvalues = None
        self.eigenvectors = None
        self.transformed_data = None
        self.reconstructed_data = None
        self.explained_variance_ratio = None
        self.feat_vec = None
        self.U_eigenvalues = None
        self.U_eigenvectors = None

    def fit(self, axes = 2):
        # Computing mean of each axis(feature) in the data
        self.means = self.data.mean(0)
        # Substracting each data point from the means
        sub_means = np.subtract(self.data,self.means)
        # Computing covariance matrix 
        self.cov_mat = self.covariance_matrix(sub_means)
        # Getting eigenvalues and eigenvectors
        self.eigenvalues, self.eigenvectors = SLA.eig(self.cov_mat, left = True, right = False)
        self.eigenvalues = self.eigenvalues.astype(float)
        self.U_eigenvalues, self.U_eigenvectors = self.eigenvalues.copy(), self.eigenvectors.copy()
        # Descending ordering to eigenvalues
        order = np.argsort(self.eigenvalues)[::-1]
        self.eigenvalues = self.eigenvalues[order]
        # Ordering eigenvectors according to eigenvalues
        self.eigenvectors = self.eigenvectors.T[order]
        self.eigenvectors = np.array([-self.eigenvectors[i] if i%2 != 0 else self.eigenvectors[i] for i in range(len(self.eigenvectors))]).astype(float)
        # Choosing number of components of the feature vector
        self.feat_vec = self.eigenvectors[:axes]
        # Transforming the data
        self.transformed_data = (self.feat_vec.dot(sub_means.T))
        # Reconstructing to the original data
        self.reconstructed_data = self.transformed_data.T.dot(self.feat_vec)+self.means
        self.explained_variance_ratio = self.eigenvalues / self.eigenvalues.sum()
        return -self.transformed_data.T

    def visualize(self, labels, axes=[0, 1, 2], figsize=(10, 10), original=True, save=None):
        if original == 'Original':
            data = self.data
            title = 'Original Data'
        elif original == 'Reconstructed':
            data = self.reconstructed_data
            title ='Reconstructed Data'
        else:
            data = self.transformed_data.T
            title = 'Transformed Data'

        values = []
        for i in axes:
            values.append(data[:, i])
        values = np.array(values).T
        dims = len(axes)


        if dims == 4:
            self.scatter_4D(values, labels, axes, title+ ' Own PCA', self.data_name, figsize, save)
        elif dims == 3:
            self.scatter_3D(values, labels, axes, title+ ' Own PCA', self.data_name, figsize, save)
        elif dims == 2:
            self.scatter_2D(values, labels, axes, title+ ' Own PCA', self.data_name, figsize, save)

        if save:
            plt.savefig(save)
        
    def scree_plot(self, save=False):
        plt.plot(np.cumsum(self.explained_variance_ratio), marker='.', color=colors[1])
        plt.bar(list(range(0, self.n_features)), self.explained_variance_ratio, color=colors[2])
        plt.title('Explained Variance Own PCA')
        plt.xlabel('Number of Components')
        plt.ylabel('Variance (%)')

        if save:
            plt.savefig(save + 'scree_plot_{}.pdf'.format(self.data_name))

        plt.show()


    @staticmethod
    def covariance_matrix(sub_means):
        # Getting the shape of the matrix
        cov = np.zeros((sub_means.shape[1], sub_means.shape[1]))
        # Computing all possible features combinations
        c = list(itertools.product(sub_means.T,repeat = 2))
        s = int(sub_means.shape[1])
        # Computing the matrix
        for k,i in enumerate(c):
            cov[(-(k%s-(k))//s,k%s)] = (i[0]*i[1]).sum()/(sub_means.shape[0]-1)
        return cov

    @staticmethod
    def scatter_4D(data, labels, axes, title, data_name, figsize=(10, 10), save=None):
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(data[:, 0], data[:, 1], data[:, 2], c=labels, s=data[:, 3] * 10)
        ax.set_title(title)
        ax.set_xlabel(axes[0])
        ax.set_ylabel(axes[1])
        ax.set_zlabel(axes[2])

        if save:
            ax.savefig(save + 'scatter_plot_4D_{}.pdf'.format(title))
        
        plt.show()


    @staticmethod
    def scatter_3D(data, labels, axes, title, data_name, figsize=(10, 10), save=None):
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(data[:, 0], data[:, 1], data[:, 2], c=labels, s=15)
        ax.set_title(title)
        ax.set_xlabel(axes[0])
        ax.set_ylabel(axes[1])
        ax.set_zlabel(axes[2])

        if save: 
            fig.savefig(save + 'scatter_plot_3D_{}.pdf'.format(title))
        
        plt.show()


    @staticmethod
    def scatter_2D(data, labels, axes, title, data_name, figsize=(10, 10), save=None):
        fig = plt.figure(figsize=figsize)
        plt.scatter(data[:, 0], data[:, 1], c=labels)#, cmap='cool' )
        plt.title(title)
        plt.xlabel(axes[0])
        plt.ylabel(axes[1])

        if save:
            plt.savefig(save + 'scatter_plot_2D_{}.pdf'.format(title))

        plt.show()


