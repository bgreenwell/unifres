#' Compute uniform endpoints for functional residuals
#'
#' Computes the lower and upper endpoints of the functional residual intervals
#' described in Liu et al. (2025). These endpoints define the cumulative
#' distribution function (CDF) for each functional residual, which follows a
#' Uniform(0,1) distribution under correct model specification.
#'
#' @param object A fitted model object. Currently supported model types include:
#' * [glm][stats::glm] - generalized linear models from the core __stats__
#' package.
#' * [gam][mgcv::gam] - generalized additive models from the
#' [mgcv](https://cran.r-project.org/package=mgcv) package.
#' * [zeroinfl][pscl::zeroinfl] - zero-inflated Poisson (ZIP) models from the
#' [pscl](https://cran.r-project.org/package=pscl) package.
#' * [vglm][VGAM::vglm]/[vgam][VGAM::vgam] - vector generalized linear/additive
#' models (VGLMs/VGAMs) from the [VGAM](https://cran.r-project.org/package=VGAM)
#' package.
#'
#' @param y Optional response vector. If `NULL` (the default), the response is
#' extracted from the fitted model object.
#'
#' @param fill Logical indicating whether to expand discrete endpoints to cover
#' the full \eqn{[0, 1]} range. Default is `FALSE`.
#'
#' @param ... Additional optional arguments passed to methods.
#'
#' @returns A matrix with two columns: `lwr` (lower endpoint) and `upr` (upper
#' endpoint) for each observation. Each row defines the bounds of a functional
#' residual's CDF.
#'
#' @references
#' Liu, D., Lin, Z., & Zhang, H. (2025). A unified framework for residual
#' diagnostics in generalized linear models and beyond. *Journal of the American
#' Statistical Association*, 1–29.
#' \doi{10.1080/01621459.2025.2504037}
#'
#' @seealso [fresiduals()], [fredplot()], [ffplot()]
#'
#' @examples
#' # Fit a Poisson regression model
#' set.seed(42)
#' n <- 100
#' x <- rnorm(n)
#' y <- rpois(n, exp(0.5 + 0.3*x))
#' fit <- glm(y ~ x, family = poisson)
#'
#' # Compute uniform endpoints
#' endpoints <- unifend(fit)
#' head(endpoints)
#'
#' # The endpoints define the functional residual CDFs
#' # Under correct specification, each F_i should be uniform on (lwr_i, upr_i)
#'
#' @export
unifend <- function(object, y = NULL, fill = FALSE, ...) {
  UseMethod("unifend")
}


#' @export
unifend.glm <- function(object, y = NULL, ...) {

  # Extract needed components
  fam <- family(object)$family  # get family name as character string
  if (is.null(y)) {  # get response vector
    if (is.null(object$y)) {
      stop("No response vector could be found, please supply it ",
           "using the `y` argument.", call. = FALSE)
    } else {
      y <- object$y
    }
  }
  fv <- object$fitted.values  # get fitted values

  # Compute and return endpoints for function residual

  # Binomial -------------------------------------------------------------------
  if (fam %in% c("binomial", "quasibinomial")) {
    endpoints <- cbind(
      "lwr" = ifelse(y == 1, 1 - fv, 0),
      "upr" = ifelse(y == 1, 1, 1 - fv)
    )
  # Quasi-Poisson --------------------------------------------------------------
  } else if (fam == "quasipoisson") {
    phi <- summary(object)$dispersion
    if (phi > 1) {
      endpoints <- cbind(
        "lwr" = pnbinom(y - 1, mu = fv, size = fv / (phi - 1)),
        "upr" = pnbinom(y, mu = fv, size = fv / (phi - 1))
      )
    } else {
      endpoints <- cbind(
        "lwr" = ppois(y - 1, lambda = fv),
        "upr" = ppois(y, lambda = fv)
      )
    }
  # Poisson --------------------------------------------------------------------
  } else if (fam == "poisson") {
    endpoints <- cbind(
      "lwr" = ppois(y - 1, lambda = fv),
      "upr" = ppois(y, lambda = fv)
    )
  } else {
    stop("Unsupported family type.", call. = FALSE)
  }
  return(endpoints)

}


#' @export
#' @method unifend negbin
#' @note
#' Support for GLMs with negative binomial family fit via the
#' [MASS](https://cran.r-project.org/package=MASS) package.
unifend.negbin <- function(object, y = NULL, ...) {
  if (is.null(y)) {  # get response vector
    if (is.null(object$y)) {
      stop("No response vector could be found, please supply it ",
           "using the `y` argument.", call. = FALSE)
    } else {
      y <- object$y
    }
  }
  fv <- object$fitted.values  # get fitted values
  endpoints <- cbind(
    "lwr" = pnbinom(y - 1, mu = fv, size = object$theta),
    "upr" = pnbinom(y, mu = fv, size = object$theta)
  )
  return(endpoints)
}


#' @export
#' @method unifend vglm
#' @note
#' Support for vector generalized linear models (VGLMs)  and vector generalized
#' additive models (VGAMs) fit via the
#' [vgam](https://cran.r-project.org/package=VGAM) package.
unifend.vglm <- function(object, ...) {
  # Seems to work for VGAMs to since they also apparently inherit from class "vglm"
  fam <- object@family@vfamily
  if ("VGAMordinal" %in% fam) {
    y <- apply(object@y, MARGIN = 1, FUN = function(j) which.max(j))
    # cumprobs <- cbind(0, t(apply(fitted(object), MARGIN = 1, FUN = cumsum)))
    cumprobs <- cbind(0, t(apply(object@fitted.values, MARGIN = 1, FUN = cumsum)))
    res <- cbind(
      "lwr" = cumprobs[cbind(seq_along(y), y)],     # P(Y < y_i)  (e.g., will be 0 if y_i = 1)
      "upr" = cumprobs[cbind(seq_along(y), y + 1)]  # P(Y <= y_i) (e.g., will be 1 if y_i = J)
    )
    return(res)
  } else {
    stop("Unsupported family type.", call. = FALSE)
  }
}


#' @export
#' @method unifend gam
#' @note
#' Support for generalized additive models (GAMs) fit via the
#' [mgcv](https://cran.r-project.org/package=mgcv) package.
unifend.gam <- function(object, ...) {
  # This should just work since mgcv models also inherit from class glm
  unifend.glm(object, ...)
}


#' @export
#' @method unifend zeroinfl
#' @note
#' Support for zero-inflated models fit via the
#' [pscl](https://cran.r-project.org/package=pscl) package.
unifend.zeroinfl <- function(object, y = NULL, ...) {
  if (!requireNamespace("VGAM", quietly = TRUE)) {
    stop("Package \"VGAM\" is required for this function to work. ",
         "Please install it.", call. = FALSE)
  }
  if (!requireNamespace("pscl", quietly = TRUE)) {
    stop("Package \"pscl\" is required for this function to work. ",
         "Please install it.", call. = FALSE)
  }
  if (is.null(y)) {  # get response vector
    if (is.null(object$y)) {
      stop("No response vector could be found, please supply it ",
           "using the `y` argument.", call. = FALSE)
    } else {
      y <- object$y
    }
  }
  fv.count <- predict(object, type = "count")
  fv.binary <- predict(object, type = "zero")
  res <- cbind(
    "lwr" = VGAM::pzipois(y - 1, lambda = fv.count, pstr0 = fv.binary),
    "upr" = VGAM::pzipois(y, lambda = fv.count, pstr0 = fv.binary)
  )
  return(res)
}


#' @noRd
#' @keywords internal
expand <- function(endpoints, resolution = 101, flat = FALSE) {
  # Much faster than `apply()` + `seq()`
  z <- matrix(nrow = nrow(endpoints), ncol = resolution)
  for (i in seq_len(resolution)) {
    z[, i] <- endpoints[, 1L] + (endpoints[, 2L] - endpoints[, 1L]) /
      (resolution - 1) * (i - 1)
  }
  if (isTRUE(flat)) {
    z <- as.vector(t(z))
  }
  return(z)
}
