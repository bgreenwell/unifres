import unittest
import numpy as np
import statsmodels.api as sm
from unifres import fresiduals, ffplot, fredplot
from unifres.residuals import FunctionalResidual
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for testing
import matplotlib.pyplot as plt


class TestResiduals(unittest.TestCase):
    def setUp(self):
        # Generate some synthetic data
        np.random.seed(1217)
        n = 100
        x = np.random.normal(size=n)
        mu = np.exp(1 + 0.5 * x)
        y = np.random.poisson(mu)
        self.x = x
        self.y = y
        self.n = n
        self.exog = sm.add_constant(x)

    def test_poisson_glm_function(self):
        """Test functional residuals with Poisson GLM"""
        model = sm.GLM(self.y, self.exog, family=sm.families.Poisson()).fit()
        res = fresiduals(model, type="function")

        self.assertEqual(len(res), len(self.y))
        self.assertIsInstance(res[0], FunctionalResidual)

        # Test that we can call CDF on the distributions
        test_val = res[0].cdf(0.5)
        self.assertGreaterEqual(test_val, 0)
        self.assertLessEqual(test_val, 1)

    def test_poisson_glm_surrogate(self):
        """Test surrogate residuals with Poisson GLM"""
        model = sm.GLM(self.y, self.exog, family=sm.families.Poisson()).fit()
        surr = fresiduals(model, type="surrogate")

        self.assertEqual(len(surr), len(self.y))
        self.assertTrue(np.all(surr >= 0) and np.all(surr <= 1))

    def test_poisson_glm_probscale(self):
        """Test probability-scale residuals with Poisson GLM"""
        model = sm.GLM(self.y, self.exog, family=sm.families.Poisson()).fit()
        prob = fresiduals(model, type="probscale")

        self.assertEqual(len(prob), len(self.y))
        self.assertTrue(np.all(prob >= -1) and np.all(prob <= 1))

    def test_binomial_glm(self):
        """Test residuals with Binomial GLM"""
        z = 1 - 2*self.x + np.random.logistic(size=self.n)
        y_bin = np.where(z > 0, 1, 0)
        model = sm.GLM(y_bin, self.exog, family=sm.families.Binomial()).fit()

        res = fresiduals(model, type="function")
        self.assertEqual(len(res), self.n)

        surr = fresiduals(model, type="surrogate")
        self.assertTrue(np.all(surr >= 0) and np.all(surr <= 1))

    def test_negbin_glm(self):
        """Test residuals with Negative Binomial GLM"""
        model = sm.GLM(self.y, self.exog, family=sm.families.NegativeBinomial()).fit()
        res = fresiduals(model, type="function")
        self.assertEqual(len(res), len(self.y))

    def test_negbin_discrete(self):
        """Test residuals with discrete Negative Binomial model"""
        model = sm.NegativeBinomial(self.y, self.exog).fit(disp=0)
        res = fresiduals(model, type="function")
        self.assertEqual(len(res), len(self.y))

    def test_fresiduals_with_provided_y(self):
        """Test that providing y parameter works"""
        model = sm.GLM(self.y, self.exog, family=sm.families.Poisson()).fit()

        res1 = fresiduals(model)
        res2 = fresiduals(model, y=self.y)

        # Both should produce same length results
        self.assertEqual(len(res1), len(res2))

    def test_invalid_type(self):
        """Test that invalid type raises error"""
        model = sm.GLM(self.y, self.exog, family=sm.families.Poisson()).fit()

        with self.assertRaises(ValueError):
            fresiduals(model, type="invalid")

    def test_ffplot_basic(self):
        """Test basic function-function plot"""
        model = sm.GLM(self.y, self.exog, family=sm.families.Poisson()).fit()
        ax = ffplot(model)
        self.assertIsNotNone(ax)
        plt.close()

    def test_ffplot_with_resolution(self):
        """Test ffplot with custom resolution"""
        model = sm.GLM(self.y, self.exog, family=sm.families.Poisson()).fit()
        ax = ffplot(model, resolution=50)
        self.assertIsNotNone(ax)
        plt.close()

    def test_ffplot_with_subsampling(self):
        """Test ffplot with subsampling"""
        model = sm.GLM(self.y, self.exog, family=sm.families.Poisson()).fit()
        ax = ffplot(model, n=50)
        self.assertIsNotNone(ax)
        plt.close()

    def test_ffplot_with_list_input(self):
        """Test ffplot with pre-computed residuals"""
        model = sm.GLM(self.y, self.exog, family=sm.families.Poisson()).fit()
        fres = fresiduals(model, type="function")
        ax = ffplot(fres)
        self.assertIsNotNone(ax)
        plt.close()

    def test_fredplot_kde(self):
        """Test FRED plot with KDE"""
        model = sm.GLM(self.y, self.exog, family=sm.families.Poisson()).fit()
        ax = fredplot(model, self.x, type="kde")
        self.assertIsNotNone(ax)
        plt.close()

    def test_fredplot_hex(self):
        """Test FRED plot with hexbin"""
        model = sm.GLM(self.y, self.exog, family=sm.families.Poisson()).fit()
        ax = fredplot(model, self.x, type="hex")
        self.assertIsNotNone(ax)
        plt.close()

    def test_fredplot_with_lowess(self):
        """Test FRED plot with LOWESS smoother"""
        model = sm.GLM(self.y, self.exog, family=sm.families.Poisson()).fit()
        ax = fredplot(model, self.x, lowess=True)
        self.assertIsNotNone(ax)
        plt.close()

    def test_fredplot_without_lowess(self):
        """Test FRED plot without LOWESS smoother"""
        model = sm.GLM(self.y, self.exog, family=sm.families.Poisson()).fit()
        ax = fredplot(model, self.x, lowess=False)
        self.assertIsNotNone(ax)
        plt.close()


if __name__ == '__main__':
    unittest.main()
