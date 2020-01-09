from abc import ABC, abstractmethod
import numpy as np


class Optimizer(ABC):
    @abstractmethod
    def allocate(self, mu: np.array, cov: np.array) -> np.array:
        """
        Create an optimal portfolio allocation given the expected returns vector and covariance matrix. See section 4.3
        of the "A Robust Estimator of the Efficient Frontier" paper.
        @param mu: Expected return vector
        @param cov: Expected covariance matrix
        @return Vector of weights
        """
        pass

    @abstractmethod
    @property
    def name(self) -> str:
        """
        Name of this optimizer. The name will be displayed in the MCOS results DataFrame.
        """
        pass