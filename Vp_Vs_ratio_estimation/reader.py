'''
fuctions for reading and processing
'''
import os
from obspy import UTCDateTime


def read_hypodd_reloc(freloc):
    if not os.path.exists(freloc): return
    f=open(freloc); lines=f.readlines(); f.close()
    evids = []
    for line in lines:
        codes = line.split()
        evid = codes[0]
        evids.append(evid)
    return evids

def read_dtcc(fdtcc, evids, cc_thrd):
    """
    fdtcc: dt.cc file
    evids: the same cluster id list
    cc_thrd: threshold of cc
   
    Retrun : list of [station, evid1, evid2, dtp, dts]
    """
    if not os.path.exists(fdtcc):
        return []

    f=open(fdtcc); lines=f.readlines(); f.close()
    result = []
    in_cluster = False
    idx_pair = None
    cc_pairs = {}  # { (evid1, evid2): {station: {'P': dt, 'S': dt}} }
    for l in lines:
        l = l.strip()
        if not l: 
            continue
        codes = l.split()
        if codes[0] == "#":
            evid1, evid2 = codes[1], codes[2]
            if (evid1 in evids) and (evid2 in evids):
                idx_pair = (evid1, evid2)
                cc_pairs[idx_pair] = {}
                in_cluster = True
            else:
                in_cluster = False
                idx_pair = None
        else:
            if in_cluster:
                station = codes[0]
                dt = float(codes[1])
                cc = float(codes[2])
                phase = codes[3].upper() 

                if cc >= cc_thrd:
                    if station not in cc_pairs[idx_pair]:
                        cc_pairs[idx_pair][station] = {}
                    cc_pairs[idx_pair][station][phase] = dt

    # both P and S
    for (evid1, evid2), stations in cc_pairs.items():
        for station, phases in stations.items():
            if 'P' in phases and 'S' in phases:
                result.append([station, evid1, evid2, phases['P'], phases['S']])

    return result