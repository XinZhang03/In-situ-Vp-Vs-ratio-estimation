import numpy as np
import matplotlib.pyplot as plt
from config import Config

cfg = Config()
out_arr = cfg.out_array
dtp_thrd = cfg.dtp_thrd
fontsize = 12
data = np.load(out_arr)
dtps = data["dtps"]
dtss = data["dtss"]
vpvs = data["vpvs"]


plt.figure(figsize=(5,10))
plt.scatter(dtps,dtss,s=1,c="gray")
plt.plot(dtps,vpvs*dtps,c="r")
plt.text(-dtp_thrd*0.9,dtp_thrd*1.7,f"Vp/Vs = {vpvs:.4f}\nnpts:{len(dtps)}",fontsize=fontsize+5)
plt.xlim([-dtp_thrd,dtp_thrd])
plt.ylim([-dtp_thrd*2,dtp_thrd*2])
plt.xlabel("dtp(s)",fontsize=fontsize)
plt.ylabel("dts(s)",fontsize=fontsize)
plt.tick_params(labelsize=fontsize)
plt.tight_layout()
plt.savefig("output/vpvs.png",dpi=300)