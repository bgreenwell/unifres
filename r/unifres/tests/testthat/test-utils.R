test_that("unifend works with binomial GLM", {
  set.seed(1217)
  n <- 100
  x <- rnorm(n)
  z <- 1 - 2*x + rlogis(n)
  y <- ifelse(z > 0, 1, 0)
  fit <- glm(y ~ x, family = binomial)

  uends <- unifend(fit)
  expect_equal(dim(uends), c(n, 2))
  expect_true(all(uends[, 1] >= 0))
  expect_true(all(uends[, 2] <= 1))
  expect_true(all(uends[, 1] <= uends[, 2]))

  # For y = 1, lower should be 1 - fitted, upper should be 1
  y1_indices <- which(y == 1)
  expect_equal(uends[y1_indices, 2], rep(1, length(y1_indices)))

  # For y = 0, lower should be 0, upper should be 1 - fitted
  y0_indices <- which(y == 0)
  expect_equal(uends[y0_indices, 1], rep(0, length(y0_indices)))
})

test_that("unifend works with Poisson GLM", {
  set.seed(1217)
  n <- 100
  x <- rnorm(n)
  mu <- exp(1 + x)
  y <- rpois(n, lambda = mu)
  fit <- glm(y ~ x, family = poisson)

  uends <- unifend(fit)
  expect_equal(dim(uends), c(n, 2))
  expect_true(all(uends[, 1] >= 0))
  expect_true(all(uends[, 2] <= 1))
  expect_true(all(uends[, 1] <= uends[, 2]))
})

test_that("unifend handles models without y in object", {
  set.seed(1217)
  n <- 50
  x <- rnorm(n)
  y <- rbinom(n, 1, plogis(x))
  fit <- glm(y ~ x, family = binomial, y = FALSE)

  expect_error(unifend(fit), "No response vector")
  expect_no_error(unifend(fit, y = y))
})

test_that("expand function works correctly", {
  endpoints <- cbind(
    lwr = c(0.1, 0.3, 0.5),
    upr = c(0.2, 0.4, 0.6)
  )

  expanded <- unifres:::expand(endpoints, resolution = 5, flat = FALSE)
  expect_equal(dim(expanded), c(3, 5))
  expect_equal(expanded[1, 1], 0.1)
  expect_equal(expanded[1, 5], 0.2)

  expanded_flat <- unifres:::expand(endpoints, resolution = 5, flat = TRUE)
  expect_equal(length(expanded_flat), 15)
  expect_equal(expanded_flat[1], 0.1)
  expect_equal(expanded_flat[5], 0.2)
})

test_that("unifend with mgcv::gam models", {
  skip_if_not_installed("mgcv")

  set.seed(1217)
  n <- 200
  x <- rnorm(n)
  mu <- exp(1 + x + 0.5*x^2)
  y <- rpois(n, lambda = mu)
  fit <- mgcv::gam(y ~ s(x), family = poisson)

  uends <- unifend(fit)
  expect_equal(dim(uends), c(n, 2))
  expect_true(all(uends[, 1] >= 0))
  expect_true(all(uends[, 2] <= 1))
  expect_true(all(uends[, 1] <= uends[, 2]))
})

test_that("unifend with VGAM ordinal models", {
  skip_if_not_installed("VGAM")

  set.seed(1217)
  n <- 200
  x <- rnorm(n)
  eta <- 1 + 2*x
  probs <- cbind(
    plogis(-2 - eta),
    plogis(-1 - eta) - plogis(-2 - eta),
    plogis(0 - eta) - plogis(-1 - eta),
    1 - plogis(0 - eta)
  )
  y <- apply(probs, 1, function(p) sample(1:4, 1, prob = p))

  fit <- VGAM::vglm(factor(y) ~ x, family = VGAM::cumulative(parallel = TRUE))

  uends <- unifend(fit)
  expect_equal(dim(uends), c(n, 2))
  expect_true(all(uends[, 1] >= 0))
  expect_true(all(uends[, 2] <= 1))
  expect_true(all(uends[, 1] <= uends[, 2]))
})

test_that("unifend with zero-inflated Poisson", {
  skip_if_not_installed("pscl")
  skip_if_not_installed("VGAM")

  set.seed(1217)
  n <- 200
  x <- rnorm(n)
  mu <- exp(1 + x)
  pi <- plogis(-1 + 0.5*x)
  y <- ifelse(rbinom(n, 1, pi) == 1, 0, rpois(n, mu))

  fit <- pscl::zeroinfl(y ~ x | x, dist = "poisson")

  uends <- unifend(fit)
  expect_equal(dim(uends), c(n, 2))
  expect_true(all(uends[, 1] >= 0))
  expect_true(all(uends[, 2] <= 1))
  expect_true(all(uends[, 1] <= uends[, 2]))
})

test_that("unifend errors with unsupported family", {
  set.seed(1217)
  n <- 50
  x <- rnorm(n)
  y <- rgamma(n, shape = 2, rate = 1)
  fit <- glm(y ~ x, family = Gamma)

  expect_error(unifend(fit), "Unsupported family")
})
