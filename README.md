# In-situ-Vp-Vs-ratio-estimation
In-situ Vp Vs ratio estimation using Orthogonal Distance Regression (ODR)
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
- Usage
  `python run_vpvs.py`
## Dependencies

- Python ≥ 3.8
- numpy
- scipy
- matplotlib (optional, for visualization)

## Reference
1. Lin, G., & Shearer, P. (2007). Estimating Local Vp/Vs Ratios within Similar Earthquake Clusters. Bulletin of the Seismological Society of America, 97(2), 379-388. 10.1785/0120060115

2. Liu, T., Gong, J., Fan, W., & Lin, G. (2023). In-Situ Vp/Vs Reveals Fault-Zone Material Variation at the Westernmost Gofar Transform Fault, East Pacific Rise. Journal of Geophysical Research: Solid Earth, 128(3), e2022JB025310. https://doi.org/10.1029/2022JB025310
