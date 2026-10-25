# Lattice trong Mật Mã Học — Lý thuyết toàn tập

> Bản dịch - biên soạn tự do (thuần Việt) từ paper **"A Gentle Tutorial for Lattice-Based Cryptanalysis"** — Joseph Surin & Shaanan Cohney (University of Melbourne, ePrint 2023/032).
>
> Tài liệu này bao quát **mọi chủ đề về lattice** có trong paper: nền tảng hình học, thuật toán LLL, giải CVP (Babai, Kannan), ba "bài toán nền" (tìm nghiệm nhỏ — Coppersmith, bài toán balô — knapsack, bài toán số ẩn — HNP/EHNP) và các tấn công thật (RSA stereotyped message, Boneh–Durfee, partial key exposure, ECDSA với nonce xấu, Bleichenbacher bản lattice). Mỗi chứng minh khó đều được diễn giải **từng bước kèm ví dụ số**, và có một **bản đồ liên kết** ở mục cuối cho thấy tất cả ghép với nhau như thế nào.

---

## Mục lục

- [Phần 0 — Bức tranh toàn cảnh](#phần-0--bức-tranh-toàn-cảnh)
- [Phần 1 — Lattice: nền tảng hình học](#phần-1--lattice-nền-tảng-hình-học)
- [Phần 2 — Rút gọn cơ sở và thuật toán LLL](#phần-2--rút-gọn-cơ-sở-và-thuật-toán-lll)
- [Phần 3 — Giải bài toán CVP](#phần-3--giải-bài-toán-cvp)
- [Phần 4 — Ứng dụng thuần toán số: tìm đa thức tối tiểu](#phần-4--ứng-dụng-thuần-toán-số-tìm-đa-thức-tối-tiểu)
- [Phần 5 — Ba bài toán nền của tấn công lattice](#phần-5--ba-bài-toán-nền-của-tấn-công-lattice)
  - [5.1 Tìm nghiệm nhỏ của đa thức mod N (Coppersmith)](#51-tìm-nghiệm-nhỏ-của-đa-thức-mod-n--phương-pháp-coppersmith)
  - [5.2 Bài toán balô / tổng con (knapsack, subset sum)](#52-bài-toán-balô--tổng-con-knapsack-subset-sum)
  - [5.3 Bài toán số ẩn (Hidden Number Problem)](#53-bài-toán-số-ẩn-hidden-number-problem--hnp)
- [Phần 6 — Các tấn công thực tế](#phần-6--các-tấn-công-thực-tế)
- [Phần 7 — Bản đồ liên kết: tất cả ghép với nhau thế nào](#phần-7--bản-đồ-liên-kết-tất-cả-ghép-với-nhau-thế-nào)
- [Phần 8 — Luyện tập: challenge theo từng dạng](#phần-8--luyện-tập-challenge-theo-từng-dạng)
- [Phần 9 — Tài liệu tham khảo](#phần-9--tài-liệu-tham-khảo)

---

# Phần 0 — Bức tranh toàn cảnh

## 0.1 Lattice là gì, tại sao nó quan trọng trong phá mã?

Hãy tưởng tượng một **mạng lưới các điểm** trong không gian, sinh ra bằng cách lấy mọi tổ hợp *số nguyên* của vài vector cơ sở — giống như mọi ô lưới trên giấy kẻ ô vuông, nhưng các " ô" có thể bị méo thành hình bình hành bất kỳ. Đó chính là một **lattice** (dàn). Sức mạnh của lattice trong mật mã học đến từ một sự thật đơn giản:

> **Rất nhiều "bí mật" trong mật mã là những số NHỎ giấu bên trong các phương trình tuyến tính theo mô-đun lớn** — và "một số nhỏ ẩn trong một cấu trúc tuyến tính" chính là... một **vector ngắn của một lattice nào đó**.

Ví dụ: trong ECDSA, nếu nonce $k$ chỉ có vài bit cao bị lộ thì phương trình chữ ký $s k \equiv z + r d \pmod n$ trở thành một phương trình tuyến tính mod $n$ có chứa số ẩn $d$ (khóa bí mật) và số "sai số nhỏ" $k$. Người ta dựng một lattice sao cho vector chứa $d$ và các $k$ là vector **rất ngắn** so với trung bình — rồi dùng thuật toán **rút gọn cơ sở** (LLL) để moi vector ngắn đó ra. Khóa bí mật lộ.

Kể từ khi thuật toán LLL ra đời năm 1982 (Lenstra–Lenstra–Lovász), lattice đã được dùng để phá: hệ mật mã balô Merkle–Hellman (1983), LCG bị cắt cụt (1988), RSA với số mũ công khai nhỏ (Coppersmith 1996), RSA với số mũ bí mật nhỏ (Boneh–Durfee 1999), ECDSA/DSA với nonce xấu (2001), và vô số hệ thống trong thế giới thật (LadderLeak 2020, ataque TLS 2019...).

## 0.2 Giải phẫu của một tấn công lattice — pipeline 3 bước

Toàn bộ paper (và tài liệu này) xoay quanh một mô hình 4 tầng — **đây là chìa khóa để hiểu mọi thứ liên kết với nhau**:

```
┌─────────────────────────────┐
│  TẤN CÔNG MẬT MÃ (setting)  │   Ví dụ: ECDSA với nonce lệch
└──────────────┬──────────────┘
               │ BƯỚC 1: BIẾN ĐỔI (transformation)
               ▼      — viết lại phương trình mật mã
┌─────────────────────────────┐
│   BÀI TOÁN NỀN LATTICE      │   Ví dụ: bài toán số ẩn (HNP)
└──────────────┬──────────────┘
               │ BƯỚC 2: DỰNG LATTICE (lattice construction)
               ▼      — chọn cơ sở ma trận thích hợp
┌─────────────────────────────┐
│   BÀI TOÁN LATTICE          │   Ví dụ: CVP_γ / SVP_γ
└──────────────┬──────────────┘
               │ BƯỚC 3: RÚT GỌI LATTICE (lattice reduction)
               ▼      — LLL / BKZ / Babai / Kannan
┌─────────────────────────────┐
│        NGHIỆM (bí mật)      │   Ví dụ: khóa bí mật d
└─────────────────────────────┘
```

Ba điểm cần khắc cốt ghi tâm:

1. **Một bài toán nền phục vụ nhiều tấn công khác nhau.** HNP không chỉ phá ECDSA biased nonce mà còn phá LCG cụt bit, oracle đệm PKCS#1 (Bleichenbacher bản lattice), thậm chí cả việc "đoán số bị ẩn đi phần lớn" trong side-channel. Học một bài toán nền = mở được nhiều cánh cửa.
2. **Bước "dựng lattice" là nghệ thuật.** Cùng một bài toán nền có thể dựng được nhiều lattice; chọn cơ sở tốt (cân bằng kích thước các cột, thêm hệ số `embedding factor`, "cân lại" — recentering...) quyết định thành bại.
3. **Bước 3 là máy móc.** LLL chạy trong thời gian đa thức và gần như luôn tìm được vector ngắn *nếu như* vector đích thật sự ngắn hơn hẳn phần còn lại của lattice. Toàn bộ "phép màu" nằm ở việc *thiết kế* sao cho điều đó đúng.

Bảng tóm tắt các tấn công được nghiên cứu trong paper (Bảng 1 của paper):

| Bài toán nền | Tấn công | Mô tả |
|---|---|---|
| Tìm nghiệm nhỏ | RSA stereotyped message | RSA số mũ nhỏ, biết trước phần lớn bản rõ |
| Tìm nghiệm nhỏ | Boneh–Durfee | RSA với số mũ bí mật $d < N^{0.292}$ |
| Tìm nghiệm nhỏ | Partial key exposure | RSA với $d$ nhỏ + biết một phần bit của $d$ |
| Bài toán balô | ECDSA với $k = z \oplus d$ | nonce = hash thông điệp XOR khóa bí mật |
| Bài toán số ẩn (HNP) | ECDSA biased nonces | nonce bị lệch (biết/sạch MSB hoặc LSB) |
| HNP | Bleichenbacher PKCS#1 v1.5 (bản lattice) | oracle đệm PKCS, thu thập nhiều quan hệ |
| HNP mở rộng (EHNP) | ECDSA key disclosure problem | biết từng mảnh rời của nonce VÀ của khóa |

Và một số ví dụ "tuyến" cụ thể (Hình 2 của paper):

```
RSA biết bit cao của p  ──►  Tìm nghiệm nhỏ (Coppersmith)  ──┐
ECDSA nonce lệch        ──►  Bài toán số ẩn (HNP)           ├──►  SVP_γ hoặc CVP_γ  ──►  LLL/Babai  ──►  bí mật
LCG cụt bit             ──►  Bài toán số ẩn (HNP)           ──┘
```

---

# Phần 1 — Lattice: nền tảng hình học

> Tương ứng mục 3.2 của paper.

## 1.1 Định nghĩa

**Định nghĩa (Lattice).** Một lattice $n$ chiều $L$ là một **tập con rời rạc (discrete) và đóng dưới phép cộng** của $\mathbb{R}^n$ (tức một nhóm con cộng rời rạc của $\mathbb{R}^n$).

Cách xây dựng cụ thể: cho $m$ vector **độc lập tuyến tính** $b_1, \dots, b_m \in \mathbb{R}^n$, lattice do chúng sinh ra là

$$
\mathcal{L}(B) = \left\{ \sum_{i=1}^{m} a_i b_i \;\middle|\; a_i \in \mathbb{Z} \right\}
$$

— tức **mọi tổ hợp số nguyên** của các vector cơ sở. Ma trận $B$ chứa các $b_i$ viết theo **hàng** được gọi là **cơ sở** (basis) của lattice. Số vector trong cơ sở, $m$, gọi là **hạng** (rank). Khi $m = n$ ta có lattice **đầy hạng** (full-rank) — paper chủ yếu làm việc với loại này.

Ví dụ số: $b_1 = (2, 0)$, $b_2 = (1, 3)$ sinh ra mọi điểm $(x,y)$ có dạng $(2a + c,\ 3c)$ với $a, c \in \mathbb{Z}$. Điểm $(3, 3) = b_1 + b_2$, điểm $(5, -3) = 2b_1 - b_2$, v.v. Đây là một "mạng lưới" các điểm dày đặc trong mặt phẳng nhưng **rời rạc**: quanh mỗi điểm có một lân cận không chứa điểm nào khác.

Hai nhận xét nền tảng:

- Lattice **không-triết-để** luôn có **vô số điểm** (mọi $a_i$ nguyên), nhưng tất cả đều sinh hữu hạn từ cơ sở.
- **Cơ sở không duy nhất**: $\{(2,0),(1,3)\}$ và $\{(4,3),(2,0)\}$ sinh cùng một lattice, vì $(4,3) = b_1 + b_2$. Thậm chí **mọi lattice không tầm thường đều có vô số cơ sở**.

Câu hỏi then chốt: trong vô số cơ sở đó, cơ sở nào là "tốt"? Trước khi trả lời, ta cần các đại lượng **bất biến** — cái không đổi khi đổi cơ sở, giống như số đếm của một tập hợp không phụ thuộc cách ta liệt kê nó.

## 1.2 Hình bình hành cơ bản — tiêu chuẩn hình học của một cơ sở

**Định nghĩa (Hình bình hành cơ bản — fundamental parallelepiped).** Với cơ sở $B = \{b_1, \dots, b_m\}$:

$$
\mathcal{P}(B) = \left\{ \sum_{i=1}^{m} a_i b_i \;\middle|\; a_i \in [0,1) \right\}
$$

tức vùng "ô cơ bản" dựng từ các vector cơ sở với hệ số bị chặn trong $[0,1)$. Lưu ý nửa mở — không gồm biên.

Hình dung 2 chiều: hai vector $b_1, b_2$ tạo thành một hình bình hành; $\mathcal{P}(B)$ chính là hình bình hành đó.

**Tiêu chuẩn hình học:** một bộ vector là cơ sở của lattice $\Leftrightarrow$ hình bình hành cơ bản của nó **không chứa điểm lattice nào khác ngoài 0**:

$$
\mathcal{P}(B) \cap \mathcal{L} = \{0\}
$$

Vì sao? Hướng thuận trực quan: nếu $\mathcal{P}(B)$ chứa điểm lattice $c \ne 0$ thì $c$ nằm "lọt vào trong ô" — mà mọi điểm lattice đều phải là tổ hợp *số nguyên* của cơ sở; một điểm nằm gọn trong ô (hệ số $< 1$) thì không thể biểu diễn như vậy trừ khi nó là 0. Hướng ngược: nếu ô chỉ chứa 0 thì khi " lát gạch" (tile) toàn bộ $\mathbb{R}^n$ bằng các bản sao tịnh tiến của $\mathcal{P}(B)$, mỗi ô chứa đúng một điểm lattice — không dư, không thiếu — nên cơ sở phủ đủ lattice.

Đây là cách **kiểm tra bằng mắt** một bộ vector có phải cơ sở không: nhìn hình bình hành của nó, nếu có điểm lattice rơi vào trong (không tính đỉnh/gốc) thì chưa phải cơ sở.

## 1.3 Định thức của lattice — bất biến thứ nhất

**Định nghĩa (Determinant).** Với lattice đầy hạng $L = \mathcal{L}(B)$:

$$
\det(L) = \text{vol}(\mathcal{P}(B)) = |\det(B)|
$$

— thể tích $n$ chiều của hình bình hành cơ bản.

Tại sao đổi cơ sở mà thể tích không đổi? Cần một đặc tả đại số của hai cơ sở cùng lattice. Giả sử $B = \{b_1,\dots,b_n\}$ và $B' = \{b'_1,\dots,b'_n\}$ đều là cơ sở của cùng lattice $L$. Mỗi $b'_i$ nằm trong lattice nên viết được **duy nhất** dưới dạng tổ hợp nguyên của $B$:

$$
b'_1 = a_{11}b_1 + \dots + a_{1n}b_n,\quad \dots,\quad b'_n = a_{n1}b_1 + \dots + a_{nn}b_n
$$

gộp lại thành $B' = A B$ với $A$ ma trận hệ số **nguyên**. Ngược lại mỗi $b_i$ cũng là tổ hợp nguyên của $B'$, tức $B = A^{-1}B'$ nên $A^{-1}$ cũng nguyên. Do đó:

$$
\det(A)\det(A^{-1}) = \det(I) = 1,\qquad \det(A), \det(A^{-1}) \in \mathbb{Z} \;\Longrightarrow\; |\det(A)| = 1.
$$

Ma trận nguyên có định thức $\pm 1$ được gọi là **unimodular**. Ta có định lý quan trọng:

> **Định lý.** $L(B) = L(B')$ khi và chỉ khi $B = U B'$ với $U$ nguyên, $|\det U| = 1$.

Từ đó bất biến của định thức là hiển nhiên: $B = UB' \Rightarrow \det(B) = \det(U)\det(B') = \pm\det(B')$, nên $|\det B| = |\det B'|$.

**Ý nghĩa (trực quan):** dù cơ sở "méo" hay "đẹp", mỗi ô cơ bản luôn đựng đúng một điểm lattice, nên tổng thể tích chiếm của mỗi ô là như nhau — lattice có một "mật độ điểm" cố định, và $\det(L)$ chính là nghịch đảo của mật độ đó. **Lattice có định thức nhỏ = điểm dày = có nhiều vector ngắn**; định thức lớn = điểm thưa. So sánh này sẽ được dùng liên tục để ước lượng "vector ngắn chừng nào thì tìm được".

## 1.4 Các cực tiểu liên tiếp — bất biến thứ hai

Độ dài (chuẩn Euclid) của vector ngắn nhất khác 0 của lattice gọi là **cực tiểu thứ nhất** $\lambda_1(L)$. Tổng quát:

**Định nghĩa (Successive minima).** $\lambda_i(L)$ là số $r$ nhỏ nhất sao cho tồn tại $i$ vector độc lập tuyến tính trong $L$ có độ dài $\le r$.

Hình học: $\lambda_i$ là bán kính quả cầu nhỏ nhất quanh gốc chứa $i$ vector độc lập. Với $i=1$ đó là bán kính quả cầu nhỏ chạm điểm lattice gần nhất.

Sự thật đáng nhớ: **không có thuật toán hiệu quả nào tính chính xác các $\lambda_i$** (bài toán đó khó ngang SVP). Nhưng có chặn trên nổi tiếng:

> **Định lý Minkowski (dạng 1).** Với lattice đầy hạng $n$ chiều:
> $$\lambda_1(L) \le \sqrt{n}\,|\det(L)|^{1/n}$$

Diễn giải: một lattice $n$ chiều luôn *tồn tại* vector ngắn cỡ $\sqrt{n} \cdot$ "cạnh lập phương trung bình" $\det(L)^{1/n}$. Đây là **thước đo chuẩn** để phán xét vector: nếu bài toán của bạn ẩn chứa một vector ngắn hơn hẳn ngưỡng Minkowski của lattice, nó "lệch chuẩn" một cách dễ thấy — và các thuật toán rút gọn sẽ tìm ra nó. (Nguyên lý chứng minh Minkowski dùng "định lý phần thân lồi": quả cầu lồi thể tích đủ lớn chứa $\ge 2^n \det(L)$ thì buộc chứa điểm lattice khác 0 — chi tiết omit, giữ cho gentle.)

## 1.5 Các bài toán tính toán: SVP và CVP

Hai bài toán trung tâm của mọi tấn công trong tài liệu này:

> **Bài toán vector ngắn nhất (SVP — Shortest Vector Problem).** Cho cơ sở $B$ của $L = \mathcal{L}(B)$, tìm vector khác 0 $v \in L$ sao cho $\|v\| = \lambda_1(L)$.

> **Bài toán vector gần nhất (CVP — Closest Vector Problem).** Cho cơ sở $B$ của $L$ và một **vector đích** $t$ (không nhất thiết thuộc $L$), tìm $v \in L$ sao cho $\|v - t\|$ nhỏ nhất.

SVP hỏi "điểm lattice nào gần gốc nhất", CVP hỏi "điểm lattice nào gần một điểm ngoài lattice cho trước nhất". Cả hai đều **NP-khó**. May thay, dạng xấp xỉ thì khả giải:

> **SVP $\gamma$ / CVP $\gamma$**: chỉ cần tìm $v$ với $\|v\| \le \gamma \lambda_1(L)$ (tương ứng $\|v - t\| \le \gamma \cdot \min_{w\in L}\|w - t\|$), với **hệ số xấp xỉ** $\gamma$.

LLL cho lời giải **đa thức thời gian** với $\gamma$ mũ theo số chiều ($\gamma \approx 2^{n/2}$). Nghe thì tệ, nhưng trong thực hành phá mã, "vector bí mật" thường ngắn hơn hẳn mọi thứ xung quanh rất nhiều lần, nên kể cả xấp xỉ thô vẫn bắt được nó.

**Cách đọc mọi tấn công về sau:** mỗi tấn công = một cách dịch bài toán mật mã thành SVP $_\gamma$/CVP $_\gamma$ trên một lattice được thiết kế, sao cho nghiệm bí mật chính là vector ngắn/gần nhất đó.

---

# Phần 2 — Rút gọn cơ sở và thuật toán LLL

> Tương ứng mục 3.4 của paper.

## 2.1 Ý tưởng: "cắt gọt" cơ sở

**Rút gọn cơ sở (lattice reduction)** = biến một cơ sở bất kỳ thành cơ sở *cùng lattice* nhưng **ngắn hơn và gần vuông góc hơn**. Vì hàng đầu của cơ sở sau rút gọn là vector khá ngắn, bản thân việc rút gọn đã là lời giải xấp xỉ cho SVP.

Nhưng ta được phép biến đổi cơ sở bằng những phép nào? Nhắc lại Định lý ở mục 1.3: hai cơ sở liên hệ qua ma trận unimodular $U$ ($|\det U| = 1$). Hai phép biến đổi nguyên cơ sinh ra mọi ma trận unimodular:

1. **Hoán vị vector** — nhân trái với $T_{i,j}$ (đổi hàng $i$ và $j$), $\det = -1$.
2. **Cộng vector** — nhân trái với $L_{i,j}(k)$ (cộng $k$ lần hàng $j$ vào hàng $i$), $\det = 1$.

Đây chính là các **phép biến đổi hàng nguyên** quen thuộc (giống khử Gauss, nhưng chỉ được dùng hệ số *nguyên* — không chia, không nhân tỷ lệ). LLL là một chuỗi khéo léo của hai phép này.

## 2.2 Trực giao hóa Gram–Schmidt

LLL cần một "thước đo trực giao" — bộ các vector trực giao $b^*_1, \dots, b^*_n$ đồng hành với cơ sở:

$$
b^*_i = b_i - \sum_{j=1}^{i-1} \mu_{i,j} b^*_j, \qquad \mu_{i,j} = \frac{\langle b_i, b^*_j\rangle}{\langle b^*_j, b^*_j\rangle}
$$

Ý nghĩa: $b^*_i$ là phần của $b_i$ **vuông góc** với không gian span của $b_1, \dots, b_{i-1}$; $\mu_{i,j}$ là "độ nghiêng" của $b_i$ theo hướng $b^*_j$. Các $b^*_i$ **không** thuộc lattice (hệ số $\mu$ thực, không nguyên) — chúng chỉ là công cụ đo.

Ví dụ số (sẽ chạy suốt phần này): $b_1 = (-2, 2)$, $b_2 = (-2, 1)$.

$$
b^*_1 = b_1 = (-2, 2)
$$
$$
b^*_2 = b_2 - \frac{\langle b_2, b^*_1\rangle}{\langle b^*_1, b^*_1\rangle} b^*_1
= (-2,1) - \frac{4 + 2}{4+4}(-2,2) = (-2,1) - 0{,}75(-2,2) = (-0{,}5, -0{,}5)
$$
$$
\mu_{2,1} = \frac{6}{8} = 0{,}75
$$

Cách đọc: $b_2$ nghiêng $0{,}75$ theo hướng $b_1$ — khá "xiên". Một cơ sở đẹp là cơ sở gần vuông góc, tức các $|\mu_{i,j}| \le 1/2$.

## 2.3 Cơ sở LLL-reduced là gì?

**Định nghĩa ($\delta$-LLL-reduced).** Cơ sở $\{b_1, \dots, b_n\}$ là $\delta$-LLL-reduced ($\delta \in (1/4, 1)$, thường lấy $3/4$) nếu:

1. **Size-reduced:** $|\mu_{i,j}| \le 1/2$ với mọi $i > j$ — các vector không nghiêng quá $30°$ so với các hướng trước;
2. **Điều kiện Lovász:** $(\delta - \mu^2_{i+1,i})\|b^*_i\|^2 \le \|b^*_{i+1}\|^2$ với mọi $i$ — theo trình tự trực giao, vector sau không được ngắn quá một mức so với vector trước.

Điều kiện (1) một mình chưa đủ: cơ sở có thể size-reduced nhưng $b_1$ dài lũ lũ (lấy $b_1$ dài, $b_2$ chỉ hơi nghiêng theo nó). Điều kiện (2) "phạt" tình trạng lệch cục bộ giữa hai vector liên tiếp, buộc các độ dài $\|b^*_i\|$ phải giảm **đều** từ trên xuống. Kết hợp lại, một cơ sở LLL-reduced có các vector ngắn, gần vuông góc, và **hàng đầu tiên rất ngắn**.

## 2.4 Thuật toán LLL

```
LLL(B = {b1..bn}, δ):
  lặp mãi:
    1) SIZE-REDUCE: với mỗi i = 2..n, với mỗi j = i-1..1:
         tính μi,j (từ Gram–Schmidt hiện tại)
         bi ← bi − ⌊μi,j⌉ · bj        # làm |μi,j| ≤ 1/2
    2) nếu tồn tại i sao cho (δ − μ²i+1,i)‖b*i‖² > ‖b*i+1‖²:
         đổi chỗ bi và bi+1            # Lovász thất bại → swap, lặp lại
       ngược lại:
         trả về {b1..bn}               # đã LLL-reduced
```

Hai nguyên liệu: khử kích thước (trừ đi bội *nguyên* gần nhất để giảm độ nghiêng — phép biến đổi unimodular) và swap khi Lovász thất bại (cũng unimodular). Thuật toán bảo đảm dừng sau hữu hạn bước và chạy **đa thức theo chiều** $n$ (với số nguyên có độ dài cố định; tổng quát đa thức theo bit-size).

### Chạy tay ví dụ 2D (Ví dụ 3.12 của paper)

Đầu vào $b_1 = (-2,2)$, $b_2 = (-2,1)$, $\delta = 0{,}75$. Các bước Gram–Schmidt đã tính ở mục 2.2: $\mu_{2,1} = 0{,}75$.

**Vòng 1 — size-reduce:** $\lfloor 0{,}75 \rceil = 1$ nên

$$
b_2 \leftarrow b_2 - 1 \cdot b_1 = (-2,1) - (-2,2) = (0, -1)
$$

**Kiểm tra Lovász** giữa $b^*_1 = (-2,2)$ và $b^*_2 = (-0{,}5,-0{,}5)$:

$$
(\delta - \mu^2_{2,1})\|b^*_1\|^2 = (0{,}75 - 0{,}5625)\cdot 8 = 1{,}5 \quad>\quad 0{,}5 = \|b^*_2\|^2
$$

— thất bại (vector sau "ngắn quá bất thường") → **swap**: $b_1 = (0,-1)$, $b_2 = (-2,2)$.

**Vòng 2 — Gram–Schmidt mới:** $b^*_1 = (0,-1)$; $\mu_{2,1} = \frac{\langle(-2,2),(0,-1)\rangle}{1} = -2$; $b^*_2 = (-2,2) - (-2)(0,-1) = (-2, 0)$.

**Size-reduce:** $\lfloor -2 \rceil = -2$, nhưng $b_2 - (-2)b_1 = (-2,2) - (0,2) = (-2,0)$... thực ra ở đây $\mu_{2,1} = -2$ nguyên nên $|\mu| \le 1/2$? Không — $|-2| > 1/2$, vậy vẫn khử: $b_2 \leftarrow b_2 - (-2)\,b_1 = (-2, 2) + 2(0,-1) = (-2, 0)$.

**Kiểm tra Lovász:** $(0{,}75 - (-2)^2)\cdot 1 = -3{,}25 \le 0 = \|b^*_2\|^2$ — thỏa (vế trái âm thì hiển nhiên đúng).

**Kết thúc.** Cơ sở LLL-reduced: $b'_1 = (0,-1)$, $b'_2 = (-2,0)$ — hai vector đơn vị trực giao, đẹp hoàn hảo. Vector ngắn nhất của lattice là $b'_1 = (0,-1)$, đúng $\lambda_1 = 1$.

Nhận xét: LLL **không luôn** tìm được vector ngắn nhất như thế này; nó chỉ cam kết tìm vector trong *hệ số xấp xỉ mũ*. Nhưng với lattice nhỏ/vừa và vector đích "ngắn bất thường" (như mọi bài CTF), LLL thường ăn khớp.

## 2.5 Chứng minh cận dưới: $\lambda_1 \ge \min_i \|b^*_i\|$

> **Định lý 3.13 của paper.** Với mọi cơ sở $B$ và Gram–Schmidt $B^*$: $\lambda_1(L(B)) \ge \min_{i} \|b^*_i\|$.

Ý nghĩa: các vector trực giao Gram–Schmidt "chặn dưới" độ dài vector ngắn nhất — không thể có điểm lattice nào ngắn hơn vector GS ngắn nhất. Chứng minh từng bước:

*Bước 1.* Lấy điểm lattice bất kỳ $xB = \sum_i x_i b_i \ne 0$ với $x \in \mathbb{Z}^n$. Gọi $j$ là **chỉ số lớn nhất** có $x_j \ne 0$ (các $x_i = 0$ với $i > j$).

*Bước 2.* Tích trong với $b^*_j$:

$$
\langle xB, b^*_j \rangle = \sum_{i=1}^{n} x_i \langle b_i, b^*_j \rangle
$$

*Bước 3.* Hai tính chất của Gram–Schmidt: (a) $b_i$ với $i < j$ là tổ hợp tuyến tính của $b^*_1..b^*_{j-1}$ nên trực giao với $b^*_j$ — rút gọn tổng còn đúng số hạng $i = j$; (b) theo công thức $b_j = b^*_j + \sum_{k<j}\mu_{j,k}b^*_k$ nên $\langle b_j, b^*_j\rangle = \langle b^*_j, b^*_j\rangle = \|b^*_j\|^2$. Kết quả:

$$
\langle xB, b^*_j \rangle = x_j \|b^*_j\|^2
$$

*Bước 4.* Bất đẳng thức Cauchy–Schwarz: $|\langle xB, b^*_j\rangle| \le \|xB\| \cdot \|b^*_j\|$, suy ra

$$
|x_j| \cdot \|b^*_j\|^2 \le \|xB\| \cdot \|b^*_j\| \;\Longrightarrow\; |x_j|\,\|b^*_j\| \le \|xB\|
$$

*Bước 5.* Vì $x_j$ nguyên khác 0 nên $|x_j| \ge 1$, do đó $\|b^*_j\| \le \|xB\|$. Mà $j$ tùy ý (do $xB$ tùy ý), nên với mọi điểm lattice khác 0 đều có $\min_i \|b^*_i\| \le \|xB\|$. Chọn $xB$ là vector ngắn nhất: $\lambda_1 \ge \min_i \|b^*_i\|$. $\blacksquare$

Kiểm tra bằng ví dụ 2D trên: cơ sở gốc có $\|b^*_2\| = \|(-0{,}5,-0{,}5)\| \approx 0{,}707$... vậy $\lambda_1 \ge 0{,}707$; thực tế $\lambda_1 = 1$ — khớp.

## 2.6 Chặn trên: LLL tìm được vector ngắn cỡ nào?

> **Định lý lý tưởng 3.14.** Cơ sở $\delta$-LLL-reduced có $\|b_1\| \le \left(\frac{2}{\sqrt{4\delta - 1}}\right)^{n-1} \lambda_1$.

Chứng minh theo paper:

*Bước 1.* Từ điều kiện Lovász: $(\delta - \mu^2_{i+1,i})\|b^*_i\|^2 \le \|b^*_{i+1}\|^2$.

*Bước 2.* Từ size-reduce: $|\mu_{i+1,i}| \le 1/2 \Rightarrow \mu^2 \le 1/4$, nên vế trái nhỏ nhất khi $\mu^2$ lớn nhất:

$$
\left(\delta - \tfrac14\right)\|b^*_i\|^2 \le \|b^*_{i+1}\|^2
$$

*Bước 3.* Chuỗi hóa bất đẳng thức từ $1$ tới $i$:

$$
\|b^*_1\|^2 \le \left(\frac{4}{4\delta-1}\right)^{i-1} \|b^*_i\|^2
$$

*Bước 4.* Chú ý $\|b^*_1\| = \|b_1\|$ (vector đầu không bị trừ gì). Đưa lên tới $i = n$ và kết hợp với Định lý 2.5 ($\|b^*_n\| \le \lambda_1$... chặt hơn: $\min_i \|b^*_i\| \le \lambda_1$, và từ chuỗi trên $\|b_1\| \le (\cdot)^{n-1}\|b^*_n\| \le (\cdot)^{n-1} \min_i \|b^*_i\| \cdot(\text{hệ số})$ — ở đây paper dùng trực tiếp $\|b^*_n\| \le \max$... bản gốc: $\|b^*_n\|$ không nhất thiết là min; cách viết chặt của paper là chuỗi tới $n$ rồi dùng Lemma 3.13):

$$
\|b_1\| \le \left(\frac{2}{\sqrt{4\delta-1}}\right)^{n-1} \lambda_1
$$

Với $\delta = 3/4$: $\frac{2}{\sqrt{4\cdot 0{,}75 - 1}} = \frac{2}{\sqrt 2} = \sqrt 2$, nên **$\|b_1\| \lesssim (\sqrt2)^{\,n-1}\,\lambda_1 \approx 2^{0{,}25 n}\,\lambda_1$** — hệ số xấp xỉ hàm mũ theo chiều, đúng như lời đồn.

*Bước cuối — ghép với Minkowski:* thay $\lambda_1 \le \sqrt n \det(L)^{1/n}$ vào:

> **Hệ quả 3.15 (công thức "ngón tay cái" của LLL).**
> $$\|b_1\| \le \left(\frac{2}{\sqrt{4\delta-1}}\right)^{n-1} \sqrt{n}\,|\det(L)|^{1/n}$$

**Đây là công cụ ước lượng quan trọng nhất của toàn bộ tài liệu.** Cách dùng khi thiết kế tấn công:

1. Dựng lattice cho bài toán của mình, tính $\det(L)$ và chiều $n$.
2. Tính **ngưỡng LLL** $= (\sqrt2)^{n-1}\sqrt n \det^{1/n}$ (hoặc thực tế hơn: heuristic $\approx 1{,}02^n \det^{1/n}$ của Nguyen–Stehlé cho lattice ngẫu nhiên).
3. So sánh với **độ dài vector bí mật** $\|v_{\text{secret}}\|$ đã ước lượng. Nếu $\|v_{\text{secret}}\| \ll$ ngưỡng → LLL gần như chắc chắn tìm được nó. Nếu chỉ hơi nhỏ hơn → rủi ro, cân nhắc BKZ hoặc dùng thêm "brute force vài bit cuối".

Ví dụ tính nhanh: lattice chiều $n = 40$, $\det = 2^{400}$ → $\det^{1/n} = 2^{10}$, ngưỡng lý thuyết $\approx 2^{10} \cdot 2^{0{,}25 \cdot 39} \approx 2^{20}$; heuristic thực tế $\approx 1{,}02^{40} \cdot 2^{10} \approx 2^{11}$. Nếu vector bí mật dài $\sim 2^8$ → dư địa lớn, yên tâm chạy.

## 2.7 Vượt xa LLL: BKZ (ngoài paper, để dùng thực tế)

LLL chỉ là "tầng 1". **BKZ** dùng chính LLL làm sub-routine trên các khối trượt (block) kích thước $\beta$ và giải SVP chính xác trong từng khối — chất lượng tăng theo $\beta$ (15–20 = gần LLL; 30–45 = rất mạnh cho CTF; $\beta \to n$ = SVP chính xác). Khi LLL "gần thành công" (vector ra có hình dạng đúng nhưng sai vài chỗ), nâng lên `BKZ(block_size=20..30)` thường cứu được. Trong fpylll: `BKZ.reduction(B, BKZ.Param(block_size))`; Sage: `M.BKZ(block_size=...)`.



---

# Phần 3 — Giải bài toán CVP

> Tương ứng mục 3.5 của paper. SVP dùng trực tiếp hàng đầu của cơ sở rút gọn; CVP cần thêm một lớp kỹ thuật. Hai công cụ: **Babai** (đi trực tiếp) và **Kannan** (biến CVP thành SVP).

## 3.1 Thuật toán mặt phẳng gần nhất của Babai (1986)

**Ý tưởng:** quy nạp theo chiều. Với cơ sở đã rút gọn $\{b_1, \dots, b_n\}$ và đích $t$:

1. Nhìn **siêu mặt phẳng** (hyperplane) lưới gồm các mặt phẳng $z\,b^*_n + \text{span}(b_1..b_{n-1})$, $z \in \mathbb{Z}$ — chúng "lát" không gian thành các tầng song song. Chọn tầng gần $t$ nhất: hệ số $c_n = \left\lceil \frac{\langle t, b^*_n\rangle}{\langle b^*_n, b^*_n\rangle} \right\rfloor$ (làm tròn), rồi tịnh tiến đích $t' = t - c_n b_n$ — giờ $t'$ nằm "giữa" tầng đó.
2. Lặp lại quy nạp trong không gian $n-1$ chiều với $t'$ và $b_1..b_{n-1}$.
3. Tổng $c_1 b_1 + \dots + c_n b_n$ chính là điểm lattice gần $t$ (xấp xỉ).

```
Babai(B = {b1..bn}, t):
  rút gọn B (LLL/BKZ)
  tính Gram–Schmidt b*1..b*n
  w ← t
  for i = n down to 1:
      ci ← ⌈⟨w, b*i⟩ / ⟨b*i, b*i⟩⌋      # làm tròn hệ số theo hướng trực giao
      w ← w − ci·bi                       # bắn đích vào "tầng" thứ i
  trả về t − w                            # điểm lattice tìm được
```

Bản chất là "làm tròn thông minh theo hướng trực giao" thay vì làm tròn ngây thơ theo tọa độ. Độ chính xác phụ thuộc chất lượng cơ sở: dùng LLL thì giải được CVP $_\gamma$ với $\gamma$ mũ theo $n$ — đủ cho hầu hết bài CTF.

**Ví dụ số nhỏ:** lattice cơ sở $b_1 = (2, 1)$, $b_2 = (1, 3)$ (đã khá đẹp), đích $t = (3{,}7,\ 2{,}2)$.

- Gram–Schmidt: $b^*_1 = (2,1)$; $\mu_{2,1} = \frac{1\cdot2 + 3\cdot1}{5} = 1$; $b^*_2 = (1,3) - (2,1) = (-1, 2)$.
- $i = 2$: $c_2 = \lceil\langle(3{,}7,2{,}2),(-1,2)\rangle / 5\rceil = \lceil(-3{,}7+4{,}4)/5\rceil = \lceil 0{,}14 \rceil = 0$; $w$ giữ nguyên.
- $i = 1$: $c_1 = \lceil\langle(3{,}7,2{,}2),(2,1)\rangle/5\rceil = \lceil(7{,}4+2{,}2)/5\rceil = \lceil1{,}92\rceil = 2$; $w = t - 2(2,1) = (-0{,}3, 0{,}2)$.
- Nghiệm: $v = t - w = (4, 2) = 2b_1 + 0b_2$. Kiểm tra: khoảng cách $\|(3{,}7,2{,}2)-(4,2)\| \approx 0{,}36$ — thực sự là điểm lattice gần nhất.

## 3.2 Phương pháp nhúng của Kannan (1987)

**Ý tưởng:** biến CVP thành SVP bằng cách "gắn" vector đích vào lattice, nâng lên $n+1$ chiều.

Giả sử nghiệm CVP là $v = \sum_i c_i b_i$ gần $t$, tức $t = v + e$ với $\|e\|$ nhỏ. Xét lattice $(n+1)$ chiều với cơ sở:

$$
B' = \begin{pmatrix} B & 0 \\ t & q \end{pmatrix}
$$

 với $q$ nguyên dương gọi là **hệ số nhúng** (embedding factor). Tổ hợp $(-c_1, \dots, -c_n, 1)$ sinh ra vector:

$$
(-c_1,\dots,-c_n,1)\,B' = (-v + t,\ q) = (e,\ q)
$$

— một vector **ngắn** của lattice mới! Rút gọn $B'$, tìm $(e, q)$ (hoặc âm của nó $(-e, -q)$), rồi $v = t - e$ chính là nghiệm CVP.

**Chọn $q$:** phải cân đối với $\|e\|$ kỳ vọng (thường $q \approx \|e\|$ hoặc nhỏ hơn chút). $q$ quá lớn → vector $(e,q)$ không còn "ngắn bất thường"; $q$ quá nhỏ → bị lẫn với vector khác. Trong các bài HNP thực tế người ta thường thử một dải giá trị $q$ (sweep). Tham khảo chi tiết: Galbraith (2012), Sun và cộng sự (2021).

**Khi nào dùng Babai, khi nào dùng Kannan?** Cùng giải CVP $_\gamma$; kinh nghiệm CTF: thử Kannan/embedding trước (SVP bằng LLL thường "sạch" hơn Babai), nếu ra garbage thì quay lại Babai hoặc chỉnh $q$ / cân lại các cột.

---

# Phần 4 — Ứng dụng thuần toán số: tìm đa thức tối tiểu

> Mục 3.6 của paper — ví dụ "làm quen" đầu tiên: dùng lattice ngoài mật mã, khôi phục một cấu trúc đại số từ con số thập phân xấp xỉ (Kannan–Lenstra–Lovász 1984).

**Bài toán.** Cho $\beta \approx 8{,}70997594$ (8 chữ số thập phân) — xấp xỉ của $\alpha = 7 + \sqrt[3]{5}$. Tìm **đa thức tối tiểu** (minimal polynomial) của $\alpha$: đa thức monic bậc thấp nhất hệ số nguyên có $\alpha$ là nghiệm.

**Bước 1 — viết phương trình "gần đúng" tuyến tính theo hệ số.** Nghi ngờ $f$ bậc 3: $f(x) = a_0 + a_1 x + a_2 x^2 + a_3 x^3$ với $f(\alpha) = 0$. Vì $\beta \approx \alpha$ nên $f(\beta) \approx 0$. Để làm việc trên số nguyên, nhân $10^8$:

$$
10^8 a_0 + \lfloor 10^8 \beta\rfloor a_1 + \lfloor 10^8 \beta^2\rfloor a_2 + \lfloor 10^8 \beta^3\rfloor a_3 \approx 0
$$

Cụ thể: $10^8\beta = 870997594$, $10^8\beta^2 = 7586368087$, $10^8\beta^3 = 66077083514$.

**Bước 2 — dựng lattice** sao cho vector hệ số là vector ngắn:

$$
B = \begin{pmatrix}
10^8 & 1 & 0 & 0\\
870997594 & 0 & 1 & 0\\
7586368087 & 0 & 0 & 1\\
66077083514 & 0 & 0 & 0
\end{pmatrix}
$$

Ba hàng đầu = "phương trình gần đúng" (cột 0) + chốt nhận diện $a_1, a_2, a_3$ (khối đơn vị); hàng cuối... chú ý cấu trúc: tổ hợp $t = (a_0, a_1, a_2, a_3) \cdot B$ cho ra $(\,\underbrace{\approx 0}_{\text{số lớn triệt tiêu}},\ a_1,\ a_2,\ a_3)$. Tức là **vector hệ số nằm trong lattice và có tọa độ đầu gần 0** — nó là vector ngắn!

**Bước 3 — kiểm tra bằng công thức ngón tay cái.** Giả sử biết chặn cao (height) $M = 400$ cho các hệ số: $\|v_{\text{đích}}\| \approx \sqrt{3M^2} = 692$. Còn LLL tìm được vector ngắn cỡ (chiều 4, $\delta = 3/4$, $\det B = 10^8$):

$$
\|b_1\| \lesssim (\sqrt 2)^3 \sqrt 4 \cdot (10^8)^{1/4} = 2\sqrt2 \cdot 2 \cdot 100 = 566 \quad (\text{paper tính }\approx 2868 \text{ bằng chặn chặt hơn})
$$

— ngưỡng ≥ độ dài vector đích → có lý do tin LLL tìm được.

**Bước 4 — chạy LLL** (kết quả trong paper):

$$
B' = \begin{pmatrix}
5 & -348 & 147 & -21\\
438 & -75 & 116 & 188\\
109 & -214 & -563 & -159\\
357 & 136 & 220 & -419
\end{pmatrix}
$$

Hàng đầu có số đầu tiên là $5 \approx 0$ (so với $10^8$) — đó chính là vector đích! Đọc hệ số: $a_0 = -348,\ a_1 = 147,\ a_2 = -21,\ a_3 = 1$ (monic hóa):

$$
f(x) = x^3 - 21x^2 + 147x - 348
$$

Kiểm chứng: $f(7 + \sqrt[3]5) = 0$ thật (thử trực tiếp: $(7+\sqrt[3]5)^3 = 343 + 147\sqrt[3]5 + 21\sqrt[3]{25} + 5$; $-21(49 + 14\sqrt[3]5 + \sqrt[3]{25}) + 147(7 + \sqrt[3]5) - 348$ cộng lại triệt tiêu sạch).

**Bài học rút ra (mẫu chung của MỌI tấn công lattice):**

| Thành phần | Trong ví dụ này | Tương đồng trong mật mã |
|---|---|---|
| Thông tin biết trước | $\beta \approx \alpha$ tới 8 số | bit bị lộ của nonce, phần biết của bản rõ... |
| Phương trình tuyến tính | $10^8 a_0 + \dots + a_3 \approx 0$ | $s_i k_i - z_i - r_i d \equiv 0 \pmod n$... |
| Số nhỏ ẩn | hệ số $a_i \le 400$ | khóa $d$, bit nonce, phần bản rõ thiếu |
| Vector đích ngắn | $(\approx 0, a_1, a_2, a_3)$ | $(k_1, \dots, k_\ell, \alpha B/p, -B)$ |
| Thuật toán | LLL | LLL/BKZ |



---

# Phần 5 — Ba bài toán nền của tấn công lattice

> Mục 4 của paper. Đây là "tầng giữa" của pipeline: nhận bài toán mật mã đã biến đổi, xuất ra SVP $_\gamma$/CVP $_\gamma$. Các bài toán này có đặc điểm chung: **tính tuyến tính + một hứa hẹn "cái gì đó nhỏ"**.

## 5.1 Tìm nghiệm nhỏ của đa thức mod N — phương pháp Coppersmith

> Mục 4.1 của paper. Một trong những kết quả ảnh hưởng nhất của mật mã công khai thập niên 90 (Coppersmith 1996): tìm nghiệm **nhỏ** của phương trình đa thức modulo số **hợp số** mà không cần biết phân tích thừa số.

Tại sao đáng tiền? Nghiệm mod nguyên tố dễ (Sage giải ngay); nghiệm mod hợp số nói chung khó ngang phân tích $N$. Coppersmith chiếm vùng giữa: nghiệm **nhỏ hơn ngưỡng** $N^{1/\delta}$ (với đa thức monic bậc $\delta$) thì tìm được mà không cần factor.

### 5.1.1 Bản chất: "tìm đa thức hệ số nhỏ cùng nghiệm"

Cho $N$ hợp số, $f(x) = x^d + \sum_{i<d} a_i x^i \in \mathbb{Z}[x]$ **monic** bậc $d$. Muốn tìm nghiệm $x_0$ của $f(x_0) \equiv 0 \pmod N$ với $|x_0| < B$.

Chìa khóa: nếu tìm được đa thức $h(x) \in \mathbb{Z}[x]$ **cùng nghiệm $x_0$ nhưng thoát khỏi mô-đun** — tức $h(x_0) = 0$ trên số nguyên — thì nghiệm tìm bằng các thuật toán chuẩn (căn của đa thức trên $\mathbb{Z}$). Làm thế nào? Hai quan sát:

1. Cộng thêm bội của $N$: $g_i(x) = N x^i$ cũng có nghiệm $x_0$ mod $N$. Vậy **mọi tổ hợp nguyên** của $f$ và các $g_i$ đều chia sẻ nghiệm $x_0$ mod $N$.
2. Nếu $h(x_0)$ nhỏ hơn $N$ tuyệt đối thì từ $N \mid h(x_0)$ buộc $h(x_0) = 0$ **trên nguyên**. Muốn $|h(x_0)| < N$ với $|x_0| < B$, đủ (không cần thiết) là mỗi số hạng $|h_i x_0^i| < N/(d+1)$.

Vậy cần một đa thức $h$ trong "không gian đa thức cùng nghiệm" mà **hệ số nhỏ** — lại là bài toán tìm vector ngắn! Dựng lattice (hàng = đa thức, viết theo hệ số của $h(Bx)$):

$$
\mathsf{B} = \begin{pmatrix}
N & & & &\\
& BN & & &\\
& & B^2 N & &\\
& & & \ddots &\\
a_0 & a_1 B & a_2 B^2 & \cdots & B^d
\end{pmatrix}
$$

Hàng $i$ (0-index, $0 \le i < d$) mã hóa $g_i(Bx) = N (Bx)^i$; hàng cuối mã hóa $f(Bx)$. Cột $i$ nhân sẵn $B^i$ để các hệ số "chuẩn hóa" về cùng thước đo. **Lattice tam giác** nên định thức tính ngay:

$$
\det(\mathcal{L}) = N^d \cdot B^{0+1+\dots+d} = N^d B^{d(d+1)/2}
$$

Chiều $n = d+1$. Theo công thức ngón tay cái (Hệ quả 3.15, $\delta = 3/4$):

$$
\|b_1\| \lesssim 2^{d/2}\sqrt{d+1}\cdot \left(N^d B^{d(d+1)/2}\right)^{1/(d+1)} = 2^{d/2}\sqrt{d+1}\cdot B^{d/2}\, N^{d/(d+1)}
$$

Yêu cầu thành công: mỗi hệ số $|h_i| \le \|b_1\| < N/(d+1)$. Bỏ hệ số đa thức nhỏ, điều kiện tinh thần là $B^{d/2} N^{d/(d+1)} \lesssim N$, giải ra:

$$
B \lesssim N^{2/(d(d+1))} \quad\xrightarrow{\ d\ \text{lớn}\ }\quad B < N^{1/d}
$$

Ví dụ $d = 2$: $B < N^{1/4}$; $d = 3$: $B < N^{1/9}$... trông thấp, nhưng với bài RSA ($N$ 1024 bit) thì "phần nhỏ" vài chục đến vài trăm bit — quá đủ cho các tấn công phần-bản-rõ-biết-trước.

**Quy trình giải:**

1. Dựng $\mathsf{B}$ như trên (với $B$ = chặn trên ước lượng của nghiệm);
2. LLL cơ sở, lấy **hàng đầu** $b_1 = (b_0, b_1, \dots, b_d)$;
3. Hiệu chỉnh scale: $h(x) = b_0 + \frac{b_1}{B}x + \frac{b_2}{B^2}x^2 + \dots + x^d$;
4. Tìm nghiệm nguyên của $h$ (Newton/b+công thức căn bậc 2/sympy), kiểm tra lại mod $N$.

### 5.1.2 Ví dụ chạy tay đầy đủ (Ví dụ 4.1 của paper)

$N = 23 \cdot 29 = 667$, $f(x) = x^2 + 6x + 352$, nghiệm nhỏ $x_0 = 15$ ($f(15) = 225 + 90 + 352 = 667 \equiv 0$; nhưng $f(15) \ne 0$ trên nguyên). Chọn $B = 20 > 15$. Lattice ($d = 2$, 3 hàng):

$$
\mathsf{B} = \begin{pmatrix}
N & 0 & 0\\
0 & BN & 0\\
a_0 & a_1 B & B^2
\end{pmatrix}
= \begin{pmatrix}
667 & 0 & 0\\
0 & 13340 & 0\\
352 & 120 & 400
\end{pmatrix}
$$

LLL cho cơ sở rút gọn:

$$
\mathsf{B}' = \begin{pmatrix}
-315 & 120 & 400\\
352 & 120 & 400\\
167 & 12260 & -3600
\end{pmatrix}
$$

Đọc hàng đầu: $h(Bx) = 400x^2 + 120x - 315$, hoàn nguyên scale về:

$$
h(x) = \frac{400}{20^2}x^2 + \frac{120}{20}x - 315 = x^2 + 6x - 315
$$

Nghiệm nguyên: $x^2 + 6x - 315 = 0 \Leftrightarrow (x-15)(x+21) = 0 \Rightarrow x_0 = 15$ ✓ (và $-21$, bị loại vì $|-21| > B$).

### 5.1.3 Các mở rộng (trích kết quả chính, không chứng minh)

> **Định lý 4.2 (Coppersmith tổng quát).** $N$ có ước $b \ge N^\beta$ (không cần biết $b$), $f$ monic bậc $\delta$ chặn nghiệm... thì tìm được mọi $x_0$ với $|x_0| \le \frac12 N^{\beta^2/\delta}$ trong thời gian đa thức.

Trường hợp dùng nhiều nhất: **$\beta = 1/2$** — tức $b$ là ước cỡ $\sqrt N$ (đúng bằng một thừa số nguyên tố của RSA!) cho $|x_0| \le \frac12 N^{1/(4\delta)}$. Đây chính là gốc của tấn công "biết bit cao của $p$": $p = p_{\text{cao}} + x_0$, $f(x) = p_{\text{cao}} + x$ monic hóa, nghiệm nhỏ $x_0 < N^{1/4}$ tìm được.

> **Định lý 4.3 (Coppersmith 2 biến trên nguyên — Coron 2007).** $f(x,y) \in \mathbb{Z}[x,y]$ bất khả quy bậc $\delta$, chặn nghiệm $|x_0| \le X, |y_0| \le Y$, đặt $W = \max |f_{i,j}| X^i Y^j$. Nếu $XY < W^{1/\delta}$ thì tìm được $(x_0, y_0)$.

> **Đa biến (heuristic).** Dựng lattice lớn hơn với các *shift polynomial* (thêm lũy thừa $f$ và $N$), sau rút gọn lấy **nhiều hàng ngắn** ra nhiều đa thức cùng nghiệm; giải hệ bằng **basis Gröbner** hoặc **resultant**. Không có bảo đảm đại số (các đa thức có thể phụ thuộc), nhưng thực tế chạy tốt — toàn bộ Boneh–Durfee, stereotyped nhiều phần ẩn, short-pad attack... đứng trên nền này.

Công cụ phân tích chặn cho đa biến:

> **Định lý 4.4 (Howgrave-Graham 1997).** Với $h$ gồm $\omega$ đơn thức: nếu (1) $f(r) \equiv 0 \pmod N$ với $|r_i| < X_i$, và (2) $\|h(x_1 X_1, \dots)\| < N/\sqrt\omega$ thì $f(r) = 0$ **trên nguyên**.

(Đây là bản chặt chẽ của lập luận "$h(x_0) < N \Rightarrow h(x_0) = 0$" ở trên: chuẩn nhỏ hơn $N/\sqrt\omega$ đủ chặn mọi $|h(r)| < N$ theo Cauchy–Schwarz.)

**Trong thực hành CTF:** dùng `small_roots` của Sage (`f.small_roots(X=..., beta=..., epsilon=...)`) hoặc thư viện `coppersmith` của Python; tự dựng chỉ khi cần tùy biến shift.

## 5.2 Bài toán balô / tổng con (knapsack, subset sum)

> Mục 4.2 của paper. Bài toán NP-đầy đủ "cổ nhất" được dùng làm cửa sập mật mã (Merkle–Hellman 1978) — và cũng là nạn nhân đầu tiên của LLL (Adleman 1983, Lagarias–Odlyzko 1985).

### 5.2.1 Định nghĩa và mật độ

> **Bài toán tổng con (subset sum).** Cho trọng số dương $a_1, \dots, a_n$ và đích $s$; tìm $e_i \in \{0,1\}$ sao cho $\sum_i e_i a_i = s$.

**Mật độ** (density) đo "chật" của instance:

$$
d = \frac{n}{\log_2 \max(a_i)}
$$

Trực giác: nếu các $a_i$ dài $\ell$ bit, có $2^n$ tổ hợp rơi vào khoảng giá trị cỡ $2^\ell$; $d < 1$ nghĩa là tổ hợp ít hơn giá trị — nghiệm gần như **duy nhất**. Nghịch lý đáng yêu: nghiệm duy nhất lại chính là điều kiện để lattice tấn công thành công (vector đích là vector ngắn **duy nhất**). Hai mốc lịch sử:

- **Lagarias–Odlyzko 1985 (LO):** giải được $d < 0{,}6463$ với oracle SVP.
- **Coster–Joux–LaMacchia–Odlyzko 1992 (CJLOSS):** tinh chỉnh lattice, nâng lên $d < 0{,}9408$.

### 5.2.2 Lattice LO và CJLOSS

**Lattice LO (đơn giản):**

$$
B = \begin{pmatrix}
1 & & & & a_1\\
& 1 & & & a_2\\
& & \ddots & & \vdots\\
& & & 1 & a_n\\
& & & & s
\end{pmatrix}
$$

Tổ hợp $t = (e_1, \dots, e_n, -1)$ cho $tB = (e_1, \dots, e_n,\ \sum e_i a_i - s) = (e_1,\dots,e_n, 0)$ — vector toàn 0/1, **ngắn** (chuẩn $\le \sqrt n$) và có cột cuối = 0. Kỳ vọng LLL tìm nó.

**Lattice CJLOSS (tốt hơn):** "gốc" hệ số về giữa khoảng $[0,1]$ thay vì đầu mút:

$$
B' = \begin{pmatrix}
1 & & & & Na_1\\
& 1 & & & Na_2\\
& & \ddots & & \vdots\\
& & & 1 & Na_n\\
\tfrac12 & \tfrac12 & \cdots & \tfrac12 & Ns
\end{pmatrix}, \qquad N > \sqrt n \text{ nguyên}
$$

Cùng tổ hợp $t = (e_1, \dots, e_n, -1)$:

$$
tB' = (e_1 - \tfrac12,\ \dots,\ e_n - \tfrac12,\ 0)
$$

— vector toàn $\pm\tfrac12$ với **chuẩn cố định** $\frac12\sqrt n$ bất kể nghiệm là gì (điều này làm phân tích xác suất sạch sẽ). Nghiệm đọc ra: $e_i = |v_i| + \tfrac12$ (tự xử lý dấu).

**Vì sao giới hạn $d < 0{,}9408$?** Paper chứng minh: xác suất để vector CJLOSS *không* là vector ngắn duy nhất bị chặn

$$
P \le \frac{n(4n\sqrt n + 1)\, 2^{c_0 n}}{\max(a_i)}, \qquad c_0 = 1{,}0628\dots
$$

Muốn $P \to 0$ cần $\max(a_i) > 2^{c_0 n}$, tức $\log_2 \max(a_i) > c_0\, n$, tức:

$$
d = \frac{n}{\log_2\max(a_i)} < \frac{1}{c_0} = 0{,}9408\dots
$$

Lưu ý thực hành: đây là phân tích **lý thuyết với oracle SVP hoàn hảo**; LLL thực tế chỉ xấp xỉ. Với mật độ thấp ($d \lesssim 0{,}7$) LLL gần như luôn thắng; $d \to 0{,}94$ cần BKZ; $d > 1$ (nghiệm không duy nhất) là trận khác hẳn.

### 5.2.3 Ví dụ chạy tay (Ví dụ 4.6 của paper)

$a = (83, 59, 47, 81, 76, 51)$, $s = 291$, $n = 6$. Mật độ $d = 6/\log_2 83 = 6/6{,}375 = 0{,}9412$ (vượt ngưỡng tí chút — vẫn thử). Chọn $N = 3 > \sqrt 6 \approx 2{,}449$. Dựng CJLOSS $7 \times 7$, chạy LLL, kết quả hàng đầu (nhân đôi để sổ phân số):

$$
b_1 = \tfrac12(-1,\ 1,\ 1,\ -1,\ -1,\ -1,\ 0)
$$

Đọc: $v = (\tfrac{-1}2, \tfrac12, \tfrac12, \tfrac{-1}2, \tfrac{-1}2, \tfrac{-1}2)$ là $\pm(e_i - \tfrac12)$. Dấu: $\tfrac12 - v_i = (1, 0, 0, 1, 1, 1)$. Kiểm tra: $83 + 81 + 76 + 51 = 291$ ✓.

### 5.2.4 Các biến thể: nhiều phương trình & theo mô-đun

Ba biến thể đều quy về cùng một kỹ thuật (Peng–Zhang 2016):

> **Multiple subset sum:** $k$ bộ trọng số chia sẻ cùng $e_i$: $\sum_i e_i a_{j,i} = s_j$ với mọi $j$. Mật độ $d = \frac{n}{k\log_2 \max a_{j,i}}$.

Lattice (mỗi phương trình một cột):

$$
B = \begin{pmatrix}
1 & & & Na_{1,1} & \cdots & Na_{k,1}\\
& \ddots & & \vdots & & \vdots\\
& & 1 & Na_{1,n} & \cdots & Na_{k,n}\\
\tfrac12 & \cdots & \tfrac12 & Ns_1 & \cdots & Ns_k
\end{pmatrix}
$$

Tổ hợp $(e_1, \dots, e_n, -1)$ lại sinh $(e_1 - \tfrac12, \dots, e_n - \tfrac12, 0, \dots, 0)$. Giải được tới $d < 0{,}9408$ với $N > \sqrt{(n+1)/4}$.

> **Modular subset sum:** $\sum_i e_i a_i \equiv s \pmod M$. Viết lại $\sum_i e_i a_i = s + \ell M$ ($\ell$ nguyên ẩn!) và thêm **một hàng cho $M$** để lattice "hấp thụ" số dư:

$$
B' = \begin{pmatrix}
1 & & & Na_1\\
& \ddots & & \vdots\\
& & 1 & Na_n\\
& & & NM\\
\tfrac12 & \cdots & \tfrac12 & Ns
\end{pmatrix}
$$

Tổ hợp $(e_1, \dots, e_n, -\ell, -1)$ cho vector ngắn như cũ. Mật độ modular: $d = \frac{n}{\log_2 M}$. (Multiple modular = tổ hợp cả hai: $k$ cột đích + $k$ hàng $M$.)

**Ứng dụng thật:** này chính là lõi của tấn công **Merkle–Hellman** (khóa công khai của hệ balô có mật độ thấp) và bài **ECDSA với $k = z \oplus d$** (mục 6.4) — cả hai đều là multiple modular subset sum trá hình.

## 5.3 Bài toán số ẩn (Hidden Number Problem — HNP)

> Mục 4.3 của paper. Được Boneh–Venkatesan đưa ra năm 1996 để chứng minh "tính an toàn bit" của Diffie–Hellman; nay là bài toán nền của gần như mọi tấn công "lộ bit" trên (EC)DSA, LCG cụt bit, và oracle đệm PKCS.

### 5.3.1 Định nghĩa

> **Bài toán số ẩn (HNP).** Cho số nguyên tố $p$, số ẩn $\alpha \in [1, p-1]$, và $m$ cặp $(t_i, a_i)$ thỏa
> $$\beta_i - t_i\,\alpha + a_i \equiv 0 \pmod p$$
> với $\beta_i$ **không biết** nhưng **nhỏ**: $|\beta_i| < B \ll p$. Tìm $\alpha$.

Đọc theo ngôn ngữ rò rỉ: $\alpha$ là "số bị ẩn" (khóa bí mật); $t_i \alpha + a_i \bmod p$ là giá trị công khai; $\beta_i$ là "phần nhỏ bị che" — ví dụ bit thấp của nonce. Biết gần hết một đại lượng tuyến tính theo $\alpha$, chỉ thiếu một mẩu nhỏ $\Rightarrow$ tìm lại được $\alpha$.

### 5.3.2 Giải bằng CVP (bản Boneh–Venkatesan)

Viết lại phương trình: $\beta_i + a_i = t_i \alpha + k_i p$ với $k_i$ nguyên. Xét lattice (hàng):

$$
B = \begin{pmatrix}
p & & & &\\
& \ddots & & &\\
& & p & &\\
t_1 & \cdots & t_m & 1/p
\end{pmatrix}
\quad\text{(hàng cuối: } (t_1, \dots, t_m,\ 1/p)\text{)}
$$

Tổ hợp $x = (k_1, \dots, k_m, \alpha)$:

$$
xB = (\underbrace{t_1\alpha + k_1 p}_{=\ \beta_1 + a_1},\ \dots,\ \underbrace{t_m\alpha + k_m p}_{=\ \beta_m + a_m},\ \alpha/p)
$$

Đặt vector đích CVP $t = (a_1, \dots, a_m, 0)$. Khi đó:

$$
xB - t = (\beta_1, \dots, \beta_m, \alpha/p) =: u, \qquad \|u\| \le \sqrt{m+1}\, B
$$

— tức **lattice chứa một điểm cách đích $t$ đúng khoảng "mảnh ẩn" $\beta$**! Trong khi đó định thức lattice $\det = p^{m-1}$ (m hàng $p$ và một hàng có $1/p$), nên khoảng cách ngắn "bình thường" của lattice cỡ $\det^{1/(m+1)} \cdot \sqrt{m+1} = p^{(m-1)/(m+1)}\sqrt{m+1}$ — lớn hơn nhiều khi $B$ nhỏ. Giải CVP(xấp xỉ) tìm $u$, đọc $\alpha = u_{m+1} \cdot p$.

**Điều kiện lý thuyết (BV96):** thành công với $m = 2\sqrt{\log p}$ và $B \le p/2^{\sqrt{\log p}}$ — tức chỉ cần lộ khoảng $\sqrt{\log p}$ bit (với $p$ 160 bit: ~12 bit, 12 chữ số... thực tế luyện tập thường lộ nhiều hơn cho chắc).

### 5.3.3 Giải bằng SVP (Kannan embedding — thường mạnh hơn)

Nhúng đích vào lattice (đặt thêm hệ số $B$ để cân cột):

$$
B' = \begin{pmatrix}
p & & & &\\
& \ddots & & &\\
& & p & &\\
t_1 & \cdots & t_m & B/p &\\
a_1 & \cdots & a_m & & B
\end{pmatrix}
$$

Tổ hợp $(k_1, \dots, k_m, \alpha, -1)$ sinh:

$$
u' = (\beta_1, \dots, \beta_m,\ \alpha B/p,\ -B), \qquad \|u'\| \le \sqrt{m+2}\, B
$$

— vector ngắn trong lattice chiều $m+2$! LLL rồi tìm hàng có tọa độ cuối $= \pm B$, đọc $\alpha = \pm(\text{hàng}[m{+}1]) \cdot p / B \bmod p$.

**Bẫy quen thuộc:** vector $(0,\dots,0,B,0)$ (tổ hợp $(-t_1, \dots, -t_m, p, 0)$) luôn **ngắn hơn** $u'$ và hay chiếm vị trí hàng đầu. Nghiệm thường nằm ở **hàng thứ hai** hoặc mang dấu âm — khi lọc kết quả, hãy kiểm tra cả $\pm$ từng hàng và điều kiện đích "tọa độ cuối $\pm B$".

### 5.3.4 Ví dụ chạy tay (Ví dụ 4.11 của paper)

$p = 401$, $t = (143, 293, 304)$, $a = (62, 300, 86)$, $B = 20$, đáp số $\alpha = 309$. Dựng lattice $5 \times 5$ embedding như trên:

$$
B' = \begin{pmatrix}
401 & 0 & 0 & 0 & 0\\
0 & 401 & 0 & 0 & 0\\
0 & 0 & 401 & 0 & 0\\
143 & 293 & 304 & 20/401 & 0\\
62 & 300 & 86 & 0 & 20
\end{pmatrix}
$$

(Người chơi nhân toàn bộ cột 4 với 401 để nguyên hóa — chi tiết thực hành.) Chạy LLL, cơ sở rút gọn (viết theo paper):

- hàng 1 = $(0,0,0,20,0)$ — đúng như dự báo: vector "bẫy" ngắn nhất;
- hàng 2 = $(-15,-12,-16,\tfrac{1840}{401}, 20)$ — tọa độ cuối $+20 = B$! Đây là $-u'$.

Đọc: $\alpha = -\tfrac{1840}{401} \cdot \tfrac{401}{20} \bmod 401 = -92 \bmod 401 = 309$ ✓. Đồng thời thu được $\beta = (15, 12, 16)$ — cả ba mảnh ẩn đều nhỏ hơn $B = 20$ như hứa hẹn.

### 5.3.5 HNP mở rộng (EHNP) — khi biết "từng mảnh rời"

> Mục 4.3.2 của paper, theo Hlaváč–Rosa 2007. Mở rộng HNP theo hai hướng cùng lúc: (1) mỗi phương trình có **nhiều mảnh ẩn** (không liền kề nhau); (2) bản thân **số ẩn $\alpha$ cũng bị lộ từng mảnh**.

> **Định nghĩa (EHNP).** Số ẩn $x = \bar x + \sum_{j=1}^{m} 2^{\pi_j} x_j$ (biết $\bar x$, $\pi_j$; ẩn $0 \le x_j < 2^{\nu_j}$). Cho $d$ phương trình
> $$\alpha_i \sum_j 2^{\pi_j} x_j + \sum_{j=1}^{l_i} \rho_{i,j} k_{i,j} \equiv \beta_i - \alpha_i \bar x \pmod p$$
> với $\alpha_i, \rho_{i,j}, \beta_i$ biết, $0 \le k_{i,j} < 2^{\mu_{i,j}}$ ẩn. Tìm $x$.

Đây đúng là hình ảnh "đoán bit rời rạc": khóa $d$ biết một vài đoạn, mỗi nonce $k_i$ biết một vài đoạn (side-channel chỉ lộ chỗ cây bút chì chạm, không nhất thiết liền nhau).

**Lattice EHNP:** với hằng số cân $\delta > 0$ (chọn sau):

$$
B = \begin{pmatrix}
p \cdot I_d & A & 0\\
0 & X & 0\\
0 & R & K
\end{pmatrix}
\;\;\text{với}\;\;
A = \big(\alpha_i 2^{\pi_j}\big)_{j,i},\;
X = \mathrm{diag}\Big(\frac{\delta}{2^{\nu_j}}\Big),\;
R = \big(\rho_{i,j}\big),\;
K = \mathrm{diag}\Big(\frac{\delta}{2^{\mu_{i,j}}}\Big)
$$

Tổ hợp chứa toàn bí mật $x = (r_1..r_d,\ x_1..x_m,\ k_{1,1}..k_{d,l_d})$ sinh ra vector lattice $u$ mà các tọa độ giữa/chính là các mảnh ẩn **đã scale về khoảng $[0, \delta)$**. Vector đích CVP đặt ngay "tâm" của các khoảng đó:

$$
w = (\beta_1 - \alpha_1 \bar x, \dots,\ \underbrace{\tfrac\delta2, \dots, \tfrac\delta2}_{m + L \text{ phần tử}})
$$

Giải CVP với đích $w$ tìm $u$, đọc mảnh $x_j = u_{d+j} \cdot 2^{\nu_j} / \delta$ (làm tròn).

**Chọn $\delta$:** chứng minh của HR07 yêu cầu $0 < \kappa_D \delta < 1$ với $\kappa_D = \sqrt[D]{2^D/(4(m+L))} + \tfrac12$, $D = d + m + L$, $L = \sum l_i$. Xác suất thành công $P > 1 - \frac{(2\kappa_D)^{L+m} 2^{\tau + \xi}}{p^d}$ với $\tau = \sum \nu_j$, $\xi = \sum\sum \mu_{i,j}$ — càng nhiều phương trình ($d$), càng ít phần ẩn thì càng thắng. Trong thực hành: normalize hết về $[0,\delta)$ như trên, LLL, và nếu hụt thì "săn đuổi": brute force mảnh nhỏ nhất.

**Mối quan hệ HNP ⊂ EHNP:** HNP là EHNP với một mảnh ($m = 1$, $\pi_1 = 0$, $\nu_1 = \log_2 B$) và mỗi phương trình một biến phụ $l_i = 1$. Ngược lại, mọi kỹ thuật HNP (embedding, recentering, chọn hệ số cân) dùng được cho EHNP.



---

# Phần 6 — Các tấn công thực tế

> Mục 5 của paper. Mỗi mục dưới đây đi theo đúng pipeline: **bối cảnh → biến đổi → bài toán nền → dựng lattice → đọc nghiệm**. Đây là nơi thấy rõ "một bài toán nền phục vụ nhiều tấn công".

## 6.1 RSA stereotyped message (tin nhắn khuôn mẫu)

> Tấn công của Coppersmith 1997 trên RSA số mũ nhỏ khi biết trước phần lớn bản rõ.

**Bối cảnh.** $N$, $e$ nhỏ (classically $e = 3$), bản mã $c = m^e \bmod N$, biết $m = m' + x_0$ với $m'$ **biết trước** (ví dụ bản rõ có khuôn mẫu cố định "my secret pin is XXXX") và $x_0$ nhỏ.

**Biến đổi (1 dòng):**

$$
c = (m' + x_0)^e \pmod N \;\Longleftrightarrow\; f(x) = (m' + x)^e - c \equiv 0 \pmod N
$$

— đa thức monic bậc $e$, nghiệm nhỏ $x_0$. **Đúng ngõ Coppersmith univariate** (mục 5.1): tìm được khi $|x_0| \le \frac12 N^{1/e}$. Với $e = 3$: phục hồi được phần ẩn chiếm tới **1/3 kích thước $N$** — tức biết trước 2/3 bản rõ là đủ.

**Ví dụ trong paper (5.1).** $N$ 170-bit, $e = 3$, bản rõ "my secret pin is XXXX" với XXXX là mã PIN 4 chữ số. Chuyển phần biết (thay XXXX bằng byte 0) thành số $m'$; phần ẩn $x_0 < 2^{32}$. Nghiệm Coppersmith trả về $x_0 = 825439031$ → bytes = `1337`. (Lưu ý kỹ thuật: phần ẩn nằm ở **cuối** message nên cộng thẳng vào $m'$; nếu phần ẩn nằm giữa thì nhân trọng số $2^{8t}$ — xem "nhiều phần ẩn" dưới đây.)

**Nhiều phần ẩn (rời rạc).** Ví dụ "my username is XXXX and pin is YYYY":

$$
m = m' + 2^{t_x} x_0 + 2^{t_y} y_0
\;\Longrightarrow\;
f(x, y) = (m' + 2^{t_x}x + 2^{t_y}y)^e - c \equiv 0 \pmod N
$$

với $t_x, t_y$ là vị trí bit của các phần ẩn. Dùng **Coppersmith đa biến** (heuristic — mục 5.1.3): dựng lattice shift polynomial lớn, LLL, giải hệ bằng resultant/Gröbner. Đây chính là tinh thần của challenge kinh điển và cả short-pad attack.

**Liên hệ:** đây là "Finding small roots" ứng dụng trực tiếp nhất; cùng họ với "biết bit cao của $p$" ($f(x) = p_{\text{cao}} + x$ với ước $p \approx N^{1/2}$, dùng beta=1/2) mà bạn đã gặp trong bộ RSA challenge (mục 15, 16).

## 6.2 Boneh–Durfee: RSA với $d < N^{0.292}$

> Boneh–Durfee 1999. Vượt lên trên tấn công Wiener ($d < N^{0.25}$, dùng phân số liên tục chứ không cần lattice).

**Bối cảnh.** $N = pq$ cân bằng, $e$ lớn (vì $d$ nhỏ thì $e$ thường lớn), $d < N^\delta$ với $\delta < 0{,}292$. Không biết gì thêm.

**Biến đổi.** Từ phương trình khóa $ed = 1 + k\varphi(N)$, $\varphi(N) = N - p - q + 1$:

$$
1 + k(N - p - q + 1) \equiv 0 \pmod e
$$

$(N+1)$ và $(p+q)$ đều chẵn nên chia 2 cho gọn:

$$
f(x, y) = 1 + 2x\left(\frac{N+1}{2} - y\right) \equiv 0 \pmod e
$$

**Hai nghiệm nhỏ:** $(x_0, y_0) = \left(k,\ \frac{p+q}{2}\right)$. Kiểm tra kích thước: $k = \frac{ed-1}{\varphi(N)} < d < N^\delta$ (với $e < \varphi$), còn $\frac{p+q}{2} \approx \sqrt N = N^{0{,}5}$ — cả hai đều "nhỏ" so với mô-đun $e \approx N$.

**Giải:** Coppersmith **bivariate modular** với bộ shift polynomial đặc biệt của Boneh–Durfee (x-y swapped, dùng cả $x$ lũy thừa và $y$). Họ chứng minh nghiệm tìm được khi $\delta < 1 - 1/\sqrt2 \approx 0{,}29289$. Sau khi có $(k, s)$:

$$
ed = 1 + k(N + 1 - 2s) \;\Longrightarrow\; d = \frac{1 + k(N+1-2s)}{e}, \quad \text{rồi } \varphi = (ed-1)/k \Rightarrow \text{factor } N.
$$

**Thực hành:** có script Sage chuẩn (boneh_durfee.sage của mimoo) với hai chế độ lattice "x-axis"/"y-axis"; giới hạn thực dụng ~0.280–0.292 tùy chất lượng LLL/BKZ. Vượt 0.292 là **đường biên lý thuyết suốt 25+ năm** — chưa ai phá.

## 6.3 Partial key exposure: biết MSB của $d$

> Ernst và cộng sự 2005, giản lược theo Sarkar–Sen Gupta–Maitra 2010. Kịch bản: $d$ hơi lớn hơn ngưỡng Boneh–Durfee, NHƯNG bị lộ một phần bit (side-channel, backup lỗi...).

**Bối cảnh.** $d < N^\delta$ (có thể $\delta > 0{,}292$!), biết $d_0$ sao cho $|d - d_0| < N^\gamma$ (biết $(\delta - \gamma)\log_2 N$ bit cao của $d$).

**Biến đổi — ý tưởng: xấp xỉ $k$ từ bit đã biết.** Từ $d = d_0 + d_1$:

$$
k = \frac{e(d_0 + d_1) - 1}{\varphi(N)} \approx \frac{e\,d_0}{N}
\;\Longrightarrow\; k_0 = \left\lfloor \frac{e d_0}{N} \right\rfloor
$$

(vì $\varphi(N) = N - p - q + 1 \approx N$). Blömer–May chứng minh $|k - k_0| < 4N^\lambda$ với $\lambda = \max(\gamma, \delta - \tfrac12)$. Thay vào phương trình Boneh–Durfee:

$$
f(x, y) = 1 + 2(k_0 + x)\left(\frac{N+1}{2} - y\right) \equiv 0 \pmod e
$$

với nghiệm nhỏ $(x_0, y_0) = (k - k_0,\ \frac{p+q}{2})$ — giờ $x_0$ nhỏ hơn nhiều so với $k$ nguyên vẹn (chỉ còn phần "lệch" của xấp xỉ). Lattice tương tự Boneh–Durfee, giải tương tự.

**Thông điệp tổng quát:** *mọi bit lộ thêm đều "hạ" kích thước nghiệm cần tìm, kéo bài toán về vùng Coppersmith khả giải.* Đây là mẫu "lattice + partial information" lặp đi lặp lại: HNP là bản tuyến tính của triết lý này, còn Coppersmith là bản đa thức.

## 6.4 ECDSA với $k = z \oplus d$ (nonce = hash XOR khóa)

> Bắt nguồn từ challenge "Signature" — TSJ CTF 2022 (maple3142). Ví dụ sống của **multiple modular subset sum**.

**Bối cảnh.** $\ell$ chữ ký ECDSA $(z_i, r_i, s_i)$ trên đường cong bậc $n$; nonce $k_i = z_i \oplus d$ ($z_i$ = hash thông điệp, $d$ = khóa bí mật). Nghe có vẻ "không đoán được" vì $d$ ẩn... nhưng XOR **không giữ được tính tuyến tính theo bit**.

**Biến đổi.** Phương trình chữ ký: $s_i k_i = z_i + r_i d \pmod n$. Mở XOR theo bit (nhớ $d = \sum_j 2^{j-1} d_{[j]}$ với $d_{[j]}$ là bit thứ $j$):

$$
k_i = z_i \oplus d = z_i + d - \sum_{j=1}^{m} 2^j z_{i,[j]} d_{[j]}
$$

(Tại sao: bit nào của $z_i$ bằng 1 thì XOR "đảo" bit $d$ tương ứng — hiệu trừ $2\cdot(\text{bit } d)$ ở đúng trọng số; bit nào của $z_i$ bằng 0 thì giữ nguyên.) Thay vào:

$$
s_i\left(z_i + \sum_j 2^{j-1} d_{[j]} - \sum_j 2^j z_{i,[j]} d_{[j]}\right) \equiv z_i + r_i \sum_j 2^{j-1} d_{[j]} \pmod n
$$

Gom về dạng chuẩn — **mỗi chữ ký cho một phương trình tuyến tính mod $n$ theo các ẩn BIT $d_{[j]} \in \{0,1\}$**:

$$
\sum_{j=1}^{m} a_{i,j}\, d_{[j]} \equiv b_i \pmod n,
\qquad a_{i,j},\ b_i \text{ tính được từ } z_i, r_i, s_i
$$

**Đúng bài toán multiple modular subset sum** (mục 5.2.4) với "trọng số" $a_{i,j}$ cỡ $n$ bit, $m$ ẩn bit, $\ell$ phương trình. Mật độ $d = m/(\ell \log_2 n) \approx 1/\ell$ — với **$\ell \ge 2$ chữ ký** đã có mật độ $\le 0{,}5 < 0{,}9408$: LLL thắng. Lattice $(m + \ell + 1)$ chiều hơi lớn (vài trăm) nhưng thưa — LLL/BKZ vẫn xử lý được trong vài phút.

**Đọc nghiệm:** vector ngắn có tọa độ $\pm(d_{[j]} - \tfrac12)$; ráp bit lại thành $d$.

## 6.5 ECDSA với nonce lệch (biased nonces) → HNP

> Howgrave-Graham–Smart 2001; paper nền lý thuyết: Boneh–Venkatesan. "Lệch chỉ dưới 1 bit cũng chết" (Aranha et al. 2020 — LadderLeak).

**Bối cảnh chung.** $\ell$ chữ ký $(z_i, r_i, s_i)$, phương trình $s_i k_i \equiv z_i + r_i d \pmod n$. Tách $d$:

$$
k_i - \underbrace{(s_i^{-1} r_i)}_{t_i}\, d + \underbrace{(-s_i^{-1} z_i)}_{a_i} \equiv 0 \pmod n
\;\;\Longrightarrow\;\;\beta_i - t_i d + a_i \equiv 0 \pmod n
$$

với $\beta_i = k_i$ (hoặc phần "còn thiếu" của $k_i$ tùy biến thể) — **chính là HNP** (mục 5.3) với $p \to n$, $\alpha \to d$. Bốn biến thể chỉ khác cách định nghĩa $\beta_i$:

**1. MSB bằng 0** (nonce luôn nhỏ): $k_i < 2^{\log_2 n - l}$ tức thiếu $l$ bit cao. $\beta_i = k_i$, chặn $B = 2^{\log n - l}$. HNP thẳng.

**2. LSB bằng 0** ($l$ bit cuối = 0): $k_i = 2^l k'_i$ với $k'_i$ nhỏ. Chia cả phương trình cho $2^l$ (nghịch đảo mod $n$ tồn tại):

$$
k'_i - (2^{-l} s_i^{-1} r_i)\,d + (-2^{-l} s_i^{-1} z_i) \equiv 0 \pmod n
$$

$\beta_i = k'_i < 2^{\log n - l}$ — lại HNP.

**3. Biết MSB** (side-channel lộ $l$ bit cao): $k_i = 2^{\log_2 n - l}\, t_i + k'_i$ với $t_i$ **biết**. Thay vào và chuyển hằng sang vế phải:

$$
k'_i - (s_i^{-1} r_i)\,d + (2^{\log_2 n - l}t_i - s_i^{-1} z_i) \equiv 0 \pmod n
$$

— giống biến thể 1 nhưng $a_i$ "nạp thêm" phần đã biết của nonce.

**4. MSB chung** (các nonce chia cùng $l$ bit cao $t$ — KHÔNG biết giá trị $t$): $k_i = 2^{\log n - l} t + k'_i$. Khử $t$ bằng cách **trừ từng cặp phương trình** (lấy phương trình 1 làm mốc, $i = 2..\ell$):

$$
(k'_i - k'_1) - (s_i^{-1} r_i - s_1^{-1} r_1)\,d + (s_1^{-1} z_1 - s_i^{-1} z_i) \equiv 0 \pmod n
$$

$\beta_i = k'_i - k'_1$ nhỏ (cỡ $2^{\log n - l}$) — HNP với $\ell - 1$ phương trình.

**Số lượng chữ ký cần thiết:** theo lý thuyết $\ell \approx 2\sqrt{\log n}$ với $l \approx \sqrt{\log n}$ bit lộ; thực tế CTF: lộ 4–8 bit thì cần ~50–200 chữ ký (thử tăng dần). Mẹo mạnh: **recentering** (dịch $\beta$ về đối xứng quanh 0) và **brute-force vài bit nữa** (lattice nhỏ hơn nhiều).

## 6.6 ECDSA key disclosure problem → EHNP

> Mục 5.3.3 của paper — tổng quát hóa 6.5: biết **mảnh rời** của cả nonce VÀ cả khóa.

**Bối cảnh.** Viết khóa và nonce theo mảnh bit đã biết/ẩn:

$$
d = \bar d + \sum_{j=1}^{m} 2^{\pi_j} d_j \quad (0 \le d_j < 2^{\nu_j}), \qquad
k_i = \bar k_i + \sum_{j=1}^{l_i} 2^{\lambda_{i,j}} k_{i,j} \quad (0 \le k_{i,j} < 2^{\mu_{i,j}})
$$

(biết $\bar d, \bar k_i$ và mọi vị trí $\pi_j, \lambda_{i,j}$; các $d_j, k_{i,j}$ ẩn). Thay vào $s_i k_i \equiv z_i + r_i d$:

$$
r_i \sum_{j=1}^{m} 2^{\pi_j} d_j + \sum_{j=1}^{l_i} (-2^{\lambda_{i,j}} s_i)\, k_{i,j} \equiv (s_i \bar k_i - z_i) - r_i \bar d \pmod n
$$

— **đúng format EHNP** (mục 5.3.5) với $\alpha_i = r_i$, $\rho_{i,j} = -2^{\lambda_{i,j}} s_i \bmod n$, $\beta_i = s_i \bar k_i - z_i$. Dựng lattice $[pI; AX; RK]$, đích $w$ ở "tâm" $\delta/2$, giải CVP như đã trình bày.

## 6.7 Bleichenbacher PKCS#1 v1.5 — bản lattice

> Mục 5.4. Bản gốc 1998 của Bleichenbacher là "nhị phân phân vùng khoảng"; paper giới thiệu công thức lattice của Nguyen 2009 — không nhanh hơn nhưng trực quan và là một ứng dụng HNP đẹp.

**PKCS#1 v1.5 nhắc lại.** Khối mã hóa $EB = 00\,\|\,02\,\|\,PS\,\|\,00\,\|\,M$ — bắt đầu bằng byte `00 02`, chuỗi đệm $PS$ khác 0, byte 0 ngăn cách, rồi thông điệp. Oracle $\mathcal{O}_B(c) = 1$ nếu bản rõ của $c$ "đúng format" (dễ có thật: server TLS cũ trả lỗi khác nhau cho đệm sai).

**Thu hoạch quan hệ.** Chọn ngẫu nhiên $r$, hỏi oracle $r^e c \bmod N$ — nếu trả 1 thì bản rõ $(r m \bmod N)$ bắt đầu bằng `00 02`, tức:

$$
2B \le r m \bmod N < 3B, \qquad B = 2^{l - 16}
$$

($l$ = số bit của $N$; $2B$ = byte `00 01`... chú ý $2B$ tương ứng tiền tố `00 02` chiếm 2 byte). Viết $r m \bmod N = 2B + k$ với $0 \le k < B$:

$$
k - r\,m + 2B \equiv 0 \pmod N, \qquad |k| < B
$$

— **HNP** với số ẩn $m$, "nonce ẩn" $k$ bị chặn $B = 2^{l-16}$ (tức lộ $\log_2 B \approx l - 16$ bit trên tổng $l$). Xác suất một $r$ ngẫu nhiên được chấp nhận $\approx 1/65536$ — cần ~$\ell \cdot 65536$ truy vấn để có $\ell$ phương trình.

**Cần bao nhiêu phương trình?** Vector HNP ngắn có chuẩn $\sqrt{\ell + 2}\,B$; theo Minkowski/Gaussian-heuristic vector ngắn "bình thường" của lattice $\approx \sqrt{\ell + 2}\,(B^2 N^{\ell - 1})^{1/(\ell+2)}$. Yêu cầu lệch chuẩn:

$$
B \ll (B^2 2^{l(\ell-1)})^{1/(\ell+2)} \;\Longleftrightarrow\; l \ll 16\,\ell
$$

Với $l = 512$ bit: $\ell \gtrsim 32$, paper khuyên $\ell > 40$ (~2{,}6 triệu truy vấn). Sau khi giải HNP được $m$ — bản rõ lộ.

## 6.8 (Mở rộng theo Hình 2 của paper) LCG cụt bit — HNP trá hình

Paper giới thiệu ở Hình 2 tuyến "truncated LCG → HNP" (Frieze–Håstad–Kannan–Lagarias–Shamir 1988). Đầy đủ để bạn nhận diện dạng này:

**Bối cảnh.** LCG: $x_{i+1} = a x_i + b \pmod M$; chỉ được thấy **bit cao** của mỗi $x_i$: $y_i = \lfloor x_i / 2^t \rfloor$ (thấp $t$ bit bị cắt). Khôi phục trạng thái.

**Biến đổi.** Đặt $x_i = 2^t y_i + e_i$ với $0 \le e_i < 2^t$ nhỏ — phần bị cắt chính là "$\beta_i$" của HNP. Khử đệ quy (biểu diễn $x_i$ theo $x_0$: $x_i \equiv a^i x_0 + \frac{a^i - 1}{a - 1} b$) rồi thay vào:

$$
\underbrace{(2^t y_i + e_i)}_{x_i} \equiv a^i x_0 + c_i \pmod M
\;\Longrightarrow\;
e_i - \underbrace{a^i}_{t_i}\,x_0 + \underbrace{(2^t y_i - c_i)}_{a_i} \equiv 0 \pmod M
$$

— HNP với mô-đun $M$ (không nguyên tố vẫn chạy được bằng embedding), số ẩn $x_0$, các $\beta_i = e_i < 2^t$. Càng nhiều bit bị cắt (t lớn) càng cần nhiều mẫu. Nhận diện nhanh: **"bài cho các số gần đúng của một chuỗi truy hồi tuyến tính" → LLL ngay**.



---

# Phần 7 — Bản đồ liên kết: tất cả ghép với nhau thế nào

## 7.1 Ba tầng của mọi tấn công lattice

Nhắc lại pipeline ở Phần 0 — giờ đã có đủ mảnh để nhìn toàn cảnh:

```
TẤN CÔNG                    BÀI TOÁN NỀN              BÀI TOÁN LATTICE     CÔNG CỤ
─────────────────────────────────────────────────────────────────────────────────────
RSA biết bit cao của p   ─►                         ─┐
RSA stereotyped message  ─►  Tìm nghiệm nhỏ        ─┤
Boneh–Durfee (d<N^0.292) ─►  (Coppersmith)          ├─►  SVP_γ  ─►  LLL
Partial key exposure     ─►                         ─┤      + resultant/Grobner
Short-pad attack         ─►                         ─┘      (đa biến, heuristic)

Merkle–Hellman balô      ─►                         ─┐
SECCON-style knapsack    ─►  Subset sum             ─┤
ECDSA k = z ⊕ d          ─►  (CJLOSS / TSJ)         ├─►  SVP_γ  ─►  LLL/BKZ
                             (thường + modular)     ─┘

LCG cụt bit              ─►                         ─┐
ECDSA biased nonces      ─►  Hidden Number Problem  ─┤
Bleichenbacher (lattice) ─►  (HNP)                  ├─►  CVP_γ  ─►  Babai
DH bit-security (BV96)   ─►                         ─┘   hoặc SVP ← Kannan embed

ECDSA mảnh rời nonce+key ─►  EHNP                   ─►  CVP_γ  ─►  Babai + recenter
```

## 7.2 "Ai phục vụ ai" — nhìn theo từng khối

**Khối thuật toán (tầng dưới cùng):**
- **LLL** = máy móc đa thức thời gian, xấp xỉ hệ số mũ $(\sqrt2)^{n}$, thực tế
  $\approx 1{,}02^n$. BKZ = bản mạnh hơn (block-wise), dùng khi LLL "gần thắng".
- **Babai nearest plane** giải CVP một khi đã có cơ sở rút gọn — "làm tròn theo
  hướng trực giao".
- **Kannan embedding** = cầu nối CVP → SVP: nhúng vector đích vào làm một hàng
  cơ sở với hệ số $q$. Trong bài HNP, embedding thường thắng Babai.

**Khối bài toán nền (tầng giữa) — mỗi cái là một "dịch vụ" dùng lại nhiều lần:**

| Bài toán nền | Dấu hiệu nhận diện | Ai dùng nó |
|---|---|---|
| **Tìm nghiệm nhỏ** | đa thức mod $N$/ước của $N$ + lời giải bị chặn | stereotyped, bit cao của $p$, BD, PKE, short-pad |
| **Subset sum / knapsack** | "tìm vector 0/1 thỏa tổng (mod $M$)" | Merkle–Hellman, TSJ k=z⊕d |
| **HNP** | "số ẩn + mỗi quan hệ thiếu một mẩu nhỏ $\beta_i$" | biased nonces (4 biến thể), LCG cụt, Bleichenbacher-lattice, bit-security DH |
| **EHNP** | HNP nhưng mảnh RỜI + ẩn cũng bị lộ mảnh | key disclosure (Minerva-style) |

**Ba "chiêu" tái sử dụng khắp mọi nơi** (đây là phần "nghệ thuật" của dựng lattice):

1. **Cột cân (scaling):** nhân cột hệ số $2^{64}$ trong TSJ, $B$ trong HNP,
   $X^iY^j$ trong Coppersmith — để mọi thành phần của vector đích về cùng thước đo.
2. **Căn giữa (recentering):** dịch ẩn từ $[0, B)$ về $[-B/2, B/2)$ — giảm
   chuẩn đích một bit và làm phân tích sạch (Breitner–Heninger).
3. **Nhúng đích (embedding):** thêm hàng target + hệ số $q$ — biến CVP thành
   SVP để dùng thẳng LLL; nhớ xử lý **cả hai dấu ±** của vector đích, và coi chừng
   "vector bẫy" ngắn hơn (như $(0,\dots,0,B,0)$ trong HNP).

## 7.3 Chu kỳ sống của một tấn công lattice (kịch bản giải bài CTF)

1. **Nhận diện**: "modular linear equations + lời giải nhỏ/ít-bit/bị-che-một-phần" → lattice.
2. **Chuẩn hóa** về một bài toán nền (như bảng 7.2) — viết lại phương trình cho
   đúng khuôn (k_i = t_i·α + a_i, v.v.).
3. **Ước lượng trước khi code**: tính $\det$, chiều $n$, chuẩn đích $\|v\|$; kiểm tra
   $\|v\| \ll 1{,}02^n\det^{1/n}$ (ngưỡng thực hành). Nếu sát ngưỡng → cần BKZ
   hoặc brute-force thêm vài bit.
4. **Dựng lattice + LLL** (Sage `matrix(ZZ).LLL()` / fpylll / flint — chú ý dùng
   **Gram chính xác** với entry lớn).
5. **Đọc nghiệm**: quét các hàng ngắn, thử $\pm$, lọc theo ràng buộc (bit 0/1,
   cột cuối $\pm B$, tổng đúng...) — rồi **kiểm chứng bằng dữ liệu công khai**
   ($dG = Q$, $m^e = c$, chuỗi LCG khớp...).

## 7.4 Các gốc rễ lịch sử — và vì sao chúng liên quan nhau

- **LLL (1982)** ra đời để **phân tích đa thức hữu tỷ** — ứng dụng đầu tiên của
  nó (KLL84, chính là Phần 4 của tài liệu này) thuần đại số, chưa dây đến mật mã.
- **Merkle–Hellman (1978)** — hệ mã khối đầu tiên trên NP-đầy đủ; **LO85/CJLOSS92**
  giết nó bằng chính SVP → từ đó "subset sum" trở thành bài toán nền kinh điển.
- **BV96 (HNP)** sinh ra để chứng minh *bit của Diffie–Hellman khó* — một kết quả
  "phòng thủ" — rồi bị **HS01** lật ngược thành vũ khí tấn công DSA/ECDSA nonce.
  Bài học: chứng minh "một bit khó đoán" ⟺ "một bit lộ là chết".
- **Coppersmith (1996–97)** mở kỷ nguyên "nghiệm nhỏ mod hợp số không cần factor";
  **BD99** và toàn bộ ngành "partial key exposure" mọc từ đó. Họ nhà này kết nối
  với lattice qua Howgrave-Graham: *đa thức hệ số nhỏ = vector ngắn*.
- **Thập niên 2010–20**: side-channel thật (LadderLeak, Minerva, 9-Lives-of-CAT)
  đưa HNP/EHNP từ lý thuyết ra thực chiến — đúng như pipeline, chỉ thay
  "biến đổi" bằng "đo đạc vật lý".

---

# Phần 8 — Luyện tập: challenge theo từng dạng

Bộ challenge thực hành (kèm gen/solve chạy được) nằm tại **`lattice/`** trong repo này
(`_verify_all.py` — 12/12 OK). Với mỗi dạng: cột "thực chiến" là challenge CTF thật
đã diễn ra (link writeup/bài gốc), cột "luyện tập" là challenge trong bộ.

| Dạng (mục lý thuyết) | Challenge thực chiến thật | Challenge luyện tập |
|---|---|---|
| LLL cơ bản / CVP / Babai | RaRCTF 2021 "Snore" ([jgeralnik writeup](http://jgeralnik.github.io/writeups/2021/08/12/Lattices/)) | latlib `_lib/test_latlib.py` (Babai/Kannan demo) |
| Đa thức tối tiểu (§3.6→§4) | UIUCTF 2025 "Back to Roots" ([writeup](https://awrreny.github.io/posts/uiuctf25-writeup-back-to-roots/)) | `L01_minimal_poly` |
| Subset sum CJLOSS (§5.2) | SECCON CTF 2021 ([rkm0959](https://rkm0959.tistory.com/244)); ngược lại: BackdoorCTF 2023 (density>1 → MITM, [ctftime](https://ctftime.org/writeup/38375)) | `L02_subset_sum` |
| RSA stereotyped (§6.1) | Squ1rrel CTF 2024 "Partial RSA" ([writeup](https://nightxade.github.io/ctf-writeups/writeups/2024/squ1rrel-CTF-2024/crypto/partial-rsa.html)) | `L03_stereotyped` |
| Partial key exposure (§6.3) | hiếm dạng MSB; biến thể LSB: xem bộ RSA `17_bdf_partial_key_exposure` | `L04_partial_key` |
| HNP thuần (§5.3) | tinh thần Donjon "Projective Signatures" ([cryptohack blog](https://blog.cryptohack.org/ecdsa-side-channel-attack-projective-signatures-donjon-ctf-writeup)) | `L05_hnp_basic` |
| LCG cụt bit (§6.8) | DownUnderCTF 2020 ([jsur.in](https://jsur.in)); RCTF ([hackmd](https://hackmd.io/@GowLxW7-TTGIMIQqhgOUlw/H1_a_rHOi)); ELTAM Java Random | `L06_truncated_lcg` |
| ECDSA k = z⊕d (§6.4) | **TSJ CTF 2022 "Signature"** ([repo](https://github.com/maple3142/My-CTF-Challenges/tree/master/TSJ%20CTF%202022/Signature), [mystiz](https://mystiz.hk/posts/2022/2022-03-02-tsjctf-2/)) — 2/428 solves | `L07_ecdsa_xor_nonce` |
| ECDSA biased zero-MSB (§6.5) | Donjon CTF; TBTL 2023 "Memory Safe ECDSA" ([ctftime](https://ctftime.org/writeup/37086)); LadderLeak ([eprint](https://eprint.iacr.org/2020/615)); Biased Nonce Sense ([eprint 2019/023](https://eprint.iacr.org/2019/023)) | `L08_ecdsa_biased` |
| ECDSA shared-MSB (§6.5) | biến thể của trên (ít gặp riêng) | `L09_ecdsa_shared_msb` |
| EHNP (§5.3.5, §6.6) | hiếm trên CTF — bối cảnh thật kiểu Minerva ([minerva.crocs.fi.muni.cz](https://minerva.crocs.fi.muni.cz/)) | `L10_ehnp` |
| Boneh–Durfee (§6.2) | 春秋杯 2023 (d≈N^0.273); script chuẩn [mimoo](https://github.com/mimoo/RSA-and-LLL-attacks) | `L11_boneh_durfee` |
| Bleichenbacher lattice (§6.7) | bản cổ điển: nhiều CTF (bộ RSA `14`); bản lattice hiếm — tự tạo | `L12_bleichen_lattice` |

Công cụ nên dùng khi tự giải (môi trường Windows):
SageMath (nếu có WSL) cho `small_roots`/`LLL`; trên Python thuần: `flint`
(`fmpz_mat.lll(gram='exact')` — **nhớ `'exact'`**, mặc định `'approx'` có thể
trả vector ngoài lattice với entry lớn), `fpylll` (BKZ, CVP), `jvdsn/crypto-attacks`
(subset sum, PKE), và bộ `_lib/latlib.py` của chính bộ challenge này.

---

# Phần 9 — Tài liệu tham khảo

Tài liệu gốc được biên soạn trong file này:

- **[SC23]** Joseph Surin, Shaanan Cohney. *A Gentle Tutorial for Lattice-Based
  Cryptanalysis*. IACR ePrint 2023/032. https://eprint.iacr.org/2023/032
- Code kèm theo tutorial: https://github.com/josephsurin/lattice-based-cryptanalysis

Các trích dẫn chính bên trong paper (đã dịch/phân tích trong các mục tương ứng):

- [LLL82] Lenstra, Lenstra, Lovász. *Factoring polynomials with rational coefficients*. 1982.
- [KLL84] Kannan, Lenstra, Lovász. *Polynomial factorization and nonrandomness of bits*. 1984. (§4)
- [LO85] Lagarias, Odlyzko. *Solving low-density subset sum problems*. 1985. (§5.2)
- [Bab86] Babai. *On Lovász' lattice reduction and the nearest lattice point problem*. 1986. (§3.1)
- [Kan87] Kannan. *Minkowski's convex body theorem and integer programming*. 1987. (§3.2)
- [Fri+88] Frieze, Håstad, Kannan, Lagarias, Shamir. *Reconstructing truncated integer variables*. 1988. (§6.8)
- [MH78] Merkle, Hellman. *Hiding information in trapdoor knapsacks*. 1978.
- [BV96] Boneh, Venkatesan. *Hardness of computing the most significant bits of secret keys in DH*. 1996. (HNP)
- [Cop96/97] Coppersmith. *Finding a small root of a univariate modular equation* / *Small solutions to polynomial equations, and low exponent RSA vulnerabilities*. (§5.1)
- [How97] Howgrave-Graham. *Finding small roots of univariate modular equations revisited*. 1997.
- [BD99] Boneh, Durfee. *Cryptanalysis of RSA with private key d less than N^0.292*. 1999. (§6.2)
- [Ble98] Bleichenbacher. *Chosen ciphertext attacks against protocols based on the RSA encryption standard PKCS#1*. 1998. (§6.7)
- [HS01] Howgrave-Graham, Smart. *Lattice attacks on digital signature schemes*. 2001. (§6.5)
- [HR07] Hlaváč, Rosa. *Extended Hidden Number Problem and its cryptanalytic applications*. 2007. (EHNP)
- [Cor07] Coron. *Finding small roots of bivariate integer polynomial equations*. 2007.
- [JM06] Jochemsz, May. *A strategy for finding roots of multivariate polynomials*. 2006.
- [Cos+92] Coster et al. *Improved low-density subset sum algorithms* (CJLOSS). 1992.
- [PZ16] Peng, Zhang. *Solving low-density multiple subset sum problems with SVP oracle*. 2016.
- [May03] May. *New RSA vulnerabilities using lattice reduction methods* (luận án). 2003.
- [Ngu09] Nguyen. *Public-Key Cryptanalysis* (formulation lattice cho Bleichenbacher). 2009.
- [BM03] Blömer, May. *New partial key exposure attacks on RSA*. 2003.
- [Ern+05] Ernst et al. *Partial key exposure attacks on RSA up to full size exponents*. 2005. (§6.3)
- [SGM10] Sarkar, Sen Gupta, Maitra. *Partial key exposure attack — improvements for limited lattice dimensions*. 2010.
- [NS06] Nguyen, Stehlé. *LLL on the average*. 2006. (heuristic 1.02^n)
- [Ben+14] Benger et al. *"Ooh Aah... Just a Little Bit"*. 2014.
- [BH19] Breitner, Heninger. *Biased Nonce Sense* (recentering). 2019.
- [Ara+20] Aranha et al. *LadderLeak*. 2020.
- [Sun+21] Sun et al. *Guessing Bits* (embedding factor). 2021.
- [Ron+19] Ronen et al. *The 9 Lives of Bleichenbacher's CAT*. 2019.
- [DH20] De Micheli, Heninger. *Recovering cryptographic keys from partial information, by example*. 2020.

Sách/tài liệu bổ sung nên đọc tiếp (theo thứ tự):
1. Hoffstein–Pipher–Silverman, *An Introduction to Mathematical Cryptography*
   — chương lattices cho nền toán chặt chẽ hơn.
2. Galbraith, *Mathematics of Public Key Cryptography* — chương lattice & Coppersmith đầy đủ chứng minh.
3. Nguyen, Vallée (eds.), *The LLL Algorithm* — toàn tập về LLL.
4. [ur4ndom, *Practical lattice reductions for CTF challenges*](https://ur4ndom.dev/static/files/latticetraining/practical_lattice_reductions.pdf) — luyện tay trên challenge thật.
5. jvdsn/crypto-attacks — thư viện Python các tấn công đã code sẵn (subset sum, PKE, HNP).

---

*Hết. Để luyện tập từng dạng, vào `lattice/` (L01–L12) và làm theo README ở đó.*
