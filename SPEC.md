## Spec: solve_kepler

Solve Kepler's equation `E - e sin(E) = M` for the eccentric anomaly `E`.

- Signature: `solve_kepler(M, e)`
- `M`: mean anomaly in radians; float or NumPy array, any real value.
- `e`: eccentricity, float, `0 <= e <= 0.99`; raise `ValueError` otherwise.
- Returns `E` in radians, same shape as `M`.
- Accuracy: `|E - e*sin(E) - M| < 1e-10` for every element.
- Must satisfy `solve_kepler(-M, e) = -solve_kepler(M, e)`.
- Must correctly handle `M` outside `[0, 2π)`.
- Must be vectorized over `M` (no Python loop over elements).
- Dependencies: NumPy only.

