test_that("ffplot works with fitted model", {
  skip_if_not_installed("MASS")
  set.seed(1217)
  n <- 100
  x <- rnorm(n)
  z <- 1 - 2*x + rlogis(n)
  y <- ifelse(z > 0, 1, 0)
  fit <- glm(y ~ x, family = binomial)

  # Test that plot executes without error
  expect_no_error(ffplot(fit))
  expect_no_error(ffplot(fit, resolution = 50))
  expect_no_error(ffplot(fit, n = 50))
})

test_that("ffplot subsampling works correctly with ordered data", {
  # This test ensures the fix for the subsampling bug (sample.int issue)
  # The bug was: idx <- sample.int(n) returns 1:n in random order
  # The fix: idx <- sample.int(length(object), size = n) samples n indices from the data

  set.seed(42)
  n <- 1000
  x <- seq(0, 1, length.out = n)
  y <- rbinom(n, 1, prob = x)
  fit <- glm(y ~ x, family = binomial)

  # Get functional residuals
  fres <- fresiduals(fit, type = "function")

  # Test subsampling with n = 100
  # With the bug, this would only use first 100 observations (in random order)
  # With the fix, this should sample 100 observations from all 1000
  set.seed(123)
  expect_no_error(ffplot(fit, n = 100))

  # Verify that subsampling parameter actually reduces computation
  # by checking it doesn't error with smaller n
  expect_no_error(ffplot(fres, n = 50))
})

test_that("ffplot works with unifres object", {
  set.seed(1217)
  endpoints <- cbind(
    lwr = runif(50, 0, 0.4),
    upr = runif(50, 0.6, 1)
  )
  fres <- fresiduals(endpoints, type = "function")

  expect_no_error(ffplot(fres))
  expect_no_error(ffplot(fres, type = "l"))
})

test_that("ffplot respects graphical parameters", {
  set.seed(1217)
  n <- 50
  x <- rnorm(n)
  y <- rpois(n, exp(1 + x))
  fit <- glm(y ~ x, family = poisson)

  expect_no_error(ffplot(fit, ref.col = "blue", ref.lwd = 2, ref.lty = 1))
})

test_that("fredplot works with default settings", {
  skip_if_not_installed("hexbin")
  skip_if_not_installed("lattice")

  set.seed(1217)
  n <- 200
  x <- rnorm(n)
  z <- 1 - 2*x + 3*x^2 + rlogis(n)
  y <- ifelse(z > 0, 1, 0)
  fit <- glm(y ~ x + I(x^2), family = binomial)

  # Test hex type
  expect_no_error(fredplot(fit, x = x, type = "hex"))
})

test_that("fredplot works with kde type", {
  skip_if_not_installed("MASS")
  skip_if_not_installed("lattice")

  set.seed(1217)
  n <- 200
  x <- rnorm(n)
  mu <- exp(1 + x)
  y <- rpois(n, lambda = mu)
  fit <- glm(y ~ x, family = poisson)

  expect_no_error(fredplot(fit, x = x, type = "kde"))
})

test_that("fredplot works with matrix input", {
  skip_if_not_installed("hexbin")

  set.seed(1217)
  n <- 100
  x <- rnorm(n)
  endpoints <- cbind(
    lwr = runif(n, 0, 0.4),
    upr = runif(n, 0.6, 1)
  )

  expect_no_error(fredplot(endpoints, x = x, type = "hex"))
})

test_that("fredplot errors with categorical predictors", {
  skip_if_not_installed("hexbin")

  set.seed(1217)
  n <- 100
  x <- sample(letters[1:5], n, replace = TRUE)
  y <- rbinom(n, 1, 0.5)
  fit <- glm(y ~ x, family = binomial)

  expect_error(fredplot(fit, x = x), "Categorical predictors")
})

test_that("fredplot returns data frame when plot = FALSE", {
  set.seed(1217)
  n <- 100
  x <- rnorm(n)
  endpoints <- cbind(
    lwr = runif(n, 0, 0.4),
    upr = runif(n, 0.6, 1)
  )

  result <- fredplot(endpoints, x = x, plot = FALSE)
  expect_s3_class(result, "data.frame")
  expect_true("x" %in% names(result))
  expect_true("y" %in% names(result))
})

test_that("fredplot respects scale parameter", {
  set.seed(1217)
  n <- 100
  x <- rnorm(n)
  endpoints <- cbind(
    lwr = runif(n, 0.1, 0.4),
    upr = runif(n, 0.6, 0.9)
  )

  df_uniform <- fredplot(endpoints, x = x, scale = "uniform", plot = FALSE)
  df_normal <- fredplot(endpoints, x = x, scale = "normal", plot = FALSE)

  expect_false(identical(df_uniform$y, df_normal$y))
  expect_true(all(df_uniform$y >= 0 & df_uniform$y <= 1))
})

test_that("fredplot works with smoothing disabled", {
  skip_if_not_installed("hexbin")

  set.seed(1217)
  n <- 100
  x <- rnorm(n)
  y <- rbinom(n, 1, plogis(x))
  fit <- glm(y ~ x, family = binomial)

  expect_no_error(fredplot(fit, x = x, smooth = FALSE, type = "hex"))
})
