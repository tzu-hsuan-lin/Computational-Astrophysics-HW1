import numpy as np
import pytest

from hw1.kepler import solve_kepler


def test_kepler_e_zero():
    """When eccentricity e = 0, Kepler's equation simplifies to E = M."""
    # Scalar check
    M_scalar = 1.234
    E_scalar = solve_kepler(M_scalar, 0.0)
    assert np.isclose(E_scalar, M_scalar, atol=1e-10)

    # Array check across diverse mean anomalies
    M_arr = np.linspace(-3 * np.pi, 3 * np.pi, 50)
    E_arr = solve_kepler(M_arr, 0.0)
    np.testing.assert_allclose(E_arr, M_arr, atol=1e-10)


def test_kepler_residual_accuracy_random():
    """Verify residual |E - e*sin(E) - M| < 1e-10 for 1000 random (M, e) pairs."""
    rng = np.random.default_rng(42)
    # M across several orbits [-4*pi, 4*pi]
    M_rand = rng.uniform(-4 * np.pi, 4 * np.pi, size=1000)
    # e uniformly within the valid range [0, 0.99]
    e_rand = rng.uniform(0.0, 0.99, size=1000)

    for M_val, e_val in zip(M_rand, e_rand):
        E_val = solve_kepler(M_val, float(e_val))
        residual = np.abs(E_val - e_val * np.sin(E_val) - M_val)
        assert residual < 1e-10


def test_kepler_symmetry():
    """Verify the odd symmetry requirement: solve_kepler(-M, e) == -solve_kepler(M, e)."""
    M_vals = np.array([0.0, 0.1, 0.5, 1.0, 2.0, np.pi, 4.5, 10.0])
    e_vals = [0.0, 0.1, 0.5, 0.8, 0.95, 0.99]

    for e in e_vals:
        pos_E = solve_kepler(M_vals, e)
        neg_E = solve_kepler(-M_vals, e)
        np.testing.assert_allclose(neg_E, -pos_E, atol=1e-10)


def test_kepler_m_outside_standard_interval():
    """Verify solver handles M values outside [0, 2*pi), including large and negative M."""
    M_outside = np.array([-100.0, -10 * np.pi, -np.pi / 2, 3 * np.pi, 10 * np.pi, 123.456])
    e_vals = [0.0, 0.2, 0.7, 0.95]

    for e in e_vals:
        E = solve_kepler(M_outside, e)
        residuals = np.abs(E - e * np.sin(E) - M_outside)
        assert np.all(residuals < 1e-10)


def test_kepler_vectorized_numpy_input():
    """Verify vectorized NumPy input works without Python loops and preserves input shapes."""
    # 1D array
    M_1d = np.linspace(0, 2 * np.pi, 100)
    E_1d = solve_kepler(M_1d, 0.5)
    assert isinstance(E_1d, np.ndarray)
    assert E_1d.shape == M_1d.shape
    residuals_1d = np.abs(E_1d - 0.5 * np.sin(E_1d) - M_1d)
    assert np.all(residuals_1d < 1e-10)

    # 2D array
    M_2d = np.linspace(0, 2 * np.pi, 24).reshape((4, 6))
    E_2d = solve_kepler(M_2d, 0.3)
    assert isinstance(E_2d, np.ndarray)
    assert E_2d.shape == (4, 6)
    residuals_2d = np.abs(E_2d - 0.3 * np.sin(E_2d) - M_2d)
    assert np.all(residuals_2d < 1e-10)


def test_kepler_invalid_eccentricity():
    """Verify ValueError is raised when eccentricity is outside [0, 0.99]."""
    invalid_e_values = [-1.0, -0.001, 0.990001, 0.991, 1.0, 1.5]

    for e_invalid in invalid_e_values:
        with pytest.raises(ValueError):
            solve_kepler(1.0, e_invalid)

        with pytest.raises(ValueError):
            solve_kepler(np.array([0.5, 1.0]), e_invalid)


def test_kepler_scalar_input():
    """Verify scalar input produces scalar output with residual < 1e-10."""
    M_scalar = 0.85
    e = 0.6
    E_scalar = solve_kepler(M_scalar, e)

    # Output should be a scalar float (or numpy scalar)
    assert np.isscalar(E_scalar)
    residual = np.abs(E_scalar - e * np.sin(E_scalar) - M_scalar)
    assert residual < 1e-10


def test_kepler_high_eccentricity_near_099():
    """Verify solver converges accurately at high eccentricity boundary near e = 0.99."""
    e_high = 0.99
    # Include challenging points: near periapsis (M close to 0), apoapsis (M near pi), and various phases
    M_vals = np.array([1e-6, 1e-4, 0.01, 0.1, np.pi / 2, np.pi - 1e-3, np.pi, 5.0, 15.0])
    E = solve_kepler(M_vals, e_high)

    residuals = np.abs(E - e_high * np.sin(E) - M_vals)
    assert np.all(residuals < 1e-10)
