#' Function residuals
#'
#' Computes the functional residuals described in Liu et al. (2025). Functional
#' residuals capture the entire distribution of residual randomness for each
#' observation, providing a unified framework for discrete and continuous outcomes.
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
#' @param type Character string specifying the type of residual to compute.
#' Current options include:
#' * `"function"` - (the default) for a list of functional residuals;
#' * `"surrogate"` for a sample of surrogate residuals;
#' * `"probscale"` for probability-scale residuals.
#'
#' @param link.scale Logical indicating whether or not surrogate residuals
#' (`type = "surrogate"`) should be returned on the link scale (`TRUE`) vs. the
#' probability scale (`FALSE`). Default is `TRUE`.
#'
#' @param ... Additional optional arguments. Currently ignored.
#'
#' @return If `type = "function"`, an object of class `"unifres"` which is a list
#' of cumulative distribution functions (CDFs). If `type = "surrogate"` or
#' `type = "probscale"`, a numeric vector of residuals.
#'
#' @references
#' Liu, D., Lin, Z., & Zhang, H. (2025). A unified framework for residual
#' diagnostics in generalized linear models and beyond. *Journal of the American
#' Statistical Association*, 1–29.
#' \doi{10.1080/01621459.2025.2504037}
#'
#' @examples
#' # Generate data from a logistic regression model with quadratic form
#' set.seed(1217)
#' n <- 1000
#' x <- rnorm(n)
#' z <- 1 - 2*x + 3*x^2 + rlogis(n)
#' y <- ifelse(z > 0, 1, 0)
#'
#' # Fit models with/without quadratic term
#' fit.wrong <- glm(y ~ x, family = binomial)  # wrong
#' fit.right <- glm(y ~ x + I(x^2), family = binomial)  # right
#'
#' # Generate functional residuals
#' fres.wrong <- fresiduals(fit.wrong)
#' plot(fres.wrong[[1]])  # plot first functional residual
#'
#' # Function-function plot
#' par(mfrow = c(1, 2))
#' ffplot(fres.wrong, type = "l")
#' ffplot(fit.wrong, type = "l")
#'
#' # Residual vs. predictor plot for each model based on surrogate method
#' par(mfrow = c(1, 2), las = 1)
#' lpars <- list(col = 2, lwd = 2)
#' col <- adjustcolor(1, alpha.f = 0.1)
#' palette("Okabe-Ito")
#' scatter.smooth(x, y = fresiduals(fit.wrong, type = "surrogate"),
#'                lpars = lpars, col = col, main = "Wrong model",
#'                xlab = "x", ylab = "Surrogate residual")
#' abline(h = 0, col = 3, lty = 2)
#' scatter.smooth(x, y = fresiduals(fit.right, type = "surrogate"),
#'                lpars = lpars, col = col, main = "Correct model",
#'                xlab = "x", ylab = "Surrogate residual")
#' abline(h = 0, col = 3, lty = 2)
#' @export
fresiduals <- function(object, type = c("function", "surrogate", "probscale"),
                       link.scale = TRUE, ...) {
  UseMethod("fresiduals")
}


#' @rdname fresiduals
#' @export
fresiduals.default <- function(object, type = c("function", "surrogate", "probscale"),
                       link.scale = TRUE, ...) {
  uend <- unifend(object)  # compute uniform endpoints for function residuals
  res <- fresiduals.matrix(object = uend, type = type,  link.scale = FALSE, ...)
  if (isTRUE(link.scale) && match.arg(type) == "surrogate") {
    if (!is.null(object$family$linkfun)) {
      res <- object$family$linkfun(res)
    }
  }
  return(res)
}


#' @rdname fresiduals
#' @export
fresiduals.matrix <- function(object, type = c("function", "surrogate", "probscale"),
                               link.scale = TRUE, ...) {
  # Sanity checks
  if (ncol(object) != 2) {
    stop("Input matrix should have exactly two columns.", call. = FALSE)
  }
  type <- match.arg(type)
  if (type == "function") {
    res <- apply(object, MARGIN = 1, FUN = function(endpoints) {
      function(t) punif(t, min = endpoints[1L], max = endpoints[2L])
    })
    class(res) <- c("unifres", class(res))
  } else if (type == "surrogate") {
    runifs <- apply(object, MARGIN = 1, FUN = function(endpoints) {
      function(n) runif(n, min = endpoints[1L], max = endpoints[2L])
    })
    res <- sapply(runifs, FUN = function(sampler) sampler(1))
    if (isTRUE(link.scale)) {
      warning("link.scale = TRUE requires the original model object to access the link function; returning residuals on the probability scale instead.", call. = FALSE)
    }
  } else {
    res <- apply(object, MARGIN = 1, FUN = function(endpoints) {
      2*mean(endpoints) - 1
    })
  }
  return(res)
}

