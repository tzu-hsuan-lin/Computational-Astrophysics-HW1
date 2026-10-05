import numpy as np


def solve_kepler(M, e):
    """Solve Kepler's equation E - e * sin(E) = M for the eccentric anomaly E.

    Parameters
    ----------
    M : float or numpy.ndarray
        Mean anomaly in radians. Any real value.
    e : float
        Orbital eccentricity, must satisfy 0 <= e <= 0.99.

    Returns
    -------
    float or numpy.ndarray
        Eccentric anomaly E in radians, with the same shape as M.

    Raises
    ------
    ValueError
        If eccentricity e is not in the range [0, 0.99] or not a valid float.
    """
    # Validate eccentricity
    try:
        e = float(e)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid eccentricity {e}: must be a float")

    if np.isnan(e) or e < 0.0 or e > 0.99:
        raise ValueError(f"Eccentricity e={e} must be in [0, 0.99]")

    is_scalar = np.isscalar(M) or (isinstance(M, np.ndarray) and M.ndim == 0)
    M_arr = np.asarray(M, dtype=float)

    if M_arr.size == 0:
        return M_arr.copy()

    # Identity for circular orbit
    if e == 0.0:
        return float(M_arr) if is_scalar else M_arr.copy()

    # Enforce odd symmetry: solve for |M|, then negate for negative M
    is_neg = M_arr < 0.0
    abs_M = np.abs(M_arr)

    # Range reduction: M = M_red + 2*pi*k with M_red in [0, 2*pi)
    two_pi = 2.0 * np.pi
    k = np.floor(abs_M / two_pi)
    M1 = abs_M - two_pi * k

    # Fold [0, 2*pi) onto [0, pi] by reflection around pi
    flip = M1 > np.pi
    M2 = np.where(flip, two_pi - M1, M1)

    # Danby (1988) initial guess on [0, pi]
    denom = 1.0 - np.sin(M2 + e) + np.sin(M2)
    E2 = M2 + e * np.sin(M2) / denom

    # Vectorized Halley (3rd-order Householder/Newton) iteration
    for _ in range(8):
        f = E2 - e * np.sin(E2) - M2
        f1 = 1.0 - e * np.cos(E2)
        f2 = e * np.sin(E2)
        dE = f / f1
        dE = f / (f1 - 0.5 * dE * f2)
        E2 = E2 - dE

    # Safeguard: vectorized bisection fallback if any element has |residual| > 1e-12
    res2 = np.abs(E2 - e * np.sin(E2) - M2)
    if np.any(res2 > 1e-12):
        mask = res2 > 1e-12
        low = np.zeros_like(M2)
        high = np.full_like(M2, np.pi)
        for _ in range(60):
            mid = 0.5 * (low + high)
            f_mid = mid - e * np.sin(mid) - M2
            low = np.where(f_mid < 0.0, mid, low)
            high = np.where(f_mid >= 0.0, mid, high)
        E2 = np.where(mask, 0.5 * (low + high), E2)

    # Reconstruct back from [0, pi] to [0, 2*pi)
    E1 = np.where(flip, two_pi - E2, E2)

    # Reconstruct to full positive domain
    E_pos = E1 + two_pi * k

    # Direct Newton refinement against abs_M for high precision
    f_pos = E_pos - e * np.sin(E_pos) - abs_M
    f1_pos = 1.0 - e * np.cos(E_pos)
    E_pos = E_pos - f_pos / f1_pos

    # Apply odd symmetry
    E = np.where(is_neg, -E_pos, E_pos)

    return float(E) if is_scalar else E
