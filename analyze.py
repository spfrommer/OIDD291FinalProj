import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D

def read_result(file):
    with open(file) as f:
        csv = f.read().replace(",", "")
        data = []
        for line in csv.splitlines():
            data.append(map(float, line.split()))
        return np.array(data)

def all_results():
    data = np.array([], dtype=np.float).reshape(0,12)
    for i in range(1, 13):
        d = read_result("data/{0}/res.csv".format(i))
        data = np.concatenate((data, d[:,1:4].transpose()), axis=0)
    return data

def plot_heatmap(data):
    column_labels = list(range(1,13))
    row_labels = ["Alba",
                  "Beta",
                  "Capita"]

    fig, axis = plt.subplots()
    heatmap = axis.pcolor(data, cmap='winter')

    axis.set_yticks(np.arange(data.shape[0])+0.5, minor=False)
    axis.set_xticks(np.arange(data.shape[1])+0.5, minor=False)

    axis.invert_yaxis()

    #axis.set_yticklabels(row_labels, minor=False)
    axis.set_xticklabels(column_labels, minor=False)

    plt.colorbar(heatmap)
    fig.show()

def plot_scatter2d(data):
    #scatter plot x - column 0, y - column 1, shown with marker o
    plt.plot(data[:, 0], data[:, 1], 'o', label = 'data')
    #create legend in case you have more than one series
    plt.legend()
    plt.show()

def plot_scatter3d(data):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = data[:, 0]
    y = data[:, 1]
    z = data[:, 2]

    ax.scatter(x, y, z, c='r', marker='o')

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    fig.show()

data = all_results()

pca = PCA(n_components=3)
fit = pca.fit_transform(data)
plot_heatmap(pca.components_)
plot_heatmap(data)
#plot_heatmap(data)
#plot_scatter2d(fit)

input()
