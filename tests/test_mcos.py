import pytest
import numpy as np
import pandas as pd
from numpy.testing import assert_almost_equal
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import sample_cov

from mcos.covariance_transformer import DeNoiserCovarianceTransformer
from mcos.error_estimator import ExpectedOutcomeErrorEstimator, SharpeRatioErrorEstimator, VarianceErrorEstimator
from mcos.mcos import simulate_optimizations, simulate_optimizations_from_price_history
from mcos.observation_simulator import MuCovObservationSimulator, MuCovLedoitWolfObservationSimulator,\
    MuCovJackknifeObservationSimulator

from mcos.optimizer import HRPOptimizer, MarkowitzOptimizer, NCOOptimizer, RiskParityOptimizer


prices_df = pd.read_csv('tests/stock_prices.csv', parse_dates=True, index_col='date')
mu = mean_historical_return(prices_df).values
cov = sample_cov(prices_df).values


@pytest.mark.parametrize('simulator, estimator, transformers, expected_mean, expected_stdev', [
    (
        MuCovObservationSimulator(mu, cov, n_observations=5),
        ExpectedOutcomeErrorEstimator(),
        [DeNoiserCovarianceTransformer()],
        np.array([0.07580845, 0.05966212, -0.02893896, 0.0085226]),
        np.array([0.03445259, 0.03214469, 0.01724587, 0.01244282])
    ),
    (
        MuCovObservationSimulator(mu, cov, n_observations=5),
        ExpectedOutcomeErrorEstimator(),
        [],
        np.array([0.05043029, -0.0761952, -0.03200537, -0.00413669]),
        np.array([0.05422127, 0.25850676, 0.0196157, 0.01376204])
    ),
    (
        MuCovObservationSimulator(mu, cov, n_observations=5),
        SharpeRatioErrorEstimator(),
        [DeNoiserCovarianceTransformer()],
        np.array([0.44088768, 0.32030003, -0.26876011, 0.15122857]),
        np.array([0.156086, 0.16563697, 0.13853157, 0.27771979])
    ),
    (
        MuCovObservationSimulator(mu, cov, n_observations=5),
        SharpeRatioErrorEstimator(),
        [],
        np.array([0.2390896, -0.10741015, -0.24046168, -0.0070365]),
        np.array([0.26834958, 0.171923, 0.16837215, 0.14896394])
    ),
    (
        MuCovObservationSimulator(mu, cov, n_observations=5),
        VarianceErrorEstimator(),
        [DeNoiserCovarianceTransformer()],
        np.array([0.03447771, 0.03842862, 0.01002529, 0.00207496]),
        np.array([0.01720998, 0.0161673, 0.00338963, 0.00068379])
    ),
    (
        MuCovObservationSimulator(mu, cov, n_observations=5),
        VarianceErrorEstimator(),
        [],
        np.array([0.05416531, 3.25027156, 0.02014813, 0.00666281]),
        np.array([0.00867717, 2.04014303, 0.00424525, 0.00419053])
    ),
    (
        MuCovLedoitWolfObservationSimulator(mu, cov, n_observations=5),
        ExpectedOutcomeErrorEstimator(),
        [DeNoiserCovarianceTransformer()],
        np.array([0.05183939, 0.07230958, -0.02051239, -0.0086959]),
        np.array([0.00979491, 0.00997131, 0.00640547, 0.00077058])
    ),
    (
        MuCovLedoitWolfObservationSimulator(mu, cov, n_observations=5),
        ExpectedOutcomeErrorEstimator(),
        [],
        np.array([0.05010366, 0.05885478, -0.0375485, -0.00431366]),
        np.array([0.02262029, 0.02348383, 0.00511152, 0.01081385])
    ),
    (
        MuCovLedoitWolfObservationSimulator(mu, cov, n_observations=5),
        SharpeRatioErrorEstimator(),
        [DeNoiserCovarianceTransformer()],
        np.array([0.52634486, 0.58680348, -0.44668879, -0.34823549]),
        np.array([0.12738562, 0.08301391, 0.15521816, 0.02176522])
    ),
    (
        MuCovLedoitWolfObservationSimulator(mu, cov, n_observations=5),
        SharpeRatioErrorEstimator(),
        [],
        np.array([0.37685555, 0.35742078, -0.46377915, -0.0650202]),
        np.array([0.17793642, 0.13892987, 0.03466091, 0.2445361])
    ),
    (
        MuCovLedoitWolfObservationSimulator(mu, cov, n_observations=5),
        VarianceErrorEstimator(),
        [DeNoiserCovarianceTransformer()],
        np.array([0.01001657, 0.01522694, 0.00218297, 0.00063938]),
        np.array([0.00117849, 0.00113607, 0.00020851, 0.00015752])
    ),
    (
        MuCovLedoitWolfObservationSimulator(mu, cov, n_observations=5),
        VarianceErrorEstimator(),
        [],
        np.array([0.01897399, 0.02695813, 0.00654766, 0.00203981]),
        np.array([0.00319618, 0.00262264, 0.00095974, 0.00060647])
    ),
    (
        MuCovJackknifeObservationSimulator(mu, cov, n_observations=5),
        ExpectedOutcomeErrorEstimator(),
        [DeNoiserCovarianceTransformer()],
        np.array([0.0758128, 0.06085414, -0.02948377, -0.00852103]),
        np.array([0.03445484, 0.03214721, 0.01652253, 0.01244531])
    ),
    (
        MuCovJackknifeObservationSimulator(mu, cov, n_observations=5),
        ExpectedOutcomeErrorEstimator(),
        [],
        np.array([0.0487412, 10.21950872, -0.03201583, -0.00414127]),
        np.array([0.05596715, 13.12656593, 0.01962365, 0.01365775])
    ),
    (
        MuCovJackknifeObservationSimulator(mu, cov, n_observations=5),
        SharpeRatioErrorEstimator(),
        [DeNoiserCovarianceTransformer()],
        np.array([0.44420332, 0.34013247, -0.27352751, 0.1512315]),
        np.array([0.15609054, 0.18039154, 0.13119882, 0.27774587])
    ),
    (
        MuCovJackknifeObservationSimulator(mu, cov, n_observations=5),
        SharpeRatioErrorEstimator(),
        [],
        np.array([0.2309123, 0.32883471, -0.2404617, -0.00704547]),
        np.array([0.27568471, 0.06322784, 0.16837224, 0.14896722])
    ),
    (
        MuCovJackknifeObservationSimulator(mu, cov, n_observations=5),
        VarianceErrorEstimator(),
        [DeNoiserCovarianceTransformer()],
        np.array([0.03448147, 0.03740596, 0.01034748, 0.00207010]),
        np.array([0.01721475, 0.01784114, 0.00298154, 0.00068010])
    ),
    (
        MuCovJackknifeObservationSimulator(mu, cov, n_observations=5),
        VarianceErrorEstimator(),
        [],
        np.array([0.05147521, 1706.73921323, 0.0201481, 0.0066681]),
        np.array([0.00792436, 2394.21167618, 0.0042452, 0.0041945])
    )
])
def test_simulate_observations(simulator, estimator, transformers, expected_mean, expected_stdev):
    np.random.seed(0)  # use a random seed for predictable numbers

    df = simulate_optimizations(simulator,
                                n_sims=3,
                                optimizers=[MarkowitzOptimizer(), NCOOptimizer(), HRPOptimizer(),
                                            RiskParityOptimizer()],
                                error_estimator=estimator,
                                covariance_transformers=transformers)

    assert_almost_equal(df['mean'].values, expected_mean, decimal=1)
    assert_almost_equal(df['stdev'].values, expected_stdev, decimal=1)


def test_simulate_observations_price_history():
    np.random.seed(0)

    df = simulate_optimizations_from_price_history(prices_df,
                                                  'MuCovLedoitWolf',
                                                  n_observations=3,
                                                  n_sims=3,
                                                  optimizers=[MarkowitzOptimizer(), NCOOptimizer(), HRPOptimizer(),
                                                              RiskParityOptimizer()],
                                                  error_estimator=ExpectedOutcomeErrorEstimator(),
                                                  covariance_transformers=[DeNoiserCovarianceTransformer()])

    assert_almost_equal(df['mean'].values, np.array([0.0467513, 0.0676277, -0.0181564, -0.0078399]))
    assert_almost_equal(df['stdev'].values, np.array([0.0386170, 0.0372161, 0.0098585, 0.00666344]))


