# -*- coding: utf-8 -*-
"""gen.py — L01: xap xi thap phan cua alpha = 5 + cbrt(19)."""
from decimal import Decimal, getcontext

getcontext().prec = 40
alpha = Decimal(5) + Decimal(19) ** (Decimal(1) / 3)
beta = str(alpha)[:14]  # 12 chu so le

open("output.txt", "w").write(
    "alpha = 5 + cbrt(19)\n"
    f"alpha ≈ {beta}\n"
    "degree(f) = 3, |a_i| < 1000\n"
)
print("gen ok:", beta)
