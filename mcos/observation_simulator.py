import numpy as np
from abc import abstractmethod, ABC
from sklearn.covariance import LedoitWolf


class AbstractObservationSimulator(ABC):

    @abstractmethod
    def simulate(self) -> (np.array, np.array):
        """
        Draws empirical means and covariances. See section 4.1 of the "A Robust Estimator of the Efficient Frontier"
        paper.
        :param n_observations: number of observations
        @return: Tuple of expected return vector and covariance matrix
        """
        pass


class MuCovLedoitWolfObservationSimulator(AbstractObservationSimulator):

    def __init__(self, mu: np.array, cov: np.array, n_observations: int):
        self.mu = mu
        self.cov = cov
        self.n_observations = n_observations

    def simulate(self) -> (np.array, np.array):
        x = np.random.multivariate_normal(self.mu.flatten(), self.cov, size=self.n_observations)
        return x.mean(axis=0).reshape(-1, 1), LedoitWolf().fit(x).covariance_


class MuCovObservationSimulator(AbstractObservationSimulator):

    def __init__(self, mu: np.array, cov: np.array, n_observations: int):
        self.mu = mu
        self.cov = cov
        self.n_observations = n_observations

    def simulate(self) -> (np.array, np.array):
        x = np.random.multivariate_normal(self.mu.flatten(), self.cov, size=self.n_observations)
        return x.mean(axis=0).reshape(-1, 1), np.cov(x, rowvar=False)


class MuCovJackknifeObservationSimulator(AbstractObservationSimulator):

    def __init__(self, mu: np.array, cov: np.array, n_observations: int):
        self.mu = mu
        self.cov = cov
        self.n_observations = n_observations

    def simulate(self) -> (np.array, np.array):
        x = np.random.multivariate_normal(self.mu.flatten(), self.cov, size=self.n_observations)

        x_prime = []

        for i in range(len(x)):
            x_prime.append((np.sum(x, axis=0) - x[i]) / (len(x)-1))

        return np.asarray(x_prime).mean(axis=0).reshape(-1, 1), np.cov(np.asarray(x_prime), rowvar=False)

