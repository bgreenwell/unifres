#' Function-function plot
#'
#' Constructs a function-function (Fn-Fn) plot. That is, a plot of the average
#' functional residual against the CDF of a U(0, 1) random variable.
#'
#' @param object Either a [unifres][fresiduals] object (i.e., a list of
#' functional residuals) or a fitted model for which the extraction of
#' [functional residuals][fresiduals] is meaningful (e.g., a [glm][stats::glm]
#' object).
#'
#' @param resolution Integer specifying the number of points between 0 and 1 to
#' use. Default is 101.
#'
#' @param n Integer specifying the number of functional residuals to draw at
#' random, which can help with compute time. Default is `NULL` which corresponds
#' to no subsampling.
#'
#' @param ref.col Character string or integer specifying the color to use for
#' the 45-degree reference line. Default is 1.
#'
#' @param ref.lwd Integer specifying the line width to use for the 45-degree
#' reference line. Default is 1.
#'
#' @param ref.lty Character string or integer specifying the line type to use
#' for the 45-degree reference line. Default is `"dashed"`.
#'
#' @param ... Additional optional arguments pass to [plot()][base::plot].
#'
#' @export
ffplot <- function(object, resolution = 101, n = NULL, ref.col = 2,
                   ref.lwd = 1, ref.lty = "dashed", ...) {
  UseMethod("ffplot")
}


#' @rdname ffplot
#' @export
ffplot.unifres <- function(object, resolution = 101, n = NULL, ref.col = 2,
                          ref.lwd = 1, ref.lty = "dashed", ...) {
  tvals <- seq(from = 0, to = 1, length = resolution)
  if (!is.null(n)) {
    idx <- sample.int(length(object), size = n, replace = FALSE)
    object <- object[idx]
  }
  Ft <- vapply(tvals, FUN.VALUE = numeric(1), FUN = function(tval) {
    mean(sapply(object, FUN = do.call, list(tval)))
  })
  plot(tvals, y = Ft, xlab = "t", ylab = "Mean residual", ...)
  abline(0, 1, col = ref.col, lwd = ref.lwd, lty = ref.lty)
}


#' @rdname ffplot
#' @export
ffplot.default <- function(object, resolution = 101, n = NULL, ref.col = 1,
                           ref.lwd = 1, ref.lty = "dashed", ...) {
  tvals <- seq(from = 0, to = 1, length = resolution)
  fres <- fresiduals(object, type = "function")
  if (!is.null(n)) {
    idx <- sample.int(length(fres), size = n, replace = FALSE)
    fres <- fres[idx]
  }
  Ft <- vapply(tvals, FUN.VALUE = numeric(1), FUN = function(tval) {
    mean(sapply(fres, FUN = do.call, list(tval)))
  })
  plot(tvals, y = Ft, xlab = "t", ylab = "Mean residual", ...)
  abline(0, 1, col = ref.col, lwd = ref.lwd, lty = ref.lty)
}
