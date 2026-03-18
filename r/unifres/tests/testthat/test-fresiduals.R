test_that("fresiduals works with binomial GLM", {
  set.seed(1217)
  n <- 100
  x <- rnorm(n)
  z <- 1 - 2*x + rlogis(n)
  y <- ifelse(z > 0, 1, 0)
  fit <- glm(y ~ x, family = binomial)

  # Test function type
  fres <- fresiduals(fit, type = "function")
  expect_s3_class(fres, "unifres")
  expect_equal(length(fres), n)
  expect_true(all(sapply(fres, is.function)))

  # Test that functions return valid probabilities
  test_vals <- fres[[1]](seq(0, 1, by = 0.1))
  expect_true(all(test_vals >= 0 & test_vals <= 1))

  # Test surrogate type
  surr <- fresiduals(fit, type = "surrogate", link.scale = FALSE)
  expect_equal(length(surr), n)
  expect_true(all(surr >= 0 & surr <= 1))

  # Test probscale type
  prob <- fresiduals(fit, type = "probscale")
  expect_equal(length(prob), n)
  expect_true(all(prob >= -1 & prob <= 1))
})

test_that("fresiduals works with Poisson GLM", {
  set.seed(1217)
  n <- 100
  x <- rnorm(n)
  mu <- exp(1 + x)
  y <- rpois(n, lambda = mu)
  fit <- glm(y ~ x, family = poisson)

  fres <- fresiduals(fit, type = "function")
  expect_s3_class(fres, "unifres")
  expect_equal(length(fres), n)

  surr <- fresiduals(fit, type = "surrogate", link.scale = FALSE)
  expect_equal(length(surr), n)
  expect_true(all(surr >= 0 & surr <= 1))
})

test_that("fresiduals works with quasi-Poisson", {
  set.seed(1217)
  n <- 100
  x <- rnorm(n)
  mu <- exp(1 + x)
  y <- rpois(n, lambda = mu)
  fit <- glm(y ~ x, family = quasipoisson)

  fres <- fresiduals(fit)
  expect_s3_class(fres, "unifres")
  expect_equal(length(fres), n)
})

test_that("fresiduals handles matrix input", {
  endpoints <- cbind(
    lwr = c(0.1, 0.2, 0.3),
    upr = c(0.4, 0.5, 0.6)
  )

  fres <- fresiduals(endpoints, type = "function")
  expect_s3_class(fres, "unifres")
  expect_equal(length(fres), 3)

  surr <- fresiduals(endpoints, type = "surrogate", link.scale = FALSE)
  expect_equal(length(surr), 3)
  expect_true(all(surr >= 0.1 & surr <= 0.6))

  prob <- fresiduals(endpoints, type = "probscale")
  expect_equal(length(prob), 3)
})

test_that("fresiduals errors with invalid matrix", {
  bad_matrix <- matrix(1:9, nrow = 3, ncol = 3)
  expect_error(fresiduals(bad_matrix), "exactly two columns")
})

test_that("fresiduals surrogate with link.scale works", {
  set.seed(1217)
  n <- 50
  x <- rnorm(n)
  z <- 1 - 2*x + rlogis(n)
  y <- ifelse(z > 0, 1, 0)
  fit <- glm(y ~ x, family = binomial)

  surr_prob <- fresiduals(fit, type = "surrogate", link.scale = FALSE)
  surr_link <- fresiduals(fit, type = "surrogate", link.scale = TRUE)

  expect_equal(length(surr_prob), n)
  expect_equal(length(surr_link), n)
  expect_false(identical(surr_prob, surr_link))
})
