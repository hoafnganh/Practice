# L04 — SOLUTION

## Ý tưởng cốt lõi (mục 5.2.2 của paper)

Từ phương trình khóa RSA:

$$ed = 1 + k\varphi(N) = 1 + k(N + 1 - 2s), \qquad s = \frac{p+q}{2}$$

số $k = \frac{ed-1}{\varphi}$ **xấp xỉ được từ phần đã biết của $d$**:

$$k_0 = \left\lfloor \frac{e\,d_0}{N} \right\rfloor, \qquad |k - k_0| \lesssim \frac{e}{\varphi}\cdot(d - d_0)$$

— vì $e \approx \varphi\cdot(\text{tỷ lệ ngẫu nhiên}) \le \varphi$ và $\varphi \approx N$.
Trong challenge này phần ẩn chỉ 8 bit nên $|k - k_0| \le 256$: **liệt kê vài trăm ứng viên $k$**.

## Với mỗi ứng viên $k$

Lấy phương trình theo mô-đun $e$:

$$2ks \equiv 1 + k(N+1) \pmod e \;\Longrightarrow\; s \equiv (2k)^{-1}\bigl(1 + k(N+1)\bigr) \pmod e$$

Rồi giải $z^2 - 2sz + N = 0$ (nhận $s \pm \sqrt{s^2 - N}$) — nếu nghiệm nguyên và
nhân ra đúng $N$ thì đã factor xong, $d = (1 + k\varphi)/e$.

## Đi xa hơn (bản lattice đầy đủ — Ernst et al. 2005)

Khi phần ẩn của $d$ lớn (tới $N^{1/4}$ với $d < N^{0.75}$...), $k_1 = k - k_0$
không liệt kê được nữa. Khi đó cặp $(k_1, s)$ là **nghiệm nhỏ của đa thức 2 biến**:

$$f(x, y) = 1 + 2(k_0 + x)\Bigl(\frac{N+1}{2} - y\Bigr) \equiv 0 \pmod e$$

— đúng khung bivariate Coppersmith kiểu Boneh–Durfee (xây trong `latlib.bivariate_modular_small_roots`,
được dùng cho challenge L11). Việc chọn shift polynomial cho trường hợp tổng quát
phức tạp hơn BD thuần (Blömer–May 2003, Ernst et al. 2005) — ngoài phạm vi tutorial
nhưng nguyên lý vẫn là: **bit lộ → chặn nhỏ hơn → nghiệm nằm trong tầm LLL**.

## Flag

**Flag: `crypto{msb_0f_d_g1v3s_k_f0r_fr33}`**

## Nguồn

- Paper 2023/032, mục 5.2.2 (Ernst et al. 2005; Sarkar–Sen Gupta–Maitra 2010)
- Biến thể LSB với e nhỏ (BDF) đã có trong bộ RSA challenge 17
