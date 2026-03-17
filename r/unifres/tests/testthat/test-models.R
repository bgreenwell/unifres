test_that("unifend handles Negative Binomial models", {
  skip_if_not_installed("MASS")
  set.seed(1217)
  n <- 100
  x <- rnorm(n)
  mu <- exp(1 + x)
  y <- rnbinom(n, mu = mu, size = 1)
  fit <- MASS::glm.nb(y ~ x)
  
  uends <- unifend(fit)
  expect_equal(dim(uends), c(n, 2))
  expect_true(all(uends[, 1] >= 0))
  expect_true(all(uends[, 2] <= 1))
  expect_true(all(uends[, 1] <= uends[, 2]))
})

test_that("unifend handles Quasi-Poisson models", {
  set.seed(1217)
  n <- 100
  x <- rnorm(n)
  mu <- exp(1 + x)
  y <- rpois(n, lambda = mu)
  fit <- glm(y ~ x, family = quasipoisson)
  
  uends <- unifend(fit)
  expect_equal(dim(uends), c(n, 2))
  expect_true(all(uends[, 1] >= 0))
  expect_true(all(uends[, 2] <= 1))
})
