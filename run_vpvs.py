import numpy as np
import matplotlib.pyplot as plt
from config import Config
from reader import *
from scipy import odr

cfg = Config()
dtcc = cfg.dtcc
cluster = cfg.cluster
cc_thrd = cfg.cc_thrd
dtp_thrd = cfg.dtp_thrd
rms_max = cfg.rms_max
out_config = cfg.out_config
out_arr = cfg.out_array
# read event id in cluster
evids = read_hypodd_reloc(cluster)

# read cc pairs in cluster
cc_pairs = read_dtcc(dtcc,evids,cc_thrd)

def main():
    w = open(out_config,"w")
    dtps = np.array([i[3] for i in cc_pairs])
    dtss = np.array([i[4] for i in cc_pairs])
    w.write("*"*40+"\n")
    w.write(f"1. Total {len(dtps)} dtp-dts pairs read in.\n\n")

    # using restriction of dtp_thrd
    dtss1 = dtss[np.abs(dtps)<dtp_thrd]
    dtps1 = dtps[np.abs(dtps)<dtp_thrd]
    w.write("*"*40+"\n")
    w.write(f"2. After using restriction if dtp:\n{len(dtps1)} dtp-dts pairs\n\n")

    # do regression with TLS
    a1,b1,_,_ = tls_odr(dtps1,dtss1)
    w.write("*"*40+"\n")
    w.write(f"3. After the first regression:\nVp/Vs = {a1:.4f}\n\n")

    # reomove the intercept
    dtps2 = dtps1
    dtss2 = dtss1-b1

    # do regression with TLS
    a2,b2,dx,dy = tls_odr(dtps2,dtss2)
    w.write("*"*40+"\n")
    w.write(f"4. After the second regression(reomve intercept):\nVp/Vs = {a2:.4f}\n\n")

    # remove rms > rms_max
    rms = np.sqrt(dx**2 + dy**2)
    dtps3 = dtps2[rms<rms_max]
    dtss3 = dtss2[rms<rms_max]
    w.write("*"*40+"\n")
    w.write(f"5. After using restriction if RMS.:\n{len(dtps)} dtp-dts pairs\n\n")

    # do regression with TLS
    a3,b3,_,_ = tls_odr(dtps3,dtss3)
    w.write("*"*40+"\n")
    w.write(f"6. After the third regression(reomve intercept):\nVp/Vs = {a3:.4f}\n\n")

    # Bootstrap uncertainty
    # -------------------------
    vpvs_boot = bootstrap_tls(dtps3, dtss3, n_boot=2000)
    vpvs_mean = vpvs_boot.mean()
    vpvs_std = vpvs_boot.std()
    vpvs_ci = np.percentile(vpvs_boot, [2.5, 97.5])
    w.write("*"*40+"\n")
    w.write("7. Bootstrap uncertainty:\n")
    w.write(f"Mean Vp/Vs = {vpvs_mean:.4f}\n")
    w.write(f"Std  Vp/Vs = {vpvs_std:.4f}\n")
    w.write(f"95% CI     = [{vpvs_ci[0]:.4f}, {vpvs_ci[1]:.4f}]\n\n")
    w.close()

    # Save info.
    np.savez(
        out_arr,
        dtps=dtps3,
        dtss=dtss3,
        vpvs=a3,
        vpvs_bootstrap=vpvs_boot,
        vpvs_mean=vpvs_mean,
        vpvs_std=vpvs_std,
        rms_max=rms_max,
        dtp_thrd=dtp_thrd,
        n_pairs=len(dtps3)
    )

    print(f"[INFO] Results saved to {out_arr}\n[INFO] Config saved to {out_config}")
    
def tls_odr(x, y):
    """
    Total Least Squares (ODR) for y = a*x + b
    Returrn: a, b
    """
    x = np.asarray(x)
    y = np.asarray(y)

    # linear model
    def linear_model(beta, x):
        return beta[0] * x + beta[1]   # beta = [a, b]

    model = odr.Model(linear_model)
    data = odr.RealData(x, y)  # σx = σy = 1 → TLS
    odr_inst = odr.ODR(data, model, beta0=np.polyfit(x, y, 1))

    out = odr_inst.run()
    a, b = out.beta
    dx = out.delta
    dy = out.eps
    return a, b, dx, dy

def bootstrap_tls(x, y, n_boot=1000, random_state=42):
    """
    Bootstrap estimation of TLS slope uncertainty

    Parameters
    ----------
    x, y : array-like
        Input data
    n_boot : int
        Number of bootstrap samples

    Returns
    -------
    slopes : ndarray
        Bootstrap slopes
    """
    rng = np.random.default_rng(random_state)
    n = len(x)
    slopes = np.zeros(n_boot)

    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        xb = x[idx]
        yb = y[idx]

        a, b, _, _ = tls_odr(xb, yb)
        slopes[i] = a

    return slopes

if __name__ == "__main__":

    main()
