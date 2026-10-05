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

### Acceptance Criteria / Tests

1. e = 0 identity: `solve_kepler(M, 0) = M`
2. Residual error < 1e-10 across 1000 random (M, e) pairs with e in [0, 0.99]
3. Odd symmetry: `solve_kepler(-M, e) = -solve_kepler(M, e)`
4. Correct handling of M outside [0, 2π)
5. Multi-dimensional NumPy array vectorization and shape preservation
6. Invalid eccentricity error handling: e < 0 or e > 0.99 raises ValueError
7. Scalar float input/output compatibility
8. High-eccentricity boundary behavior near e = 0.99
