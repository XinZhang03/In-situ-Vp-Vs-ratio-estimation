"""
config for vp vs ratio calculating
"""

class Config(object):
    def __init__(self):

        # i/o paths
        self.dtcc = "input/dt.cc"
        self.cluster = "input/Duzce.reloc"

        self.out_config = "output/Duzce.log"
        self.out_array = "output/Duzce.npz"

        # preprocess params
        self.cc_thrd = 0.75

        # cal vp/vs params
        self.dtp_thrd = 0.1
        self.rms_max =0.005