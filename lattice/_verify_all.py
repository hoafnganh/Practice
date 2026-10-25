# -*- coding: utf-8 -*-
"""_verify_all.py — chay gen.py + solve.py cua tung lattice challenge, doi chieu flag.
Cach chay: python _verify_all.py [ten_folder ...]"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))

EXPECTED = {
    "L01_minimal_poly": "crypto{[-144,75,-15,1]}",
    "L02_subset_sum": "crypto{kn4ps4ck_r3d}",
    "L03_stereotyped": None,          # flag sinh ngau nhien — chi can solve ok
    "L04_partial_key": "crypto{msb_0f_d_g1v3s_k_f0r_fr33}",
    "L05_hnp_basic": "crypto{h1dd3n_numb3r_bv96_l0c4t3d}",
    "L06_truncated_lcg": "crypto{trunc4t3d_lcg_1s_hnp_1n_d1sgu1s3}",
    "L07_ecdsa_xor_nonce": "crypto{x0r_n0nc3_1s_subs3t_sum_tsj}",
    "L08_ecdsa_biased": "crypto{b14s3d_n0nc3_l34ds_t0_d00m}",
    "L09_ecdsa_shared_msb": "crypto{sh4r3d_msb_n0t_s0_s3cr3t}",
    "L10_ehnp": "crypto{3hnp_chunks_r3v34l_4ll}",
    "L11_boneh_durfee": "crypto{b0n3h_durf33_b3y0nd_w13n3r}",
    "L12_bleichen_lattice": "crypto{bl31ch3nb4ch3r_4s_hnp}",
}

targets = sys.argv[1:] if len(sys.argv) > 1 else sorted(EXPECTED.keys())
n_ok = n_fail = 0
for name in targets:
    folder = os.path.join(HERE, name)
    if not os.path.isdir(folder):
        print(f"== {name}: KHONG TON TAI")
        n_fail += 1
        continue
    print(f"== {name}", flush=True)
    t0 = time.time()
    try:
        if os.path.exists(os.path.join(folder, "gen.py")):
            g = subprocess.run([sys.executable, "gen.py"], cwd=folder,
                               capture_output=True, text=True, timeout=900)
            if g.returncode != 0:
                print(f"   GEN FAIL:\n{g.stdout[-800:]}\n{g.stderr[-800:]}")
                n_fail += 1
                continue
        # solve da duoc tach ra ..\..\solves\<name>.py (file phang, tu chdir)
        solve_py = os.path.normpath(os.path.join(HERE, "..", "..", "solves",
                                                 name + ".py"))
        if not os.path.exists(solve_py):
            print(f"   KHONG TON TAI SOLVE: {solve_py}")
            n_fail += 1
            continue
        s = subprocess.run([sys.executable, solve_py], cwd=folder,
                           capture_output=True, text=True, timeout=1800)
        out = (s.stdout + "\n" + s.stderr)[-1500:]
        flag = EXPECTED.get(name)
        ok = s.returncode == 0 and (flag is None or flag in s.stdout)
        if ok:
            print(f"   OK  ({time.time()-t0:.1f}s)  {flag or '(flag ngau nhien)'}")
            n_ok += 1
        else:
            print(f"   SOLVE FAIL ({time.time()-t0:.1f}s):")
            print("   " + out.replace("\n", "\n   "))
            n_fail += 1
    except subprocess.TimeoutExpired:
        print(f"   TIMEOUT ({time.time()-t0:.1f}s)")
        n_fail += 1
    except Exception as ex:
        print(f"   LOI: {ex}")
        n_fail += 1

print(f"\n===== {n_ok} OK, {n_fail} FAIL")
sys.exit(1 if n_fail else 0)
