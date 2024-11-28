# coding: utf-8
# coding: utf-8
"""
TL;DR Nearest Neighbors, Synthetic Dataset, Euclidean Distance.

Task: 
    1. Implement a k-nearest neighbors (KNN) classifier for two classes with a configurable number of neighbors. 
    2. Implement the accuracy metric and one other metric of your choice.
    3. Visualize the results.

Grading Criteria:
    The maximum score is 10 points. Your grade will equal the total points earned.
    
    * For KNN implementation: up to 4 points.
        - 3 points are awarded if your code works (passes the corresponding assert).
        - A fourth point is awarded if you use internal numpy functions for implementation.
        - Bonus: An additional point is available (not included in the main 10) for a unique approach in the fit method. See comments in the fit method for details.

    * For accuracy and an additional metric: 1 point each, awarded for passing the asserts.

    * For Matplotlib plots: 1 point for each well-crafted plot. This includes clear points (not overly crowded), readable labels, a plot title, legend, and labeled axes. Partial credit (0.5 points) is given if the plot contains the required data but lacks readability.

    * Significant non-compliance with PEP8: -1 point.

Important: make sure, that your code does not raise any error; otherwise I won't check your asset.

Recommendation:
    Start by examining the code from the `if __name__ == "__main__"` section, then proceed to the accuracy function and the KNN class.
"""

from typing import SupportsIndex
import numpy as np
from sklearn.metrics import classification_report, accuracy_score, f1_score


class KNN:
    """
    Class implementing the k-nearest neighbors algorithm.
    """

    def __init__(self, n_neighbors: int = 4):
        # Training data: features
        self.X_train = None

        # Training data: class labels
        self.y_train = None

        # Number of nearest neighbors
        self.n_neighbors = n_neighbors

    def fit(self, X: np.ndarray, y: SupportsIndex):
        """
        Fits the KNN model to the training data.
        In KNN, "fitting" simply involves storing the training dataset.
        """

        self.X_train = X

        self.y_train = y

        self.class_labels = np.unique(y)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predicts labels for a set of input samples.
        """

        test_reshaped = np.repeat(X, self.X_train.shape[0]).reshape(
            [X.shape[0], X.shape[1], self.X_train.shape[0]]
        )
        train_reshaped = (
            np.repeat(self.X_train, X.shape[0])
            .reshape([self.X_train.shape[0], X.shape[1], X.shape[0]])
            .T
        )

        D = np.linalg.norm((test_reshaped - train_reshaped), axis=1)

        train_classes = (
            self.y_train.repeat(X.shape[0])
            .reshape([self.y_train.shape[0], X.shape[0]])
            .T
        )
        sort_ids = np.argsort(D, axis=1)
        d_sorted = np.dstack(
            [
                np.take_along_axis(D, sort_ids, axis=1),
                np.take_along_axis(train_classes, sort_ids, axis=1),
            ]
        )

        classes_stacked = self.class_labels.repeat(
            X.shape[0] * self.n_neighbors, axis=0
        ).reshape(self.class_labels.shape[0], X.shape[0] * self.n_neighbors)
        print(classes_stacked[:, :4])

        class_counts = np.count_nonzero(
            (
                np.ndarray.flatten(d_sorted[:, : self.n_neighbors, 1])
                == classes_stacked
            ).reshape(
                self.class_labels.shape[0],
                X.shape[0],
                self.n_neighbors,
            ),
            axis=2,
        )

        # print(class_counts.shape)
        # print(classes_stacked[:, : X.shape[0]].shape)
        # print(np.argmax(class_counts, axis=0, keepdims=True).shape)
        # print(
        #     np.take_along_axis(
        #         classes_stacked[:, : X.shape[0]],
        #         np.argmax(class_counts, axis=0, keepdims=True),
        #         axis=0,
        #     )
        #     .flatten()
        #     .shape
        # )
        return np.take_along_axis(
            classes_stacked[:, : X.shape[0]],
            np.argmax(class_counts, axis=0, keepdims=True),
            axis=0,
        ).flatten()


def accuracy(labels_true: np.ndarray, labels_pred: np.ndarray) -> float:
    """
    Computes the fraction of correctly predicted labels.
    This is a simple yet imperfect measure of classification performance.
    """
    return np.count_nonzero(labels_pred == labels_true) / labels_true.shape[0]


def metric(labels_true: np.ndarray, labels_pred: np.ndarray) -> float:
    """
    Implements an additional classification metric.
    You can choose one we’ve discussed in class or come up with your own.
    """
    if labels_true.shape != labels_pred.shape:
        raise ValueError(
            f"Non-matching input arguments' shapes: got {labels_true.shape}, {labels_pred.shape}"
        )

    label_classes = np.unique(labels_true)
    labels_count = labels_true.shape[0]

    score = 0

    for label_class in label_classes:
        tp = (
            np.count_nonzero(
                np.logical_and(labels_pred == label_class, labels_true == label_class)
            )
        )
        fp = (
            np.count_nonzero(
                np.logical_and(labels_pred == label_class, labels_true != label_class)
            )
        )
        fn = (
            np.count_nonzero(
                np.logical_and(labels_pred != label_class, labels_true == label_class)
            )
        )
        
        score += 2 * tp / (2 * tp + fp + fn)

    return score / label_classes.shape[0]


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # Fix random seed for reproducibility
    np.random.seed(100)

    # Create synthetic dataset for training and testing
    means0, covs0 = [1, -1], [[7, 3], [3, 7]]
    x0, y0 = np.random.multivariate_normal(means0, covs0, 190).T

    means1, covs1 = [0, -4], [[0.1, 0.0], [0.0, 25]]
    x1, y1 = np.random.multivariate_normal(means1, covs1, 100).T

    # Visualize the data (optional)
    # plt.plot(x0, y0, 'o', color='b')
    # plt.plot(x1, y1, 'o', color='r')
    # plt.show()

    # Convert data to the appropriate format
    data0, labels0 = np.vstack([x0, y0]).T, np.zeros(len(x0))
    data1, labels1 = np.vstack([x1, y1]).T, np.ones(len(x1))

    data = np.vstack([data0, data1])
    labels = np.hstack([labels0, labels1])
    total_size = data.shape[0]
    print("Dataset shape:", data.shape, labels.shape)

    # Split dataset into 70% train and 30% test
    train_size = int(total_size * 0.7)
    indices = np.random.permutation(total_size)
    X_train, y_train = data[indices][:train_size], labels[indices][:train_size]
    X_test, y_test = data[indices][train_size:], labels[indices][train_size:]
    print("Train/test shapes:", X_train.shape, X_test.shape)

    # TODO: Loop through different values of n_neighbors (1 to 5)

    # Create KNN classifier instance
    predictor = KNN(n_neighbors=3)
    predictor.fit(X_train, y_train)
    y_pred = predictor.predict(X_test)

    # check that your accuracy is honest :^)
    print("Accuracy: %.4f [ours]" % accuracy(y_test, y_pred))
    assert (
        abs(accuracy_score(y_test, y_pred) - accuracy(y_test, y_pred)) < 1e-5
    ), "Implemented accuracy is not the same as sci-kit learn one!"

    # Check classifier performance
    assert (
        accuracy_score(y_test, y_pred) > 190.0 / 290
    ), "Your classifier is worse than the constant !"

    # Calculate additional metric and compare with library version
    print("Additional metric: %.4f [custom]" % metric(y_test, y_pred))
    assert (
        abs(metric(y_test, y_pred) - f1_score(y_test, y_pred,average="macro")) < 1e-5
    ), "Custom metric does not match sklearn metric!"

    # Convenient sklearn tool to calculate standard metrics
    print(classification_report(y_test, y_pred))

    # Matplotlib Exercise:
    # Generate three plots for the test set:
    # - Ground truth labels
    # - Predictions with n_neighbors = 1
    # - Predictions with the best n_neighbors in the range 1...5

    # Each plot should include the training data points with appropriate colors,
    # (hint: using transparency or small markers to avoid covering test points).

    # Save plots !!to current folder!! using matplotlib's `savefig`.

    # Fourth plot: Plot metrics as functions of n_neighbors.
    # - Show both metrics on one graph with distinct colors and a legend.
    # - If the scales differ, use two vertical axes.
