import unittest
import numpy as np
import statsmodels.api as sm
from unifres.utils import unifend, is_fitted, expand_endpoints


class TestUtilsFunctions(unittest.TestCase):
    def setUp(self):
        np.random.seed(1217)
        self.n = 100
        self.x = np.random.normal(size=self.n)

    def test_is_fitted(self):
        """Test the is_fitted helper function"""
        # Unfitted model
        model = sm.GLM(np.zeros(10), np.ones((10, 1)), family=sm.families.Poisson())
        self.assertFalse(is_fitted(model))

        # Fitted model
        mu = np.exp(1 + 0.5 * self.x)
        y = np.random.poisson(mu)
        exog = sm.add_constant(self.x)
        fitted_model = sm.GLM(y, exog, family=sm.families.Poisson()).fit()
        self.assertTrue(is_fitted(fitted_model))

    def test_unifend_binomial(self):
        """Test unifend with binomial GLM"""
        z = 1 - 2*self.x + np.random.logistic(size=self.n)
        y = np.where(z > 0, 1, 0)
        exog = sm.add_constant(self.x)
        model = sm.GLM(y, exog, family=sm.families.Binomial()).fit()

        uends = unifend(model)

        self.assertEqual(uends.shape, (self.n, 2))
        self.assertTrue(np.all(uends[:, 0] >= 0))
        self.assertTrue(np.all(uends[:, 1] <= 1))
        self.assertTrue(np.all(uends[:, 0] <= uends[:, 1]))

        # For y = 1, upper endpoint should be 1
        self.assertTrue(np.allclose(uends[y == 1, 1], 1.0))
        # For y = 0, lower endpoint should be 0
        self.assertTrue(np.allclose(uends[y == 0, 0], 0.0))

    def test_unifend_poisson(self):
        """Test unifend with Poisson GLM"""
        mu = np.exp(1 + self.x)
        y = np.random.poisson(mu)
        exog = sm.add_constant(self.x)
        model = sm.GLM(y, exog, family=sm.families.Poisson()).fit()

        uends = unifend(model)

        self.assertEqual(uends.shape, (self.n, 2))
        self.assertTrue(np.all(uends[:, 0] >= 0))
        self.assertTrue(np.all(uends[:, 1] <= 1))
        self.assertTrue(np.all(uends[:, 0] <= uends[:, 1]))

    def test_unifend_negative_binomial_glm(self):
        """Test unifend with Negative Binomial GLM"""
        mu = np.exp(1 + 0.5 * self.x)
        y = np.random.negative_binomial(n=5, p=5/(5+mu))
        exog = sm.add_constant(self.x)
        model = sm.GLM(y, exog, family=sm.families.NegativeBinomial()).fit()

        uends = unifend(model)

        self.assertEqual(uends.shape, (self.n, 2))
        self.assertTrue(np.all(uends[:, 0] >= 0))
        self.assertTrue(np.all(uends[:, 1] <= 1))
        self.assertTrue(np.all(uends[:, 0] <= uends[:, 1]))

    def test_unifend_negative_binomial_discrete(self):
        """Test unifend with discrete Negative Binomial model"""
        mu = np.exp(1 + 0.5 * self.x)
        y = np.random.negative_binomial(n=5, p=5/(5+mu))
        exog = sm.add_constant(self.x)
        model = sm.NegativeBinomial(y, exog).fit(disp=0)

        uends = unifend(model)

        self.assertEqual(uends.shape, (self.n, 2))
        self.assertTrue(np.all(uends[:, 0] >= 0))
        self.assertTrue(np.all(uends[:, 1] <= 1))

    def test_unifend_with_provided_y(self):
        """Test that providing y parameter works"""
        mu = np.exp(1 + self.x)
        y = np.random.poisson(mu)
        exog = sm.add_constant(self.x)
        model = sm.GLM(y, exog, family=sm.families.Poisson()).fit()

        uends1 = unifend(model)
        uends2 = unifend(model, y=y)

        np.testing.assert_array_almost_equal(uends1, uends2)

    def test_unifend_invalid_model(self):
        """Test that unifend raises error for unsupported models"""
        with self.assertRaises(ValueError):
            unifend("not a model")

        with self.assertRaises(ValueError):
            unifend({"invalid": "model"})

    def test_expand_endpoints(self):
        """Test the expand_endpoints utility function"""
        endpoints = np.array([
            [0.1, 0.2],
            [0.3, 0.4],
            [0.5, 0.6]
        ])

        expanded = expand_endpoints(endpoints, resolution=5)

        self.assertEqual(len(expanded), 15)  # 3 rows * 5 resolution
        self.assertAlmostEqual(expanded[0], 0.1)
        self.assertAlmostEqual(expanded[4], 0.2)

    def test_expand_endpoints_edge_cases(self):
        """Test expand_endpoints with edge case inputs"""
        # Empty array
        empty = np.zeros((0, 2))
        self.assertEqual(len(expand_endpoints(empty)), 0)

        # Single row
        single = np.array([[0.0, 1.0]])
        self.assertEqual(len(expand_endpoints(single, resolution=2)), 2)

    def test_unifend_boundary_cases(self):
        """Test unifend with perfect predictions or boundary data"""
        # Binomial with perfect prediction (fitted = 1 or 0)
        # We'll simulate this with a small set
        y = np.array([1, 0])
        x = np.array([100, -100])
        exog = sm.add_constant(x)
        # Using Logit because GLM might struggle with perfect separation
        model = sm.Logit(y, exog).fit(disp=0)
        
        uends = unifend(model)
        # Should handle fitted values very close to 1 or 0
        self.assertEqual(uends.shape, (2, 2))
        self.assertTrue(np.all(uends >= 0) and np.all(uends <= 1))

    def test_unifend_mismatched_y(self):
        """Test unifend with mismatched y length"""
        mu = np.exp(1 + self.x)
        y = np.random.poisson(mu)
        exog = sm.add_constant(self.x)
        model = sm.GLM(y, exog, family=sm.families.Poisson()).fit()

        with self.assertRaises(ValueError):
            # Providing y with wrong length
            unifend(model, y=np.array([1, 2, 3]))


if __name__ == '__main__':
    unittest.main()
