# Hai mươi năm các cuộc tấn công vào hệ mật mã RSA

**Dan Boneh**  
**dabo@cs.stanford.edu**

## 1. Giới thiệu

Hệ mật mã RSA, do Ron Rivest, Adi Shamir và Len Adleman [21] phát minh, lần đầu được công bố rộng rãi trên số tháng 8 năm 1977 của tạp chí *Scientific American*. Hệ mật mã này được sử dụng phổ biến nhất để bảo đảm tính riêng tư và tính xác thực của dữ liệu số. Ngày nay, RSA được triển khai trong nhiều hệ thống thương mại. Nó được các máy chủ web và trình duyệt sử dụng để bảo vệ lưu lượng web, được dùng để bảo đảm tính riêng tư và tính xác thực của thư điện tử, được dùng để bảo vệ các phiên đăng nhập từ xa, và nằm ở trung tâm của các hệ thống thanh toán thẻ tín dụng điện tử. Nói ngắn gọn, RSA thường xuyên được sử dụng trong những ứng dụng mà tính an toàn của dữ liệu số là một vấn đề quan trọng.

Kể từ khi được công bố lần đầu, hệ thống RSA đã được nhiều nhà nghiên cứu phân tích nhằm tìm kiếm các điểm yếu. Mặc dù hai mươi năm nghiên cứu đã dẫn tới một số cuộc tấn công rất thú vị, không cuộc tấn công nào trong số đó mang tính hủy diệt. Phần lớn chúng minh họa những nguy cơ phát sinh khi RSA được sử dụng không đúng cách. Thực tế, triển khai RSA một cách an toàn là một nhiệm vụ không hề đơn giản. Mục tiêu của chúng tôi là khảo sát một số cuộc tấn công như vậy và mô tả các công cụ toán học nền tảng mà chúng sử dụng. Trong toàn bộ bài khảo sát, chúng tôi tuân theo quy ước đặt tên tiêu chuẩn và dùng Alice cùng Bob để chỉ hai bên bất kỳ muốn liên lạc với nhau. Chúng tôi dùng Marvin để chỉ một kẻ tấn công độc hại muốn nghe lén hoặc can thiệp vào quá trình liên lạc giữa Alice và Bob.

Chúng ta bắt đầu bằng việc mô tả một phiên bản đơn giản hóa của phép mã hóa RSA. Cho

$$
N = pq
$$

là tích của hai số nguyên tố lớn có cùng kích thước, mỗi số dài $n/2$ bit. Một kích thước điển hình của $N$ là $n = 1024$ bit, tức 309 chữ số thập phân. Mỗi thừa số khi đó dài 512 bit. Cho $e,d$ là hai số nguyên thỏa mãn

$$
ed = 1 \pmod{\varphi(N)},
$$

trong đó

$$
\varphi(N) = (p-1)(q-1)
$$

là cấp của nhóm nhân $\mathbb{Z}_N^*$. Ta gọi $N$ là **mô-đun RSA**, $e$ là **số mũ mã hóa**, và $d$ là **số mũ giải mã**. Cặp $\langle N,e\rangle$ là khóa công khai. Đúng như tên gọi, khóa này được công khai và được dùng để mã hóa thông điệp. Cặp $\langle N,d\rangle$ được gọi là khóa bí mật hay khóa riêng và chỉ người nhận các thông điệp được mã hóa mới biết. Khóa bí mật cho phép giải mã các bản mã.

Một thông điệp là một số nguyên $M \in \mathbb{Z}_N^*$. Để mã hóa $M$, ta tính

$$
C = M^e \bmod N.
$$

Để giải mã bản mã, người nhận hợp lệ tính

$$
C^d \bmod N.
$$

Thật vậy,

$$
C^d = M^{ed} = M \pmod N,
$$

trong đó đẳng thức cuối cùng suy ra từ định lý Euler.[^1] Ta định nghĩa **hàm RSA** là

$$
x \mapsto x^e \bmod N.
$$

Nếu biết $d$, ta có thể dễ dàng đảo ngược hàm này bằng đẳng thức ở trên. Chúng tôi gọi $d$ là một **cửa sập** (*trapdoor*) cho phép đảo ngược hàm. Trong bài khảo sát này, chúng tôi nghiên cứu độ khó của việc đảo ngược hàm RSA khi không có cửa sập. Chúng tôi gọi việc này là **phá RSA**. Cụ thể hơn, khi được cho bộ ba $\langle N,e,C\rangle$, ta đặt câu hỏi: khó đến mức nào để tính căn bậc $e$ của $C$ theo mô-đun $N=pq$ khi chưa biết phân tích thừa số của $N$? Vì $\mathbb{Z}_N^*$ là một tập hữu hạn, ta có thể liệt kê tất cả phần tử của $\mathbb{Z}_N^*$ cho đến khi tìm được đúng $M$. Đáng tiếc, cách này dẫn tới một thuật toán có thời gian chạy cỡ $N$, tức tăng theo hàm mũ theo kích thước đầu vào, vốn cỡ $\log_2 N$. Chúng tôi chủ yếu quan tâm tới các thuật toán có thời gian chạy thấp hơn đáng kể, cụ thể là cỡ

$$
n^c,
$$

trong đó

$$
n = \log_2 N
$$

và $c$ là một hằng số nhỏ nào đó, chẳng hạn nhỏ hơn 5. Những thuật toán như vậy thường hoạt động tốt trong thực tế trên các đầu vào đang xét. Trong toàn bộ bài viết, chúng tôi gọi các thuật toán như vậy là **hiệu quả**.

Trong bài khảo sát này, chúng tôi chủ yếu nghiên cứu hàm RSA chứ không phải toàn bộ hệ mật mã RSA. Nói một cách không hoàn toàn chặt chẽ, nếu việc đảo ngược hàm RSA trên các đầu vào ngẫu nhiên là khó thì khi được cho $\langle N,e,C\rangle$, kẻ tấn công không thể khôi phục bản rõ $M$. Tuy nhiên, một hệ mật mã phải chống được những cuộc tấn công tinh vi hơn. Nếu được cho $\langle N,e,C\rangle$, việc khôi phục **bất kỳ thông tin nào** về $M$ cũng phải là bất khả thi về mặt tính toán. Tính chất này được gọi là **an toàn ngữ nghĩa** (*semantic security*).[^2] Chúng tôi không bàn về những cuộc tấn công tinh vi đó ở đây, nhưng cần chỉ ra rằng RSA theo cách mô tả bên trên **không an toàn ngữ nghĩa**: khi biết $\langle N,e,C\rangle$, ta có thể dễ dàng suy ra một số thông tin về bản rõ $M$ (chẳng hạn, ký hiệu Jacobi của $M$ trên $N$ có thể dễ dàng suy ra từ $C$). RSA có thể đạt an toàn ngữ nghĩa bằng cách bổ sung tính ngẫu nhiên vào quá trình mã hóa [1].

Hàm RSA

$$
x \mapsto x^e \bmod N
$$

là một ví dụ về **hàm một chiều có cửa sập**. Hàm này có thể tính rất dễ dàng nhưng, theo hiểu biết hiện nay, không thể bị đảo ngược một cách hiệu quả nếu không có cửa sập $d$, ngoại trừ một số trường hợp đặc biệt. Các hàm một chiều có cửa sập có thể được dùng cho chữ ký số [19]. Chữ ký số cung cấp tính xác thực và tính không thể chối bỏ cho các tài liệu pháp lý điện tử. Chẳng hạn, chúng được dùng để ký séc số hoặc đơn đặt hàng điện tử. Để ký một thông điệp $M \in \mathbb{Z}_N^*$ bằng RSA, Alice áp dụng khóa riêng $\langle N,d\rangle$ lên $M$ và thu được chữ ký

$$
S = M^d \bmod N.
$$

Khi có $\langle M,S\rangle$, bất kỳ ai cũng có thể kiểm tra chữ ký của Alice trên $M$ bằng cách xác minh rằng

$$
S^e = M \pmod N.
$$

Vì chỉ Alice mới có thể tạo ra $S$, ta có thể nghĩ rằng đối thủ không thể giả mạo chữ ký của Alice. Đáng tiếc, mọi chuyện không đơn giản như vậy; cần thêm các biện pháp bổ sung để đạt được an toàn đúng nghĩa. Chữ ký số là một ứng dụng quan trọng của RSA. Một số cuộc tấn công được khảo sát trong bài này nhắm trực tiếp tới chữ ký số RSA.

Một cặp khóa RSA được sinh bằng cách chọn ngẫu nhiên hai số nguyên tố dài $n/2$ bit rồi nhân chúng để thu được $N$. Sau đó, với một số mũ mã hóa cho trước

$$
e < \varphi(N),
$$

ta tính

$$
d = e^{-1} \bmod \varphi(N)
$$

bằng thuật toán Euclid mở rộng. Vì các số nguyên tố có mật độ đủ lớn, một số nguyên tố ngẫu nhiên dài $n/2$ bit có thể được sinh nhanh bằng cách liên tục chọn các số nguyên ngẫu nhiên dài $n/2$ bit rồi kiểm tra tính nguyên tố của từng số bằng một phép kiểm tra nguyên tố xác suất [19].

### 1.1. Phân tích thừa số các số nguyên lớn

Cuộc tấn công đầu tiên cần xem xét đối với một khóa công khai RSA $\langle N,e\rangle$ là phân tích mô-đun $N$ thành thừa số. Khi biết phân tích thừa số của $N$, kẻ tấn công có thể dễ dàng xây dựng $\varphi(N)$, từ đó tìm được số mũ giải mã

$$
d = e^{-1} \bmod \varphi(N).
$$

Chúng tôi gọi việc phân tích mô-đun thành thừa số là một cuộc tấn công vét cạn vào RSA. Mặc dù các thuật toán phân tích thừa số liên tục được cải tiến, trình độ tốt nhất hiện nay vẫn còn rất xa mới trở thành mối đe dọa đối với RSA khi RSA được sử dụng đúng cách. Phân tích thừa số số nguyên lớn là một trong những bài toán đẹp nhất của toán học tính toán [18, 20], nhưng không phải chủ đề của bài viết này. Để đầy đủ, chúng tôi lưu ý rằng thuật toán phân tích thừa số nhanh nhất hiện nay là **General Number Field Sieve**. Thời gian chạy của nó trên các số nguyên dài $n$ bit là

$$
\exp\left((c+o(1))n^{1/3}\log^{2/3}n\right)
$$

với một hằng số nào đó $c<2$. Những cuộc tấn công RSA mất thời gian lâu hơn cận này không đáng quan tâm. Chúng bao gồm các cuộc tấn công như tìm kiếm vét cạn $M$ và một số cuộc tấn công cũ được công bố ngay sau khi RSA lần đầu xuất hiện.

Mục tiêu của chúng tôi là khảo sát những cuộc tấn công vào RSA có thể giải mã thông điệp mà không trực tiếp phân tích mô-đun RSA $N$ thành thừa số. Tuy nhiên, cũng đáng lưu ý rằng một số tập thưa các mô-đun RSA $N=pq$ có thể bị phân tích thừa số khá dễ dàng. Chẳng hạn, nếu $p-1$ là tích của các thừa số nguyên tố nhỏ hơn $B$, thì $N$ có thể bị phân tích trong thời gian nhỏ hơn

$$
B^3.
$$

Một số triển khai chủ động loại bỏ các số nguyên tố $p$ mà $p-1$ là tích của các số nguyên tố nhỏ.

Như đã nêu ở trên, nếu tồn tại một thuật toán phân tích thừa số hiệu quả thì RSA không còn an toàn. Chiều ngược lại là một bài toán mở lâu năm: có bắt buộc phải phân tích $N$ thành thừa số mới có thể tính hiệu quả căn bậc $e$ theo mô-đun $N$ hay không? Phá RSA có khó ngang với phân tích thừa số hay không? Ta phát biểu cụ thể bài toán mở dưới đây.

**Bài toán mở 1.** Cho các số nguyên $N$ và $e$ thỏa mãn

$$
\gcd(e,\varphi(N))=1,
$$

định nghĩa hàm

$$
f_{e,N}:\mathbb{Z}_N^*\to\mathbb{Z}_N^*
$$

bởi

$$
f_{e,N}(x)=x^{1/e}\bmod N.
$$

Có tồn tại một thuật toán thời gian đa thức $A$ có thể tính phân tích thừa số của $N$ khi được cho $N$ và quyền truy cập tới một “oracle” $f_{e,N}(x)$ đối với một giá trị $e$ nào đó hay không?

Một oracle cho $f(x)$ sẽ tính giá trị hàm trên bất kỳ đầu vào $x$ nào trong thời gian đơn vị. Gần đây, Boneh và Venkatesan [6] đưa ra bằng chứng cho thấy với $e$ nhỏ, câu trả lời cho bài toán trên có thể là “không”. Nói cách khác, với $e$ nhỏ có thể không tồn tại phép quy giảm thời gian đa thức từ bài toán phân tích thừa số sang bài toán phá RSA. Họ chứng minh điều này bằng cách chỉ ra rằng trong một mô hình nhất định, nếu câu trả lời cho bài toán trên là “có” đối với $e$ nhỏ thì sẽ suy ra một thuật toán phân tích thừa số hiệu quả. Ta lưu ý rằng một câu trả lời “có” cho Bài toán mở 1 sẽ dẫn tới một **cuộc tấn công bản mã được chọn** (*chosen ciphertext attack*)[^3] lên RSA. Vì vậy, một câu trả lời “không” có thể lại là điều đáng mong muốn.

Tiếp theo, chúng tôi chỉ ra rằng làm lộ khóa riêng $d$ và phân tích $N$ thành thừa số là hai việc tương đương. Vì vậy, không có ý nghĩa gì khi giấu phân tích thừa số của $N$ khỏi một bên đã biết $d$.

**Mệnh đề 1.** Cho $\langle N,e\rangle$ là một khóa công khai RSA. Khi biết khóa riêng $d$, ta có thể phân tích hiệu quả mô-đun $N=pq$ thành thừa số. Ngược lại, khi biết phân tích thừa số của $N$, ta có thể khôi phục hiệu quả $d$.

**Chứng minh.** Phân tích thừa số của $N$ cho ta $\varphi(N)$. Vì $e$ đã biết, ta có thể khôi phục $d$. Điều này chứng minh chiều ngược lại. Bây giờ ta chỉ ra rằng khi biết $d$, ta có thể phân tích $N$. Với $d$ đã biết, tính

$$
k=de-1.
$$

Theo định nghĩa của $d$ và $e$, ta biết $k$ là bội của $\varphi(N)$. Vì $\varphi(N)$ là số chẵn, ta có thể viết

$$
k=2^t r,
$$

trong đó $r$ lẻ và $t\ge 1$. Ta có

$$
g^k=1
$$

với mọi $g\in\mathbb{Z}_N^*$, do đó

$$
g^{k/2}
$$

là một căn bậc hai của 1 theo mô-đun $N$. Theo Định lý phần dư Trung Hoa, số 1 có bốn căn bậc hai theo mô-đun $N=pq$. Hai căn trong số đó là $\pm1$. Hai căn còn lại là $\pm x$, trong đó $x$ thỏa mãn

$$
x=1\pmod p
$$

và

$$
x=-1\pmod q.
$$

Dùng một trong hai căn cuối này, ta thu được phân tích thừa số của $N$ bằng cách tính

$$
\gcd(x-1,N).
$$

Một lập luận trực tiếp cho thấy nếu $g$ được chọn ngẫu nhiên từ $\mathbb{Z}_N^*$ thì với xác suất ít nhất $1/2$ (theo lựa chọn $g$), một trong các phần tử của dãy

$$
g^{k/2},\;g^{k/4},\;\ldots,\;g^{k/2^t}\pmod N
$$

là một căn bậc hai của 1 làm lộ phân tích thừa số của $N$. Tất cả phần tử trong dãy có thể được tính hiệu quả trong thời gian

$$
O(n^3),
$$

trong đó $n=\log_2N$. $\square$

## 2. Các cuộc tấn công sơ cấp

Chúng ta bắt đầu bằng việc mô tả một số cuộc tấn công sơ cấp đã có từ lâu. Những cuộc tấn công này minh họa việc sử dụng RSA sai một cách rõ ràng. Mặc dù tồn tại nhiều cuộc tấn công kiểu như vậy, chúng tôi chỉ đưa ra hai ví dụ.

### 2.1. Dùng chung mô-đun

Để tránh phải sinh một mô-đun khác nhau $N=pq$ cho mỗi người dùng, người ta có thể muốn cố định $N$ một lần cho tất cả. Cùng một $N$ được sử dụng bởi mọi người dùng. Một cơ quan trung tâm đáng tin cậy có thể cấp cho người dùng $i$ một cặp duy nhất $e_i,d_i$, từ đó người dùng $i$ tạo khóa công khai $\langle N,e_i\rangle$ và khóa bí mật $\langle N,d_i\rangle$.

Thoạt nhìn, cách này có vẻ hoạt động: một bản mã

$$
C=M^{e_a}\bmod N
$$

dành cho Alice không thể bị Bob giải mã vì Bob không có $d_a$. Tuy nhiên, điều này không đúng và hệ thống thu được là không an toàn. Theo Mệnh đề 1, Bob có thể dùng chính các số mũ $e_b,d_b$ của mình để phân tích mô-đun $N$ thành thừa số. Một khi $N$ đã bị phân tích, Bob có thể khôi phục khóa riêng $d_a$ của Alice từ khóa công khai $e_a$ của cô ấy. Quan sát này, do Simmons đưa ra, cho thấy một mô-đun RSA không bao giờ nên được nhiều hơn một thực thể sử dụng.

### 2.2. Làm mù

Cho $\langle N,d\rangle$ là khóa riêng của Bob và $\langle N,e\rangle$ là khóa công khai tương ứng. Giả sử một đối thủ Marvin muốn có chữ ký của Bob trên thông điệp $M\in\mathbb{Z}_N^*$. Vì không ngây thơ, Bob từ chối ký $M$. Marvin có thể thử cách sau: hắn chọn ngẫu nhiên $r\in\mathbb{Z}_N^*$ và đặt

$$
M' = r^eM\bmod N.
$$

Sau đó hắn yêu cầu Bob ký thông điệp ngẫu nhiên $M'$. Bob có thể sẵn sàng cung cấp chữ ký $S'$ của mình trên $M'$ trông có vẻ vô hại. Nhưng nhớ rằng

$$
S'=(M')^d\bmod N.
$$

Bây giờ Marvin chỉ cần tính

$$
S=S'/r\bmod N
$$

và thu được chữ ký $S$ của Bob trên thông điệp gốc $M$. Thật vậy,

$$
S^e = \frac{(S')^e}{r^e}
= \frac{(M')^{ed}}{r^e}
\equiv \frac{M'}{r^e}
= M \pmod N.
$$

Kỹ thuật này, gọi là **làm mù** (*blinding*), cho phép Marvin thu được chữ ký hợp lệ trên một thông điệp do hắn lựa chọn bằng cách yêu cầu Bob ký một thông điệp ngẫu nhiên đã được “làm mù”. Bob không có thông tin về thông điệp thực sự mà mình đang ký. Vì hầu hết các lược đồ chữ ký áp dụng một **hàm băm một chiều** lên thông điệp $M$ trước khi ký [19], cuộc tấn công này không phải là một mối lo nghiêm trọng. Mặc dù chúng tôi trình bày làm mù như một cuộc tấn công, thực ra đây là một tính chất hữu ích của RSA cần thiết để triển khai tiền số ẩn danh — loại tiền có thể dùng để mua hàng nhưng không tiết lộ danh tính của người thực hiện giao dịch.

## 3. Số mũ bí mật nhỏ

Để giảm thời gian giải mã (hoặc thời gian tạo chữ ký), người ta có thể muốn dùng một giá trị $d$ nhỏ thay vì một $d$ ngẫu nhiên. Vì phép lũy thừa mô-đun mất thời gian tuyến tính theo $\log_2d$, một $d$ nhỏ có thể cải thiện hiệu năng ít nhất 10 lần đối với mô-đun 1024 bit. Đáng tiếc, một cuộc tấn công tinh vi của M. Wiener [22] cho thấy một $d$ nhỏ dẫn tới việc phá vỡ hoàn toàn hệ mật mã.

**Định lý 2 (M. Wiener).** Cho $N=pq$ với

$$
q<p<2q.
$$

Cho

$$
d<\frac{1}{3}N^{1/4}.
$$

Khi biết $\langle N,e\rangle$ với

$$
ed=1\pmod{\varphi(N)},
$$

Marvin có thể khôi phục $d$ một cách hiệu quả.

**Chứng minh.** Chứng minh dựa trên phép xấp xỉ bằng phân số liên tục. Vì

$$
ed=1\pmod{\varphi(N)},
$$

nên tồn tại một $k$ sao cho

$$
ed-k\varphi(N)=1.
$$

Do đó,

$$
\left|\frac{e}{\varphi(N)}-\frac{k}{d}\right|
=\frac{1}{d\varphi(N)}.
$$

Vì vậy, $k/d$ là một xấp xỉ của $e/\varphi(N)$. Mặc dù Marvin không biết $\varphi(N)$, hắn có thể dùng $N$ để xấp xỉ nó. Thật vậy, vì

$$
\varphi(N)=N-p-q+1
$$

và

$$
p+q-1<3\sqrt N,
$$

nên

$$
|N-\varphi(N)|<3\sqrt N.
$$

Dùng $N$ thay cho $\varphi(N)$, ta thu được

$$
\begin{aligned}
\left|\frac{e}{N}-\frac{k}{d}\right|
&=\left|\frac{ed-k\varphi(N)-kN+k\varphi(N)}{Nd}\right|\\
&=\left|\frac{1-k(N-\varphi(N))}{Nd}\right|\\
&\le \frac{3k\sqrt N}{Nd}\\
&=\frac{3k}{d\sqrt N}.
\end{aligned}
$$

Bây giờ,

$$
k\varphi(N)=ed-1<ed.
$$

Vì $e<\varphi(N)$, ta có

$$
k<d<\frac{1}{3}N^{1/4}.
$$

Do đó,

$$
\left|\frac{e}{N}-\frac{k}{d}\right|
\le \frac{1}{dN^{1/4}}
<\frac{1}{2d^2}.
$$

Đây là một quan hệ xấp xỉ cổ điển. Số lượng phân số $k/d$ với $d<N$ có thể xấp xỉ $e/N$ sát đến mức này bị chặn bởi $\log_2N$. Thực tế, mọi phân số như vậy đều xuất hiện dưới dạng các phân số hội tụ của khai triển phân số liên tục của $e/N$ [12, Định lý 177]. Ta chỉ cần tính $\log N$ phân số hội tụ của phân số liên tục của $e/N$. Một trong số chúng sẽ bằng $k/d$. Vì

$$
ed-k\varphi(N)=1,
$$

ta có

$$
\gcd(k,d)=1,
$$

và do đó $k/d$ là một phân số tối giản. Đây là một thuật toán thời gian tuyến tính để khôi phục khóa bí mật $d$. $\square$

Vì thông thường $N$ dài 1024 bit, suy ra $d$ phải dài ít nhất 256 bit để tránh cuộc tấn công này. Điều đó không thuận lợi đối với các thiết bị công suất thấp như **thẻ thông minh**, nơi một $d$ nhỏ sẽ giúp tiết kiệm đáng kể. Tuy vậy, không phải mọi hy vọng đều mất. Wiener mô tả một số kỹ thuật cho phép giải mã nhanh mà không dễ bị cuộc tấn công của ông khai thác:

**$e$ lớn.** Giả sử thay vì rút gọn $e$ theo mô-đun $\varphi(N)$, ta dùng $\langle N,e'\rangle$ làm khóa công khai, trong đó

$$
e'=e+t\cdot\varphi(N)
$$

với một $t$ lớn. Rõ ràng $e'$ có thể được dùng thay cho $e$ để mã hóa thông điệp. Tuy nhiên, khi dùng một giá trị $e$ lớn, $k$ trong chứng minh ở trên không còn nhỏ nữa. Một phép tính đơn giản cho thấy nếu

$$
e'>N^{1.5},
$$

thì bất kể $d$ nhỏ đến đâu, cuộc tấn công trên cũng không thể thực hiện được. Đáng tiếc, giá trị $e$ lớn làm tăng thời gian mã hóa.

**Dùng CRT.** Một cách khác là dùng Định lý phần dư Trung Hoa (CRT). Giả sử ta chọn $d$ sao cho cả

$$
d_p=d\bmod(p-1)
$$

và

$$
d_q=d\bmod(q-1)
$$

đều nhỏ, chẳng hạn mỗi giá trị dài 128 bit. Khi đó, có thể giải mã nhanh bản mã $C$ như sau: trước hết tính

$$
M_p=C^{d_p}\bmod p
$$

và

$$
M_q=C^{d_q}\bmod q.
$$

Sau đó dùng CRT để tính giá trị duy nhất $M\in\mathbb{Z}_N$ thỏa mãn

$$
M=M_p\pmod p
$$

và

$$
M=M_q\pmod q.
$$

Giá trị $M$ thu được thỏa mãn

$$
M=C^d\bmod N
$$

như yêu cầu. Điểm quan trọng là mặc dù $d_p$ và $d_q$ nhỏ, giá trị

$$
d\bmod\varphi(N)
$$

vẫn có thể lớn, tức cỡ $\varphi(N)$. Vì vậy cuộc tấn công trong Định lý 2 không áp dụng được. Ta lưu ý rằng nếu biết $\langle N,e\rangle$, tồn tại một cuộc tấn công cho phép đối thủ phân tích $N$ thành thừa số trong thời gian

$$
O\!\left(\min\left(\sqrt{d_p},\sqrt{d_q}\right)\right).
$$

Vì thế, $d_p$ và $d_q$ không thể được làm quá nhỏ.

Chúng tôi không biết liệu một trong hai phương pháp trên có an toàn hay không. Tất cả những gì chúng tôi biết là cuộc tấn công của Wiener không hiệu quả đối với chúng. Định lý 2 gần đây được Boneh và Durfee [4] cải tiến; họ chỉ ra rằng miễn là

$$
d<N^{0.292},
$$

đối thủ có thể khôi phục $d$ một cách hiệu quả từ $\langle N,e\rangle$. Các kết quả này cho thấy cận của Wiener chưa chặt. Có khả năng cận đúng là

$$
d<N^{0.5}.
$$

Tại thời điểm bài viết này được viết, đây vẫn là một bài toán mở.

**Bài toán mở 2.** Cho $N=pq$ và

$$
d<N^{0.5}.
$$

Nếu Marvin được cho $\langle N,e\rangle$ với

$$
ed=1\pmod{\varphi(N)}
$$

và

$$
e<\varphi(N),
$$

hắn có thể khôi phục $d$ một cách hiệu quả hay không?

## 4. Số mũ công khai nhỏ

Để giảm thời gian mã hóa hoặc xác minh chữ ký, người ta thường dùng một số mũ công khai $e$ nhỏ. Giá trị nhỏ nhất có thể của $e$ là 3, nhưng để chống một số cuộc tấn công nhất định, giá trị

$$
e=2^{16}+1=65537
$$

được khuyến nghị. Khi dùng giá trị $2^{16}+1$, việc xác minh chữ ký cần 17 phép nhân, thay vì xấp xỉ 1000 phép nhân khi dùng một $e$ ngẫu nhiên thỏa mãn

$$
e\le\varphi(N).
$$

Không giống cuộc tấn công ở phần trước, các cuộc tấn công áp dụng khi dùng $e$ nhỏ còn rất xa mới có thể phá vỡ hoàn toàn hệ thống.

### 4.1. Định lý Coppersmith

Những cuộc tấn công mạnh nhất lên RSA với số mũ công khai nhỏ dựa trên một định lý của Coppersmith [7]. Định lý Coppersmith có nhiều ứng dụng, và ở đây chỉ trình bày một số trong đó. Chứng minh sử dụng thuật toán rút gọn cơ sở lưới LLL [17], như giải thích dưới đây.

**Định lý 3 (Coppersmith).** Cho $N$ là một số nguyên và $f\in\mathbb{Z}[x]$ là một đa thức monic bậc $d$. Đặt

$$
X=N^{1/d-\varepsilon}
$$

với một $\varepsilon\ge0$. Khi biết $\langle N,f\rangle$, Marvin có thể tìm hiệu quả **tất cả** các số nguyên $x_0$ thỏa mãn

$$
|x_0|<X
$$

và

$$
f(x_0)=0\pmod N.
$$

Thời gian chạy chủ yếu do thời gian chạy thuật toán LLL trên một lưới có số chiều $O(w)$, với

$$
w=\min(1/\varepsilon,\log_2N).
$$

Định lý cung cấp một thuật toán để tìm hiệu quả tất cả các nghiệm của $f$ theo mô-đun $N$ nhỏ hơn

$$
X=N^{1/d}.
$$

Khi $X$ nhỏ hơn, thời gian chạy của thuật toán giảm. Sức mạnh của định lý nằm ở khả năng tìm các nghiệm nhỏ của đa thức theo mô-đun một số hợp $N$. Khi làm việc theo mô-đun một số nguyên tố, không có lý do gì phải dùng định lý Coppersmith vì đã tồn tại các thuật toán tìm nghiệm khác tốt hơn nhiều.

Chúng tôi phác thảo những ý tưởng chính đằng sau chứng minh định lý Coppersmith. Chúng tôi theo một cách tiếp cận đơn giản hóa của Howgrave-Graham [14]. Với một đa thức

$$
h(x)=\sum_i a_ix^i\in\mathbb{Z}[x],
$$

định nghĩa

$$
\|h\|_2^2=\sum_i|a_i|^2.
$$

Chứng minh dựa trên quan sát sau.

**Bổ đề 4.** Cho $h(x)\in\mathbb{Z}[x]$ là một đa thức bậc $d$ và $X$ là một số nguyên dương. Giả sử

$$
\|h(xX)\|<\frac{N}{\sqrt d}.
$$

Nếu $|x_0|<X$ thỏa mãn

$$
h(x_0)=0\pmod N,
$$

thì trên các số nguyên ta có

$$
h(x_0)=0.
$$

**Chứng minh.** Từ bất đẳng thức Schwarz,

$$
\begin{aligned}
|h(x_0)|
&=\left|\sum_i a_ix_0^i\right|\\
&=\left|\sum_i a_iX^i\left(\frac{x_0}{X}\right)^i\right|\\
&\le \sum_i\left|a_iX^i\left(\frac{x_0}{X}\right)^i\right|\\
&\le \sum_i|a_iX^i|\\
&\le \sqrt d\,\|h(xX)\|\\
&<N.
\end{aligned}
$$

Vì $h(x_0)=0\pmod N$, suy ra $h(x_0)=0$ trên các số nguyên. $\square$

Bổ đề nói rằng nếu $h$ là một đa thức có chuẩn nhỏ thì mọi nghiệm nhỏ của $h\bmod N$ cũng là nghiệm của $h$ trên các số nguyên. Bổ đề gợi ý rằng để tìm một nghiệm nhỏ $x_0$ của $f(x)\bmod N$, ta nên tìm một đa thức khác $h\in\mathbb{Z}[x]$ có chuẩn nhỏ và có cùng các nghiệm với $f$ theo mô-đun $N$. Khi đó $x_0$ sẽ là nghiệm của $h$ trên các số nguyên và có thể tìm dễ dàng. Để làm như vậy, ta có thể tìm một đa thức $g\in\mathbb{Z}[x]$ sao cho

$$
h=gf
$$

có chuẩn nhỏ, tức chuẩn nhỏ hơn $N$. Điều này tương đương với việc tìm một tổ hợp tuyến tính nguyên có chuẩn nhỏ của các đa thức

$$
f,\;xf,\;x^2f,\;\ldots,\;x^rf.
$$

Đáng tiếc, trong phần lớn trường hợp không tồn tại một tổ hợp tuyến tính không tầm thường có chuẩn đủ nhỏ.

Coppersmith tìm ra một mẹo để giải quyết vấn đề: nếu

$$
f(x_0)=0\pmod N,
$$

thì với mọi $k$,

$$
f(x_0)^k=0\pmod{N^k}.
$$

Tổng quát hơn, định nghĩa các đa thức

$$
g_{u,v}(x)=N^{m-v}x^u f(x)^v
$$

với một $m$ được chọn trước. Khi đó $x_0$ là nghiệm của $g_{u,v}(x)$ theo mô-đun $N^m$ với mọi

$$
u\ge0
$$

và

$$
0\le v\le m.
$$

Để dùng Bổ đề 4, ta phải tìm một tổ hợp tuyến tính nguyên $h(x)$ của các đa thức $g_{u,v}(x)$ sao cho $h(xX)$ có chuẩn nhỏ hơn $N^m$; nhớ rằng $X$ là cận trên của $x_0$ và thỏa mãn

$$
X\le N^{1/d}.
$$

Nhờ cận trên của chuẩn được nới lỏng thành $N^m$ thay vì $N$, có thể chứng minh rằng với $m$ đủ lớn, luôn tồn tại một tổ hợp tuyến tính $h(x)$ thỏa mãn cận yêu cầu. Một khi tìm được $h(x)$, Bổ đề 4 suy ra rằng $x_0$ là nghiệm của $h$ trên các số nguyên. Do đó, có thể tìm $x_0$ dễ dàng.

Điều còn lại là chỉ ra cách tìm $h(x)$ một cách hiệu quả. Trước hết, ta cần nêu một số tính chất cơ bản của lưới trong $\mathbb{Z}^w$. Xem [17] để có phần giới thiệu ngắn gọn về chủ đề này. Cho

$$
u_1,\ldots,u_w\in\mathbb{Z}^w
$$

là các vectơ độc lập tuyến tính. Một lưới toàn hạng $L$ sinh bởi $\langle u_1,\ldots,u_w\rangle$ là tập tất cả các tổ hợp tuyến tính nguyên của $u_1,\ldots,u_w$. Định thức của $L$ được định nghĩa là định thức của ma trận vuông $w\times w$ có các hàng là các vectơ $u_1,\ldots,u_w$.

Trong trường hợp của chúng ta, ta xem các đa thức $g_{u,v}(xX)$ như các vectơ và nghiên cứu lưới $L$ do chúng sinh ra. Ta lấy

$$
v=0,\ldots,m
$$

và

$$
u=0,\ldots,d-1,
$$

nên lưới có số chiều

$$
w=d(m+1).
$$

Ví dụ, khi $f$ là một đa thức monic bậc hai và $m=3$, lưới thu được được sinh bởi các hàng của ma trận sau, trong đó các dấu $*$ là các hệ số của đa thức mà ta bỏ qua, còn mọi ô trống đều bằng 0:

$$
\begin{array}{c|cccccccc}
 & 1 & x & x^2 & x^3 & x^4 & x^5 & x^6 & x^7\\ \hline
g_{0,0}(xX) & N^3 \\
g_{1,0}(xX) &  & XN^3 \\
g_{0,1}(xX) & * & * & X^2N^2 \\
g_{1,1}(xX) &  & * & * & X^3N^2 \\
g_{0,2}(xX) & * & * & * & * & X^4N \\
g_{1,2}(xX) &  & * & * & * & * & X^5N \\
g_{0,3}(xX) & * & * & * & * & * & * & X^6 \\
g_{1,3}(xX) &  & * & * & * & * & * & * & X^7
\end{array}
$$

Vì ma trận là tam giác, định thức của nó là tích các phần tử trên đường chéo, tức những phần tử được ghi rõ ở trên. Mục tiêu của chúng ta là tìm các vectơ ngắn trong lưới này.

Một kết quả cổ điển của Hermite phát biểu rằng mọi lưới $L$ số chiều $w$ đều chứa một điểm khác không $v\in L$ có chuẩn $L_2$ thỏa mãn

$$
\|v\|\le\gamma_w\det(L)^{1/w},
$$

trong đó $\gamma_w$ là một hằng số chỉ phụ thuộc vào $w$. Cận Hermite có thể được dùng để chỉ ra rằng với $m$ đủ lớn, lưới của chúng ta chứa các vectơ có chuẩn nhỏ hơn $N^m$, như yêu cầu. Câu hỏi là liệu ta có thể xây dựng hiệu quả một vectơ ngắn trong $L$ có độ dài không lớn hơn cận Hermite quá nhiều hay không. Thuật toán LLL là một thuật toán hiệu quả thực hiện chính xác việc đó.

**Mệnh đề 5 (LLL).** Cho $L$ là một lưới sinh bởi $\langle u_1,\ldots,u_w\rangle$. Khi $\langle u_1,\ldots,u_w\rangle$ được đưa vào làm đầu vào, thuật toán LLL xuất ra một điểm $v\in L$ thỏa mãn

$$
\|v\|\le 2^{w/4}\det(L)^{1/w}.
$$

Thời gian chạy của LLL là bậc bốn theo độ dài đầu vào.

Thuật toán LLL, được đặt tên theo những người phát minh ra nó là L. Lovász, A. Lenstra và H. Lenstra Jr., có nhiều ứng dụng trong cả lý thuyết số tính toán lẫn mật mã học. Việc phát hiện ra LLL vào năm 1982 cung cấp một thuật toán hiệu quả để phân tích đa thức trên các số nguyên và, tổng quát hơn, trên các vành số. LLL thường xuyên được dùng để tấn công nhiều hệ mật mã. Chẳng hạn, nhiều hệ mật mã dựa trên **bài toán ba lô** đã bị phá bằng LLL.

Dùng LLL, ta có thể hoàn tất chứng minh định lý Coppersmith. Để bảo đảm vectơ do LLL tạo ra thỏa mãn cận trong Bổ đề 4, ta cần

$$
2^{w/4}\det(L)^{1/w}<\frac{N^m}{\sqrt w},
$$

trong đó

$$
w=d(m+1)
$$

là số chiều của $L$. Một phép tính thông thường cho thấy khi $m$ đủ lớn thì cận này được thỏa mãn. Cụ thể, khi

$$
X=N^{1/d-\varepsilon},
$$

chỉ cần chọn

$$
m=O(k/d)
$$

với

$$
k=\min(1/\varepsilon,\log N).
$$

Do đó, thời gian chạy chủ yếu là thời gian chạy LLL trên một lưới có số chiều $O(k)$, như yêu cầu.

Một câu hỏi tự nhiên là liệu định lý Coppersmith có thể áp dụng cho các đa thức hai biến và nhiều biến hay không. Nếu cho

$$
f(x,y)\in\mathbb{Z}_N[x,y]
$$

mà tồn tại một nghiệm $(x_0,y_0)$ với $|x_0y_0|$ bị chặn thích hợp, Marvin có thể tìm $(x_0,y_0)$ một cách hiệu quả hay không? Mặc dù cùng một kỹ thuật có vẻ hoạt động đối với một số đa thức hai biến, hiện vẫn là một bài toán mở để chứng minh điều này. Khi ngày càng nhiều kết quả phụ thuộc vào một phiên bản mở rộng hai biến của định lý Coppersmith, một thuật toán chặt chẽ sẽ rất hữu ích.

**Bài toán mở 3.** Tìm các điều kiện tổng quát mà dưới đó định lý Coppersmith có thể được mở rộng cho các đa thức hai biến.

### 4.2. Cuộc tấn công phát quảng bá của Hastad

Là ứng dụng đầu tiên của định lý Coppersmith, chúng tôi trình bày một cải tiến đối với một cuộc tấn công cũ của Hastad [13]. Giả sử Bob muốn gửi một thông điệp mã hóa $M$ cho nhiều bên

$$
P_1,P_2,\ldots,P_k.
$$

Mỗi bên có khóa RSA riêng

$$
\langle N_i,e_i\rangle.
$$

Ta giả sử $M$ nhỏ hơn mọi $N_i$. Một cách ngây thơ, để gửi $M$, Bob mã hóa nó bằng từng khóa công khai rồi gửi bản mã thứ $i$ cho $P_i$. Kẻ tấn công Marvin có thể nghe lén đường truyền mà Bob không phát hiện và thu thập $k$ bản mã được truyền đi.

Để đơn giản, giả sử mọi số mũ công khai $e_i$ đều bằng 3. Một lập luận đơn giản cho thấy Marvin có thể khôi phục $M$ nếu

$$
k\ge3.
$$

Thật vậy, Marvin thu được $C_1,C_2,C_3$, trong đó

$$
C_1=M^3\bmod N_1,
$$

$$
C_2=M^3\bmod N_2,
$$

và

$$
C_3=M^3\bmod N_3.
$$

Ta có thể giả sử

$$
\gcd(N_i,N_j)=1
$$

với mọi $i\ne j$, vì nếu không Marvin có thể phân tích một số $N_i$ thành thừa số. Do đó, áp dụng Định lý phần dư Trung Hoa lên $C_1,C_2,C_3$ cho ta một

$$
C'\in\mathbb{Z}_{N_1N_2N_3}
$$

thỏa mãn

$$
C'=M^3\pmod{N_1N_2N_3}.
$$

Vì $M$ nhỏ hơn mọi $N_i$, ta có

$$
M^3<N_1N_2N_3.
$$

Khi đó trên các số nguyên,

$$
C'=M^3.
$$

Vì vậy Marvin có thể khôi phục $M$ bằng cách tính căn bậc ba thực của $C'$. Tổng quát hơn, nếu mọi số mũ công khai đều bằng $e$, Marvin có thể khôi phục $M$ ngay khi

$$
k\ge e.
$$

Cuộc tấn công chỉ khả thi khi dùng $e$ nhỏ.

Hastad [13] mô tả một cuộc tấn công mạnh hơn nhiều. Để tạo động lực cho kết quả của Hastad, hãy xét một cách phòng vệ ngây thơ trước cuộc tấn công trên. Thay vì phát quảng bá bản mã của $M$, Bob có thể **đệm** thông điệp trước khi mã hóa. Chẳng hạn, nếu $M$ dài $m$ bit, Bob có thể gửi

$$
M_i=i2^m+M
$$

cho bên $P_i$. Vì Marvin thu được các bản mã của những thông điệp khác nhau, hắn không thể thực hiện cuộc tấn công vừa nêu.

Đáng tiếc, Hastad chỉ ra rằng phép đệm tuyến tính này không an toàn. Thực tế, ông chứng minh rằng áp dụng bất kỳ đa thức cố định nào lên thông điệp trước khi mã hóa cũng không ngăn được cuộc tấn công.

Giả sử với mỗi bên tham gia $P_1,\ldots,P_k$, Bob có một đa thức công khai cố định

$$
f_i\in\mathbb{Z}_{N_i}[x].
$$

Để phát quảng bá thông điệp $M$, Bob gửi bản mã của $f_i(M)$ cho bên $P_i$. Bằng cách nghe lén, Marvin thu được

$$
C_i=f_i(M)^{e_i}\bmod N_i
$$

với $i=1,\ldots,k$. Hastad chỉ ra rằng nếu có đủ số bên tham gia, Marvin có thể khôi phục bản rõ $M$ từ tất cả các bản mã. Định lý sau là một phiên bản mạnh hơn kết quả gốc của Hastad.

**Định lý 6 (Hastad).** Cho $N_1,\ldots,N_k$ là các số nguyên đôi một nguyên tố cùng nhau và đặt

$$
N_{\min}=\min_i(N_i).
$$

Cho

$$
g_i\in\mathbb{Z}_{N_i}[x]
$$

là $k$ đa thức có bậc lớn nhất bằng $d$. Giả sử tồn tại duy nhất một $M<N_{\min}$ thỏa mãn

$$
g_i(M)=0\pmod{N_i}
$$

với mọi $i=1,\ldots,k$. Với giả thiết

$$
k>d,
$$

ta có thể tìm hiệu quả $M$ khi biết

$$
\langle N_i,g_i\rangle_{i=1}^k.
$$

**Chứng minh.** Đặt

$$
N=N_1\cdots N_k.
$$

Ta có thể giả sử mọi $g_i$ đều monic. Thật vậy, nếu với một $i$ nào đó, hệ số bậc cao nhất của $g_i$ không khả nghịch trong $\mathbb{Z}_{N_i}^*$, thì phân tích thừa số của $N_i$ sẽ bị lộ. Bằng cách nhân mỗi $g_i$ với một lũy thừa thích hợp của $x$, ta có thể giả sử tất cả chúng đều có bậc $d$. Xây dựng đa thức

$$
g(x)=\sum_{i=1}^k T_i g_i(x),
$$

trong đó $T_i$ thỏa mãn

$$
T_i=
\begin{cases}
1\pmod{N_j}, & i=j,\\
0\pmod{N_j}, & i\ne j.
\end{cases}
$$

Các $T_i$ là những số nguyên được gọi là **các hệ số phần dư Trung Hoa**. Khi đó $g(x)$ phải là monic vì nó monic theo mô-đun mọi $N_i$. Bậc của nó là $d$. Hơn nữa, ta biết rằng

$$
g(M)=0\pmod N.
$$

Định lý 6 giờ suy ra từ Định lý 3 vì

$$
M<N_{\min}\le N^{1/k}<N^{1/d}.
$$

$\square$

Định lý cho thấy một hệ các phương trình một biến theo mô-đun những số hợp đôi một nguyên tố cùng nhau có thể được giải hiệu quả, miễn là cung cấp đủ số phương trình. Bằng cách đặt

$$
g_i=f_i^{e_i}-C_i\pmod{N_i},
$$

ta thấy Marvin có thể khôi phục $M$ từ các bản mã đã cho bất cứ khi nào số lượng các bên ít nhất bằng $d$, trong đó $d$ là giá trị lớn nhất của

$$
e_i\deg(f_i)
$$

trên mọi $i=1,\ldots,k$. Đặc biệt, nếu mọi $e_i$ đều bằng $e$ và Bob gửi các thông điệp liên hệ tuyến tính với nhau, Marvin có thể khôi phục bản rõ ngay khi

$$
k>e.
$$

Định lý gốc của Hastad yếu hơn định lý nêu ở trên. Thay vì $d$ đa thức, Hastad yêu cầu

$$
\frac{d(d+1)}{2}
$$

đa thức. Chứng minh của Hastad tương tự chứng minh định lý Coppersmith được mô tả ở phần trước. Tuy nhiên, Hastad không dùng các lũy thừa của $g$ trong lưới và vì vậy thu được một cận yếu hơn.

Kết thúc phần này, chúng tôi lưu ý rằng để phòng vệ đúng cách trước cuộc tấn công phát quảng bá ở trên, phải dùng **phép đệm ngẫu nhiên** [1] thay vì phép đệm cố định.

### 4.3. Cuộc tấn công thông điệp liên quan Franklin-Reiter

Franklin và Reiter [8] tìm ra một cuộc tấn công tinh vi khi Bob gửi cho Alice các thông điệp mã hóa có liên hệ với nhau bằng cùng một mô-đun. Cho $\langle N,e\rangle$ là khóa công khai của Alice. Giả sử

$$
M_1,M_2\in\mathbb{Z}_N^*
$$

là hai thông điệp khác nhau thỏa mãn

$$
M_1=f(M_2)\pmod N
$$

với một đa thức công khai

$$
f\in\mathbb{Z}_N[x].
$$

Để gửi $M_1$ và $M_2$ cho Alice, Bob có thể ngây thơ mã hóa các thông điệp rồi truyền đi các bản mã $C_1,C_2$. Chúng tôi chỉ ra rằng khi biết $C_1,C_2$, Marvin có thể dễ dàng khôi phục $M_1,M_2$. Mặc dù cuộc tấn công hoạt động với mọi $e$ nhỏ, chúng tôi phát biểu bổ đề sau cho $e=3$ để đơn giản hóa chứng minh.

**Bổ đề 7 (FR).** Đặt $e=3$ và cho $\langle N,e\rangle$ là một khóa công khai RSA. Cho

$$
M_1\ne M_2\in\mathbb{Z}_N^*
$$

thỏa mãn

$$
M_1=f(M_2)\pmod N
$$

với một đa thức tuyến tính

$$
f=ax+b\in\mathbb{Z}_N[x]
$$

và $b\ne0$. Khi biết

$$
\langle N,e,C_1,C_2,f\rangle,
$$

Marvin có thể khôi phục $M_1,M_2$ trong thời gian bậc hai theo $\log N$.

**Chứng minh.** Để giữ phần chứng minh này ở dạng tổng quát, ta phát biểu nó với một $e$ bất kỳ thay vì giới hạn ở $e=3$. Vì

$$
C_1=M_1^e\bmod N,
$$

ta biết $M_2$ là nghiệm của đa thức

$$
g_1(x)=f(x)^e-C_1\in\mathbb{Z}_N[x].
$$

Tương tự, $M_2$ là nghiệm của

$$
g_2(x)=x^e-C_2\in\mathbb{Z}_N[x].
$$

Nhân tử tuyến tính

$$
x-M_2
$$

chia cả hai đa thức. Vì vậy Marvin có thể dùng thuật toán Euclid[^4] để tính

$$
\gcd(g_1,g_2).
$$

Nếu ước chung lớn nhất thu được là tuyến tính thì $M_2$ được tìm thấy. GCD có thể được tính trong thời gian bậc hai theo $e$ và $\log N$.

Ta chứng minh rằng khi $e=3$, GCD bắt buộc phải tuyến tính. Đa thức

$$
x^3-C_2
$$

phân tích theo cả mô-đun $p$ và mô-đun $q$ thành một nhân tử tuyến tính và một nhân tử bậc hai bất khả quy; nhớ rằng

$$
\gcd(e,\varphi(N))=1,
$$

nên $x^3-C_2$ chỉ có một nghiệm trong $\mathbb{Z}_N$. Vì $g_2$ không thể chia $g_1$, GCD phải là tuyến tính. Với $e>3$, GCD gần như luôn tuyến tính. Tuy nhiên, đối với một số trường hợp hiếm của $M_1,M_2$ và $f$, có thể thu được một GCD phi tuyến, khi đó cuộc tấn công thất bại. $\square$

Với $e>3$, cuộc tấn công mất thời gian bậc hai theo $e$. Do đó, nó chỉ áp dụng được khi dùng số mũ công khai nhỏ $e$. Với $e$ lớn, công việc tính GCD trở nên quá tốn kém. Một câu hỏi thú vị — dù có lẽ rất khó — là liệu có thể xây dựng một cuộc tấn công như vậy với $e$ tùy ý hay không. Cụ thể, GCD của $g_1$ và $g_2$ ở trên có thể được tìm trong thời gian đa thức theo $\log e$ hay không?

### 4.4. Cuộc tấn công đệm ngắn của Coppersmith

Cuộc tấn công Franklin-Reiter có thể trông hơi nhân tạo. Suy cho cùng, tại sao Bob lại gửi cho Alice bản mã của những thông điệp có liên hệ với nhau? Coppersmith đã tăng cường cuộc tấn công và chứng minh một kết quả quan trọng về phép đệm [7].

Một thuật toán đệm ngẫu nhiên ngây thơ có thể đệm bản rõ $M$ bằng cách nối thêm một vài bit ngẫu nhiên vào một trong hai đầu. Cuộc tấn công sau chỉ ra nguy cơ của kiểu đệm quá đơn giản này. Giả sử Bob gửi cho Alice một bản mã của $M$ đã được đệm đúng cách. Kẻ tấn công Marvin chặn bản mã và ngăn nó tới đích. Bob nhận thấy Alice không phản hồi thông điệp của mình và quyết định gửi lại $M$ cho Alice. Anh ta đệm ngẫu nhiên $M$ rồi truyền bản mã thu được. Bây giờ Marvin có hai bản mã tương ứng với hai lần mã hóa cùng một thông điệp bằng hai phần đệm ngẫu nhiên khác nhau. Định lý sau cho thấy mặc dù không biết các phần đệm đã dùng, Marvin vẫn có thể khôi phục bản rõ.

**Định lý 8.** Cho $\langle N,e\rangle$ là một khóa công khai RSA, trong đó $N$ dài $n$ bit. Đặt

$$
m=\left\lfloor\frac{n}{e^2}\right\rfloor.
$$

Cho $M\in\mathbb{Z}_N^*$ là một thông điệp có độ dài không quá $n-m$ bit. Định nghĩa

$$
M_1=2^mM+r_1
$$

và

$$
M_2=2^mM+r_2,
$$

trong đó $r_1,r_2$ là hai số nguyên khác nhau thỏa mãn

$$
0\le r_1,r_2<2^m.
$$

Nếu Marvin được cho $\langle N,e\rangle$ và các bản mã $C_1,C_2$ của $M_1,M_2$ nhưng không được cho $r_1$ hay $r_2$, hắn có thể khôi phục $M$ một cách hiệu quả.

**Chứng minh.** Định nghĩa

$$
g_1(x,y)=x^e-C_1
$$

và

$$
g_2(x,y)=(x+y)^e-C_2.
$$

Ta biết rằng khi

$$
y=r_2-r_1,
$$

hai đa thức này có nghiệm chung $M_1$. Nói cách khác,

$$
\Delta=r_2-r_1
$$

là một nghiệm của **resultant**

$$
h(y)=\operatorname{res}_x(g_1,g_2)\in\mathbb{Z}_N[y].
$$

Bậc của $h$ không quá $e^2$. Hơn nữa,

$$
|\Delta|<2^m<N^{1/e^2}.
$$

Vì vậy, $\Delta$ là một nghiệm nhỏ của $h$ theo mô-đun $N$, và Marvin có thể tìm nó hiệu quả bằng định lý Coppersmith (Định lý 3). Khi đã biết $\Delta$, có thể dùng cuộc tấn công Franklin-Reiter của phần trước để khôi phục $M_2$ và do đó khôi phục $M$. $\square$

Khi $e=3$, cuộc tấn công có thể thực hiện miễn là độ dài phần đệm nhỏ hơn $1/9$ độ dài thông điệp. Đây là một kết quả quan trọng. Lưu ý rằng với giá trị $e=65537$ được khuyến nghị, cuộc tấn công không có tác dụng đối với các kích thước mô-đun tiêu chuẩn.

### 4.5. Cuộc tấn công làm lộ một phần khóa

Cho $\langle N,d\rangle$ là một khóa riêng RSA. Giả sử bằng cách nào đó Marvin có thể làm lộ một phần các bit của $d$, chẳng hạn một phần tư số bit. Hắn có thể khôi phục phần còn lại của $d$ hay không? Đáng ngạc nhiên, câu trả lời là có khi khóa công khai tương ứng nhỏ. Gần đây, Boneh, Durfee và Frankel [5] chỉ ra rằng miễn là

$$
e<\sqrt N,
$$

có thể khôi phục toàn bộ $d$ chỉ từ một phần các bit của nó. Các kết quả này minh họa tầm quan trọng của việc bảo vệ **toàn bộ** khóa riêng RSA.

**Định lý 9 (BDF).** Cho $\langle N,d\rangle$ là một khóa riêng RSA, trong đó $N$ dài $n$ bit. Khi biết

$$
\lceil n/4\rceil
$$

bit có trọng số thấp nhất của $d$, Marvin có thể khôi phục toàn bộ $d$ trong thời gian tuyến tính theo

$$
e\log_2e.
$$

Chứng minh dựa trên một định lý đẹp khác của Coppersmith [7].

**Định lý 10 (Coppersmith).** Cho $N=pq$ là một mô-đun RSA dài $n$ bit. Khi biết $n/4$ bit có trọng số thấp nhất của $p$ hoặc $n/4$ bit có trọng số cao nhất của $p$, ta có thể phân tích $N$ thành thừa số một cách hiệu quả.

Định lý 9 suy ra trực tiếp từ Định lý 10. Thật vậy, theo định nghĩa của $e$ và $d$, tồn tại một số nguyên $k$ sao cho

$$
ed-k(N-p-q+1)=1.
$$

Vì

$$
d<\varphi(N),
$$

ta phải có

$$
0<k\le e.
$$

Lấy phương trình theo mô-đun $2^{n/4}$ và đặt

$$
q=N/p,
$$

ta thu được

$$
(ed)p-kp(N-p+1)+kN=p\pmod{2^{n/4}}.
$$

Vì Marvin được cho $n/4$ bit có trọng số thấp nhất của $d$, hắn biết giá trị

$$
ed\bmod 2^{n/4}.
$$

Do đó, hắn thu được một phương trình theo $k$ và $p$. Với mỗi trong số $e$ giá trị có thể của $k$, Marvin giải phương trình bậc hai theo $p$ và thu được một số giá trị ứng viên cho

$$
p\bmod 2^{n/4}.
$$

Với mỗi giá trị ứng viên này, hắn chạy thuật toán của Định lý 10 để thử phân tích $N$. Có thể chứng minh rằng tổng số giá trị ứng viên của

$$
p\bmod2^{n/4}
$$

không quá

$$
e\log_2e.
$$

Do đó, sau nhiều nhất $e\log_2e$ lần thử, $N$ sẽ bị phân tích thành thừa số.

Định lý 9 được gọi là một **cuộc tấn công làm lộ một phần khóa**. Các cuộc tấn công tương tự tồn tại đối với các giá trị $e$ lớn hơn miễn là

$$
e<\sqrt N.
$$

Tuy nhiên, các kỹ thuật khi đó phức tạp hơn đôi chút [5]. Điều thú vị là các hệ mật mã dựa trên logarit rời rạc, chẳng hạn hệ khóa công khai ElGamal, dường như không dễ bị tấn công do làm lộ một phần khóa. Thật vậy, nếu biết

$$
g^x\bmod p
$$

và biết một tỉ lệ hằng số các bit của $x$, hiện không có thuật toán thời gian đa thức nào đã biết có thể tính phần còn lại của $x$.

Kết thúc phần này, chúng tôi chỉ ra rằng khi số mũ mã hóa $e$ nhỏ, hệ RSA làm lộ một nửa các bit có trọng số cao nhất của khóa riêng tương ứng $d$. Để thấy điều này, xét lại phương trình

$$
ed-k(N-p-q+1)=1
$$

với một số nguyên

$$
0<k\le e.
$$

Khi biết $k$, Marvin có thể dễ dàng tính

$$
\tilde d=\left\lfloor\frac{kN+1}{e}\right\rfloor.
$$

Khi đó

$$
|\tilde d-d|
\le \frac{k(p+q)}{e}
\le \frac{3k\sqrt N}{e}
<3\sqrt N.
$$

Vì vậy, $\tilde d$ là một xấp xỉ tốt của $d$. Cận trên cho thấy đối với phần lớn $d$, một nửa các bit có trọng số cao nhất của $\tilde d$ bằng với các bit tương ứng của $d$. Vì chỉ có $e$ giá trị có thể của $k$, Marvin có thể xây dựng một tập nhỏ kích thước $e$ sao cho một trong các phần tử của tập bằng một nửa các bit có trọng số cao nhất của $d$. Trường hợp $e=3$ đặc biệt thú vị. Trong trường hợp này có thể chứng minh rằng luôn luôn $k=2$, và do đó hệ thống làm lộ hoàn toàn một nửa các bit có trọng số cao nhất của $d$.

## 5. Các cuộc tấn công vào triển khai

Bây giờ chúng ta chuyển sự chú ý sang một lớp tấn công hoàn toàn khác. Thay vì tấn công cấu trúc nền tảng của hàm RSA, những cuộc tấn công này tập trung vào cách RSA được triển khai.

### 5.1. Tấn công thời gian

Xét một thẻ thông minh lưu một khóa riêng RSA. Vì thẻ có khả năng chống can thiệp vật lý, kẻ tấn công Marvin có thể không thể kiểm tra nội dung bên trong để làm lộ khóa. Tuy nhiên, một cuộc tấn công tinh vi của Kocher [16] cho thấy bằng cách đo chính xác thời gian thẻ thông minh thực hiện một phép giải mã RSA hoặc tạo chữ ký, Marvin có thể nhanh chóng khám phá số mũ giải mã bí mật $d$.

Chúng tôi giải thích cách thực hiện cuộc tấn công lên một triển khai RSA đơn giản dùng **thuật toán bình phương lặp**. Cho

$$
d=d_nd_{n-1}\ldots d_0
$$

là biểu diễn nhị phân của $d$, tức

$$
d=\sum_{i=0}^n2^id_i,
$$

với

$$
d_i\in\{0,1\}.
$$

Thuật toán bình phương lặp tính

$$
C=M^d\bmod N
$$

bằng nhiều nhất $2n$ phép nhân mô-đun. Nó dựa trên quan sát

$$
C=\prod_{i=0}^n M^{2^id_i}\bmod N.
$$

Thuật toán hoạt động như sau:

- Đặt $z=M$ và $C=1$.
- Với $i=0,\ldots,n$, thực hiện:
  1. nếu $d_i=1$, đặt $C=C\cdot z\bmod N$;
  2. đặt $z=z^2\bmod N$.
- Cuối cùng, $C$ có giá trị $M^d\bmod N$.

Biến $z$ lần lượt nhận các giá trị trong tập

$$
M^{2^i}\bmod N,
$$

với $i=0,\ldots,n$. Biến $C$ “thu thập” các lũy thừa thích hợp trong tập để thu được

$$
M^d\bmod N.
$$

Để thực hiện cuộc tấn công, Marvin yêu cầu thẻ thông minh tạo chữ ký trên một số lượng lớn các thông điệp ngẫu nhiên

$$
M_1,\ldots,M_k\in\mathbb{Z}_N^*
$$

và đo thời gian $T_i$ mà thẻ mất để tạo từng chữ ký.

Cuộc tấn công khôi phục từng bit của $d$, bắt đầu từ bit có trọng số thấp nhất. Ta biết $d$ là số lẻ, do đó

$$
d_0=1.
$$

Xét vòng lặp thứ hai. Ban đầu,

$$
z=M^2\bmod N
$$

và

$$
C=M.
$$

Nếu $d_1=1$, thẻ thông minh tính tích

$$
C\cdot z=M\cdot M^2\bmod N.
$$

Nếu không, phép tính này không được thực hiện. Gọi $t_i$ là thời gian thẻ thông minh cần để tính

$$
M_i\cdot M_i^2\bmod N.
$$

Các $t_i$ khác nhau vì thời gian tính $M_i\cdot M_i^2\bmod N$ phụ thuộc vào giá trị của $M_i$; các thuật toán rút gọn mô-đun đơn giản mất thời gian khác nhau tùy vào giá trị được rút gọn. Marvin đo các $t_i$ ngoại tuyến trước khi thực hiện cuộc tấn công, sau khi thu được các đặc tả vật lý của thẻ.

Kocher quan sát rằng khi $d_1=1$, hai tập giá trị

$$
\{t_i\}
$$

và

$$
\{T_i\}
$$

có tương quan. Chẳng hạn, nếu với một $i$ nào đó, $t_i$ lớn hơn nhiều so với kỳ vọng thì $T_i$ cũng có khả năng lớn hơn kỳ vọng. Ngược lại, nếu $d_1=0$, hai tập $\{t_i\}$ và $\{T_i\}$ hành xử như những biến ngẫu nhiên độc lập. Bằng cách đo tương quan, Marvin có thể xác định $d_1$ bằng 0 hay 1.

Tiếp tục theo cách này, hắn có thể khôi phục $d_2,d_3$, v.v. Lưu ý rằng khi sử dụng một số mũ công khai nhỏ $e$, cuộc tấn công làm lộ một phần khóa ở phần trước cho thấy cuộc tấn công thời gian của Kocher chỉ cần được dùng cho đến khi phát hiện được một phần tư số bit của $d$.

Có hai cách phòng vệ trước cuộc tấn công. Cách đơn giản nhất là thêm độ trễ thích hợp sao cho phép lũy thừa mô-đun luôn mất một lượng thời gian cố định. Cách thứ hai, do Rivest đề xuất, dựa trên kỹ thuật làm mù. Trước khi giải mã $M$, thẻ thông minh chọn ngẫu nhiên

$$
r\in\mathbb{Z}_N^*
$$

và tính

$$
M'=M\cdot r^e\bmod N.
$$

Sau đó nó áp dụng $d$ lên $M'$ và thu được

$$
C'=(M')^d\bmod N.
$$

Cuối cùng, thẻ đặt

$$
C=C'/r\bmod N.
$$

Với cách này, thẻ thông minh áp dụng $d$ lên một thông điệp ngẫu nhiên $M'$ mà Marvin không biết. Vì vậy Marvin không thể thực hiện cuộc tấn công.

Kocher gần đây phát hiện một cuộc tấn công khác theo cùng hướng này, gọi là **phân tích mật mã qua công suất** (*power cryptanalysis*). Kocher chỉ ra rằng bằng cách đo chính xác mức tiêu thụ điện của thẻ thông minh trong quá trình tạo chữ ký, Marvin thường có thể dễ dàng phát hiện khóa bí mật. Thực tế, trong một phép nhân đa độ chính xác, mức tiêu thụ điện của thẻ cao hơn bình thường. Bằng cách đo độ dài các khoảng thời gian tiêu thụ điện cao, Marvin có thể dễ dàng xác định ở một vòng lặp nhất định thẻ thực hiện một hay hai phép nhân, từ đó làm lộ các bit của $d$.

### 5.2. Lỗi ngẫu nhiên

Các triển khai giải mã và chữ ký RSA thường dùng Định lý phần dư Trung Hoa để tăng tốc việc tính

$$
M^d\bmod N.
$$

Thay vì làm việc trực tiếp theo mô-đun $N$, người ký Bob trước hết tính chữ ký theo mô-đun $p$ và $q$, sau đó kết hợp kết quả bằng Định lý phần dư Trung Hoa. Cụ thể hơn, Bob trước hết tính

$$
C_p=M^{d_p}\bmod p
$$

và

$$
C_q=M^{d_q}\bmod q,
$$

trong đó

$$
d_p=d\bmod(p-1)
$$

và

$$
d_q=d\bmod(q-1).
$$

Sau đó, Bob thu được chữ ký $C$ bằng cách đặt

$$
C=T_1C_p+T_2C_q\pmod N,
$$

trong đó

$$
T_1=
\begin{cases}
1\pmod p,\\
0\pmod q,
\end{cases}
$$

và

$$
T_2=
\begin{cases}
0\pmod p,\\
1\pmod q.
\end{cases}
$$

Thời gian chạy của bước CRT cuối cùng không đáng kể so với hai phép lũy thừa. Lưu ý rằng $p$ và $q$ chỉ dài bằng một nửa $N$. Vì các triển khai phép nhân đơn giản mất thời gian bậc hai, phép nhân theo mô-đun $p$ nhanh gấp bốn lần theo mô-đun $N$. Hơn nữa, $d_p$ chỉ dài bằng một nửa $d$, do đó tính

$$
M^{d_p}\bmod p
$$

nhanh gấp tám lần tính

$$
M^d\bmod N.
$$

Tổng thể, thời gian tạo chữ ký giảm đi khoảng bốn lần. Nhiều triển khai dùng phương pháp này để cải thiện hiệu năng.

Boneh, DeMillo và Lipton [3] quan sát rằng việc dùng phương pháp CRT tiềm ẩn một nguy cơ. Giả sử trong khi tạo chữ ký, một trục trặc trên máy tính của Bob khiến một lệnh duy nhất bị tính sai. Chẳng hạn, khi sao chép một thanh ghi từ vị trí này sang vị trí khác, một bit bị lật. Một trục trặc như vậy có thể do nhiễu điện từ môi trường hoặc có lẽ do một lỗi phần cứng hiếm gặp, giống lỗi từng xuất hiện trong một phiên bản đầu của chip Pentium. Khi có một chữ ký không hợp lệ, đối thủ Marvin có thể dễ dàng phân tích mô-đun $N$ của Bob thành thừa số.

Chúng tôi trình bày một phiên bản của cuộc tấn công theo mô tả của A. K. Lenstra. Giả sử xảy ra đúng một lỗi khi Bob tạo chữ ký. Kết quả là chính xác một trong hai giá trị $C_p$ hoặc $C_q$ sẽ bị tính sai. Giả sử $C_p$ đúng nhưng $\widehat C_q$ sai. Chữ ký thu được là

$$
\widehat C=T_1C_p+T_2\widehat C_q.
$$

Khi Marvin nhận $\widehat C$, hắn biết đây là một chữ ký sai vì

$$
\widehat C^e\ne M\pmod N.
$$

Tuy nhiên, chú ý rằng

$$
\widehat C^e=M\pmod p
$$

trong khi

$$
\widehat C^e\ne M\pmod q.
$$

Do đó,

$$
\gcd(N,\widehat C^e-M)
$$

làm lộ một thừa số không tầm thường của $N$.

Để cuộc tấn công hoạt động, Marvin phải biết đầy đủ $M$. Nói cách khác, ta đang giả sử Bob không dùng bất kỳ thủ tục đệm ngẫu nhiên nào. Đệm ngẫu nhiên trước khi ký sẽ đánh bại cuộc tấn công. Một cách phòng vệ đơn giản hơn là Bob kiểm tra chữ ký vừa tạo trước khi gửi nó ra bên ngoài. Việc kiểm tra đặc biệt quan trọng khi dùng phương pháp tăng tốc CRT. Lỗi ngẫu nhiên gây nguy hiểm cho nhiều hệ mật mã. Nhiều hệ thống, kể cả triển khai RSA không dùng CRT, có thể bị tấn công bằng lỗi ngẫu nhiên [3]. Tuy nhiên, những kết quả này mang tính lý thuyết nhiều hơn.

### 5.3. Cuộc tấn công của Bleichenbacher lên PKCS 1

Cho $N$ là một mô-đun RSA dài $n$ bit và $M$ là một thông điệp dài $m$ bit với

$$
m<n.
$$

Trước khi áp dụng mã hóa RSA, một cách tự nhiên là đệm thông điệp $M$ lên $n$ bit bằng cách nối thêm các bit ngẫu nhiên. Một phiên bản cũ của tiêu chuẩn có tên **Public Key Cryptography Standard 1 (PKCS 1)** sử dụng cách tiếp cận này. Sau khi đệm, thông điệp có dạng:

```text
02   Random   00   M
```

Thông điệp thu được dài $n$ bit và được mã hóa trực tiếp bằng RSA. Khối đầu tiên chứa `02` dài 16 bit và dùng để chỉ ra rằng một phần đệm ngẫu nhiên đã được thêm vào thông điệp.

Khi một thông điệp PKCS 1 được máy của Bob nhận, một ứng dụng — chẳng hạn trình duyệt web — giải mã nó, kiểm tra khối đầu và loại bỏ phần đệm ngẫu nhiên. Tuy nhiên, một số ứng dụng kiểm tra khối đầu `02`, và nếu khối này không xuất hiện thì chúng trả về thông báo lỗi “bản mã không hợp lệ”. Bleichenbacher [2] chỉ ra rằng thông báo lỗi này có thể dẫn tới hậu quả nghiêm trọng: bằng cách sử dụng thông báo lỗi, kẻ tấn công Marvin có thể giải mã các bản mã do hắn lựa chọn.

Giả sử Marvin chặn một bản mã $C$ dành cho Bob và muốn giải mã nó. Để thực hiện cuộc tấn công, Marvin chọn ngẫu nhiên

$$
r\in\mathbb{Z}_N^*,
$$

tính

$$
C'=rC\bmod N,
$$

rồi gửi $C'$ cho máy của Bob. Một ứng dụng chạy trên máy Bob nhận $C'$ và cố gắng giải mã. Nó hoặc trả về thông báo lỗi, hoặc không phản hồi gì cả nếu tình cờ $C'$ có định dạng hợp lệ. Vì vậy, Marvin biết liệu 16 bit có trọng số cao nhất của kết quả giải mã $C'$ có bằng `02` hay không. Về thực chất, Marvin có một oracle cho phép hắn kiểm tra xem 16 bit có trọng số cao nhất của kết quả giải mã

$$
rC\bmod N
$$

có bằng `02` hay không đối với bất kỳ $r$ nào hắn lựa chọn. Bleichenbacher chỉ ra rằng một oracle như vậy là đủ để giải mã $C$.

## 6. Kết luận

Hai thập kỷ nghiên cứu về việc đảo ngược hàm RSA đã tạo ra một số cuộc tấn công sâu sắc, nhưng chưa từng tìm thấy cuộc tấn công mang tính hủy diệt nào. Những cuộc tấn công được phát hiện cho đến nay chủ yếu minh họa các cạm bẫy cần tránh khi triển khai RSA. Ở thời điểm hiện tại, có vẻ như các triển khai đúng cách có thể được tin cậy để cung cấp an toàn trong thế giới số.

Chúng tôi phân loại các cuộc tấn công vào RSA thành bốn nhóm: (1) các cuộc tấn công sơ cấp khai thác việc sử dụng hệ thống sai một cách rõ ràng; (2) các cuộc tấn công số mũ bí mật nhỏ, nghiêm trọng đến mức không bao giờ nên dùng một số mũ bí mật nhỏ; (3) các cuộc tấn công số mũ công khai nhỏ; và (4) các cuộc tấn công vào triển khai. Nhóm cuối cùng cho thấy chỉ nghiên cứu cấu trúc toán học nền tảng là chưa đủ. Desmedt và Odlyzko [10], Joye và Quisquater [15], cùng de Jonge và Chaum [9] mô tả thêm một số cuộc tấn công khác. Trong toàn bộ bài viết, chúng ta đã thấy rằng nhiều cuộc tấn công có thể bị ngăn chặn bằng cách đệm thông điệp đúng cách trước khi mã hóa hoặc ký.

## Lời cảm ơn

Tôi cảm ơn Susan Landau vì đã khuyến khích tôi viết bài khảo sát này và Tony Knapp vì đã giúp biên tập bản thảo. Tôi cũng biết ơn Mihir Bellare, Igor Shparlinski và R. Venkatesan vì những nhận xét về một bản nháp trước đó.

## Tài liệu tham khảo

[1] M. Bellare và P. Rogaway. *Mã hóa bất đối xứng tối ưu*. Trong EUROCRYPT '94, tập 950 của *Lecture Notes in Computer Science*, trang 92-111. Springer-Verlag, 1994.

[2] D. Bleichenbacher. *Các cuộc tấn công bản mã được chọn chống lại các giao thức dựa trên tiêu chuẩn mã hóa RSA PKCS #1*. Trong CRYPTO '98, tập 1462 của *Lecture Notes in Computer Science*, trang 1-12. Springer-Verlag, 1998.

[3] D. Boneh, R. DeMillo và R. Lipton. *Về tầm quan trọng của việc kiểm tra lỗi trong các giao thức mật mã*. Trong EUROCRYPT '97, tập 1233 của *Lecture Notes in Computer Science*, trang 37-51. Springer-Verlag, 1997.

[4] D. Boneh và G. Durfee. *Các kết quả mới về phân tích mật mã RSA với số mũ bí mật nhỏ*. Bản tiền công bố, 1998.

[5] D. Boneh, G. Durfee và Y. Frankel. *Một cuộc tấn công vào RSA khi biết một phần các bit của khóa riêng*. Trong AsiaCrypt '98, tập 1514 của *Lecture Notes in Computer Science*, trang 25-34. Springer-Verlag, 1998.

[6] D. Boneh và R. Venkatesan. *Phá RSA có thể không tương đương với phân tích thừa số*. Trong EUROCRYPT '98, tập 1403 của *Lecture Notes in Computer Science*, trang 59-71. Springer-Verlag, 1998.

[7] D. Coppersmith. *Các nghiệm nhỏ của phương trình đa thức và các điểm yếu của RSA với số mũ nhỏ*. *Journal of Cryptology*, 10:233-260, 1997.

[8] D. Coppersmith, M. Franklin, J. Patarin và M. Reiter. *RSA số mũ nhỏ với các thông điệp liên quan*. Trong EUROCRYPT '96, tập 1070 của *Lecture Notes in Computer Science*, trang 1-9. Springer-Verlag, 1996.

[9] W. de Jonge và D. Chaum. *Các cuộc tấn công vào một số chữ ký RSA*. Trong Crypto '85, tập 218 của *Lecture Notes in Computer Science*, trang 18-27. Springer-Verlag, 1986.

[10] Y. Desmedt và A. Odlyzko. *Một cuộc tấn công văn bản được chọn vào hệ mật mã RSA và một số lược đồ logarit rời rạc*. Trong CRYPTO '85, *Lecture Notes in Computer Science*, trang 516-522. Springer-Verlag, 1985.

[11] S. Goldwasser. *Tìm kiếm các hệ mật mã có thể chứng minh là an toàn*. Trong *Cryptology and computational number theory*, tập 42 của *Proceedings of the 42nd Symposium in Applied Mathematics*. American Mathematical Society, 1990.

[12] G. H. Hardy và E. M. Wright. *Nhập môn Lý thuyết số*. Oxford Clarendon Press, 1975. Ấn bản thứ tư.

[13] J. Hastad. *Giải đồng thời các phương trình mô-đun bậc thấp*. *SIAM Journal of Computing*, 17:336-341, 1988.

[14] N. Howgrave-Graham. *Xét lại bài toán tìm các nghiệm nhỏ của phương trình mô-đun một biến*. Trong *Cryptography and Coding*, tập 1355 của *Lecture Notes in Computer Science*, trang 131-142. Springer-Verlag, 1997.

[15] M. Joye và J.-J. Quisquater. *Về tầm quan trọng của việc bảo vệ thùng rác của bạn: cuộc tấn công người thu gom rác xen giữa*. Trong *4th ACM Conference on Computer and Communications Security*, trang 135-141. ACM Press, 1997.

[16] P. Kocher. *Các cuộc tấn công thời gian lên triển khai Diffie-Hellman, RSA, DSS và các hệ thống khác*. Trong CRYPTO '96, tập 1109 của *Lecture Notes in Computer Science*, trang 104-113. Springer-Verlag, 1996.

[17] L. Lovász. *Một lý thuyết thuật toán về số, đồ thị và tính lồi*. SIAM Publications, 1986.

[18] A. K. Lenstra và H. W. Lenstra, Jr. *Các thuật toán trong lý thuyết số*. Trong *Handbook of Theoretical Computer Science (Volume A: Algorithms and Complexity)*, chương 12, trang 673-715. Elsevier và MIT Press, 1990.

[19] A. Menezes, P. van Oorschot và S. Vanstone. *Sổ tay Mật mã học Ứng dụng*. CRC, 1996.

[20] C. Pomerance. *Câu chuyện về hai thuật toán sàng*. *Notices of the American Mathematical Society*, 43:1473-1485, 1996.

[21] R. L. Rivest, A. Shamir và L. Adleman. *Một phương pháp để tạo chữ ký số và các hệ mật mã khóa công khai*. *Communications of the ACM*, 21:120-126, 1978.

[22] M. Wiener. *Phân tích mật mã các số mũ bí mật RSA ngắn*. *IEEE Transactions on Information Theory*, 36:553-558, 1990.

---

[^1]: Mô tả của chúng tôi đơn giản hóa đôi chút phép mã hóa RSA. Trong thực tế, thông điệp được đệm bằng một lượng ngẫu nhiên trước khi mã hóa [1]. Chẳng hạn, một thuật toán đệm đơn giản nhưng chưa đủ an toàn có thể đệm bản rõ $M$ bằng cách nối thêm một vài bit ngẫu nhiên vào một trong hai đầu trước khi mã hóa. Việc bổ sung tính ngẫu nhiên vào quá trình mã hóa là cần thiết để đạt được an toàn đúng nghĩa.

[^2]: Một nguồn giải thích về an toàn ngữ nghĩa và đưa ra các ví dụ về những hệ mã an toàn ngữ nghĩa là [11].

[^3]: Trong ngữ cảnh này, “cuộc tấn công bản mã được chọn” chỉ một kẻ tấn công Marvin được cung cấp khóa công khai $\langle N,e\rangle$ và quyền truy cập vào một hộp đen có thể giải mã các thông điệp do hắn lựa chọn. Marvin thành công trong việc thực hiện cuộc tấn công bản mã được chọn nếu bằng cách sử dụng hộp đen, hắn có thể khôi phục khóa riêng $\langle N,d\rangle$.

[^4]: Mặc dù $\mathbb{Z}_N[x]$ không phải là một vành Euclid, thuật toán Euclid tiêu chuẩn vẫn có thể được áp dụng cho các đa thức trong $\mathbb{Z}_N[x]$. Có thể chứng minh rằng nếu thuật toán “hỏng” theo bất kỳ cách nào thì phân tích thừa số của $N$ sẽ bị lộ.
