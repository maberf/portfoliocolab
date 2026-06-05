# %%
import pandas as pd
import numpy as np
from scipy.optimize import minimize

# %%
# portfolio PERFORMANCE calculation function
def portfolioPerformance(weights, mu, cov, riskfree):
    """
    function to calculate portfolio performance: return, volatility, sharpe ratio
    cov: matriz de covariância (numpy array)
    weights: weight vector (numpy array)
    mu: return vector (numpy array)
    riskfree: risk free ration (same period)
    returns
    ret, vol, sharpe - [type]: [float]
    """
    w = np.array(weights)
    ret = float(np.dot(w, mu))
    vol = float(np.sqrt(w.T @ cov @ w))
    if vol == 0:
        sharpe = 0.00
    else:
        sharpe = (ret - riskfree) / vol
    return ret, vol, sharpe

# %%
# portfolio MAXIMUM SHARPE calculation function
def maxSharpeWeights(mu, cov, risk_free, bounds=None, constraints=None):
    """
    finds the weights that maximize the Sharpe ratio (using minimize on -sharpe).
    bounds: list of tuples (min, max) for each asset. Default: (0,1) for all.
    constraints: list of constraint dicts for scipy.optimize.minimize (optional).
    returns the optimization result dictionary and the optimal weights.
    returns
    res - [type]: [OptimizeResult]
    res.x = [type]: [list]
    """

    n = len(mu)
    if bounds is None:
        bounds = tuple((0.0, 1.0) for _ in range(n))
    # constraint: sum of weights = 1
    cons = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0}]
    if constraints:
        cons.extend(constraints)
    # initialization: equal weights
    x0 = np.ones(n) / n

    def neg_sharpe(w):
        _, _, s = portfolioPerformance(w, mu, cov, risk_free)
        return -s

    res = minimize(neg_sharpe, x0, method='SLSQP', bounds=bounds, constraints=cons)

    return res, res.x if res.success else None


# %%
# Portfolio TARGET SHARPE calculation function (adjusted with the use of limitsport)
def targetSharpeWeights(mu, cov, target_sharpe, riskfree, port_limits, tol=1e-6, maxiter=1000):
    """
    Finds weights that approximate a target Sharpe ratio, using individual limits defined in limitsport.
    Minimizes the squared error between Sharpe(weights) and target_sharpe.
    returns
    res - [type]: [OptimizeResult]
    res.x = [type]: [list]
    info = [type]: [dict]
    """

    # convert to fraction (0..1)
    limitsport = [float(x) / 100.0 for x in port_limits]

    # check feasibility: the sum of the maximums must be >= 1 to allow sum(w)=1
    sum_limits = sum(limitsport)
    if sum_limits < 1.0 - 1e-12:
      # strategy: scale the limits proportionally until the sum becomes 1.0
      # (keeping each limit <= 1.0). This preserves the ratio among limits.
      scale = 1.0 / sum_limits
      limitsport = [min(1.0, l * scale) for l in limitsport]
      print(f"WARNING: sum of limits < 1.0 — limits scaled proportionally (scale={scale:.6f}) to make the problem feasible.")
      # recompute sum for information
      print("New limits (fraction):", limitsport)
      print("Sum of new limits:", sum(limitsport))

    n = len(mu)

    # Build bounds using the limits provided by the user (limitsport)
    bounds = tuple((0.0, limitsport[i]) for i in range(n))

    # Constraint: sum of weights = 1
    cons = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0}]

    # Initial guess
    x0 = np.ones(n) / n

    def sharpe_err_sq(w):
        _, _, s = portfolioPerformance(w, mu, cov, riskfree)
        return (s - target_sharpe)**2

    opts = {'maxiter': maxiter, 'ftol': tol}
    res = minimize(sharpe_err_sq, x0, method='SLSQP', bounds=bounds, constraints=cons, options=opts)

    if res.success:
        ret, vol, s = portfolioPerformance(res.x, mu, cov, riskfree)
        info = {'target_sharpe': target_sharpe, 'achieved_sharpe': s, 'ret': ret, 'vol': vol}
    else:
        info = {'message': res.message}

    return res, res.x if res.success else None, info


