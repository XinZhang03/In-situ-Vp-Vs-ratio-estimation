# In-situ Vp/Vs Estimation

This repository provides a robust Python workflow to estimate the **Vp/Vs ratio**
from earthquake cluster **dtP–dtS** data using
**Total Least Squares (TLS)** regression implemented via
**Orthogonal Distance Regression (ODR)**.

Uncertainty is quantified using **bootstrap resampling**, making the method
suitable for research and reproducible seismic analysis.

---

## Scientific Background

In an ideal case where events occur in a homogeneous medium (P and S rays share the same path), and the measurements contain no error or noise, the P and S differential travel times of an arbitrary pair of events 1 and 2 recorded at the same station i ($\Delta t_{12,i}^p$ and  $\Delta t_{12,i}^s$) lie on a line with zero intercept and a slope equal to the $( V_p / V_s )$ of the medium:

$$
\Delta t_{12,i}^p = t_{1,i}^p - t_{2,i}^p
= \frac{\Delta L}{V_p},
$$
$$
\Delta t_{12,i}^s = t_{1,i}^s - t_{2,i}^s
= \frac{\Delta L}{V_s},
$$

$$
\Delta t_{12,i}^s=\frac{V_p}{V_s}\Delta t_{12,i}^p,
$$

where $t_{1,i}^p, t_{2,i}^p, t_{1,i}^s$ and $t_{2,i}^s$ are the observed P and S travel times, and $\Delta L$ is the path-length difference.

In reality, the origin times of the two events contain errors $t_1^o$ and $t_2^o$, respectively, which cause the P and S differential times of each event pair to form a line with a non-zero intercept term related to the origin-time errors (e.g., Figure 5 in Lin and Shearer (2007)):

$$
\Delta t_{12,i}^p = \left( t_{1,i}^p - t_{2,i}^p \right) + \left( t_1^o - t_2^o \right)
=\frac{\Delta L}{V_p} + \Delta t_{12},
$$

$$
\Delta t_{12,i}^s = \left( t_{1,i}^s - t_{2,i}^s \right) + \left( t_1^o - t_2^o \right)
= \frac{\Delta L}{V_s} + \Delta t_{12},
$$

$$
\Delta t_{12,i}^s = \frac{V_p}{V_s} \Delta t_{12,i}^p + \left( 1 - \frac{V_p}{V_s} \right) \Delta t_{12}.
$$

However, both $\Delta t_{12,i}^p$ and $\Delta t_{12,i}^s$ contain measurement errors.
Ordinary least squares (OLS) leads to biased estimates.

This project uses:
- **TLS (ODR)** → minimizes orthogonal distance to the regression line
- **Bootstrap** → estimates uncertainty without assuming Gaussian errors

---

## Workflow

1. Read dtP–dtS pairs from cross-correlation data
2. Apply dtP threshold
3. First TLS regression (estimate intercept)
4. Remove intercept 
5. Second TLS regression
6. Remove outliers using orthogonal RMS residual
7. Final TLS regression → Vp/Vs
8. Bootstrap resampling → uncertainty estimation

---

## Input
### 1. Differential time file (`input/dt.cc`)
corss-correlation based differential time of event-pair
### 2. cluster index (`input/Duzce.reloc`)
in hypoDD.reloc format
### 3. Parameter Adjustment File (`config.py`)
---

## Output

### 1. Log file (`output/Duzce.log`)
Text file documenting:
- Data counts at each step
- Regression results
- Bootstrap uncertainty

### 2. NumPy archive (`output/Duzce.npz`)
Stored results:

| Key | Description |
|----|------------|
| `dtps`, `dtss` | Final cleaned data |
| `vpvs` | Final Vp/Vs |
| `vpvs_bootstrap` | Bootstrap samples |
| `vpvs_mean` | Bootstrap mean |
| `vpvs_std` | Bootstrap standard deviation |
| `n_pairs` | Number of data points|

---

## Reference
1. Lin, G., & Shearer, P. (2007). Estimating Local Vp/Vs Ratios within Similar Earthquake Clusters. Bulletin of the Seismological Society of America, 97(2), 379-388. 10.1785/0120060115


2. Liu, T., Gong, J., Fan, W., & Lin, G. (2023). In-Situ Vp/Vs Reveals Fault-Zone Material Variation at the Westernmost Gofar Transform Fault, East Pacific Rise. Journal of Geophysical Research: Solid Earth, 128(3), e2022JB025310. https://doi.org/10.1029/2022JB025310
