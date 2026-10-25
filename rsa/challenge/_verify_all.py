# -*- coding: utf-8 -*-
"""_verify_all.py — chay gen.py + solve.py cua tung challenge, doi chieu flag.
Cach chay: python _verify_all.py [ten_folder ...]"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))

EXPECTED = {
    "01_factor_small_n": "crypto{sm4ll_n_g0_brrr}",
    "02_fermat_close_primes": "crypto{f3rm4t_tw1n_pr1m3s_s1t_cl0s3}",
    "03_small_e_cuberoot": "crypto{sm4ll_e_n0_p4dd1ng_3asy_r00t}",
    "04_hastad_broadcast": "crypto{h4st4d_0n3_m3ss4g3_m4ny_b0x3s}",
    "05_common_modulus_external": "crypto{c0mm0n_m0dulus_n3v3r_sh4r3_N}",
    "06_common_modulus_internal": "crypto{ins1d3r_j0b_pr0p0s1t10n_1_fact0r}",
    "07_blinding_oracle": "crypto{bl1nd1ng_0r4cl3_s1gn3d_my_m3ss4g3}",
    "08_wiener_small_d": "crypto{w13n3r_c0nt1nu3d_fr4ct10ns}",
    "09_small_dp_bruteforce": "crypto{sm4ll_dp_crt_brut3f0rc3}",
    "10_crt_fault_signature": "crypto{b3llc0r3_f4ult_l34ks_p}",
    "11_parity_oracle": "crypto{lsb_0r4cl3_b1n4ry_s34rch}",
    "12_pollard_p_minus_1": "crypto{p0ll4rd_p_m1nus_1_sm00th}",
    "13_franklin_reiter": "crypto{fr4nkl1n_r31t3r_p0ly_gcd}",
    "14_bleichenbacher_pkcs1": "crypto{bb98}",
    "15_coppersmith_known_high_bits": "crypto{c0pp3rsm1th_kn0wn_h1gh_b1ts}",
    "16_short_pad_attack": "crypto{sh0rt_p4d_r3sult4nt_c0pp3rsm1th}",
    "17_bdf_partial_key_exposure": "crypto{bdf_p4rt14l_k3y_3xp0sur3}",
    "18_timing_attack_kocher": "crypto{t1m1ng_s1d3_ch4nn3l}",
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
        solve_path = os.path.join(folder, "solve.py")
        if not os.path.exists(solve_path):
            moved = os.path.join(HERE, "..", "solves", f"{name}.py")
            if os.path.exists(moved):
                print("   SKIP — solve.py da chuyen sang solves\\ (ban tham khao, "
                      "khong chay duoc tu day)")
                n_ok += 1
                continue
            print(f"   SOLVE MISSING (khong co solve.py va solves\\{name}.py)")
            n_fail += 1
            continue
        if os.path.exists(os.path.join(folder, "gen.py")):
            g = subprocess.run([sys.executable, "gen.py"], cwd=folder,
                               capture_output=True, text=True, timeout=600)
            if g.returncode != 0:
                print(f"   GEN FAIL:\n{g.stdout[-800:]}\n{g.stderr[-800:]}")
                n_fail += 1
                continue
        s = subprocess.run([sys.executable, "solve.py"], cwd=folder,
                           capture_output=True, text=True, timeout=900)
        out = (s.stdout + "\n" + s.stderr)[-1500:]
        flag = EXPECTED.get(name)
        if s.returncode == 0 and flag and flag in s.stdout:
            print(f"   OK  ({time.time()-t0:.1f}s)  {flag}")
            n_ok += 1
        else:
            print(f"   SOLVE FAIL ({time.time()-t0:.1f}s):")
            print("   " + out.replace("\n", "\n   "))
            n_fail += 1
    except subprocess.TimeoutExpired:
        print(f"   TIMEOUT sau {time.time()-t0:.0f}s")
        n_fail += 1
print(f"\n===== {n_ok} OK, {n_fail} FAIL =====")
sys.exit(1 if n_fail else 0)
