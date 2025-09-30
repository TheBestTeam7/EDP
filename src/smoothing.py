
import numpy as np

def running_mean_13(x: np.ndarray) -> np.ndarray:
    """
    13-month running mean with weights:
      - Full 13-month window:
          edge months weight = 1/24 (i-6 and i+6)
          inner 11 months weight = 1/12 each (i-5..i+5)
      - Near boundaries (where full window not available):
          simple arithmetic mean of available values.
    """
    x = np.asarray(x, dtype=float)
    n = len(x)
    y = np.full(n, np.nan, dtype=float)

    for i in range(n):
        lo = max(0, i-6)
        hi = min(n-1, i+6)
        window = x[lo:hi+1]
        k = hi - lo + 1
        if k == 13:
            # Weights for full window
            weights = np.ones(13) * (1/12)    # inner 11 months
            weights[0] = 1/24                  # i-6
            weights[-1] = 1/24                 # i+6
            y[i] = np.dot(window, weights)
        else:
            # Simple mean for boundary windows
            y[i] = np.nanmean(window)
    return y

if __name__ == '__main__':
    # Simple self-test
    test = np.arange(1, 30, dtype=float)
    sm = running_mean_13(test)
    assert np.all(np.isfinite(sm)), "Smoothed array should be finite for finite inputs"
    print("Self-test OK")
