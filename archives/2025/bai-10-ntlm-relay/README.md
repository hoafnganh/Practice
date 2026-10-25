# bai-10-ntlm-relay

**Thể loại:** forensics / network

## Đề bài

Nghi ngờ một cuộc tấn công "giặc nhà quê" (inside job) trên máy `192.168.56.104`; thông tin xác thực có thể đã bị rò rỉ từ máy `192.168.56.33`. Phân tích PCAP, nhận diện kiểu tấn công, khôi phục thông tin xác thực bị lộ và ghép flag.

Định dạng flag:
`XHM{<user>::<domain>:<16 hex>:<32 hex>:<620 hex>}`

## Lời giải

File bắt gói chứa lưu lượng NBNS/NetBIOS theo sau là SMB với NTLMSSP — chữ ký kinh điển của một vụ **bắt thông tin xác thực NTLMv2** (LLMNR/NBT-NS poisoning / SMB relay). Định dạng flag khớp chính xác với các trường của một phiên xác thực NTLMv2:

- `server challenge` — từ thông điệp NTLMSSP **Type 2** (CHALLENGE)
- `NT proof` + `blob` — từ thông điệp NTLMSSP **Type 3** (AUTHENTICATE) (`NTProofStr` là 16 byte đầu của NTLMv2 response, phần còn lại là blob)

Trích các trường bằng `tshark`:

```bash
# Server challenge (Type 2)
tshark -r capture.pcap -Y "ntlmssp.ntlmserverchallenge" \
       -T fields -e ntlmssp.ntlmserverchallenge | head -n1
# -> 46f422cd882b169d

# User, domain, NTLMv2 response (Type 3)
tshark -r capture.pcap \
       -Y "ntlmssp.auth.username && ntlmssp.auth.ntresponse" \
       -T fields -e ntlmssp.auth.username -e ntlmssp.auth.domain \
       -e ntlmssp.auth.ntresponse
# -> bob   WINDOMAIN   4837e8d2...
```

Sau đó tách NTLMv2 response: `ntresponse[0:32]` là NT proof (32 hex), `ntresponse[32:]` là blob (620 hex). `analyze_pcap.py` tự động hóa toàn bộ quá trình trích xuất và in ra cả flag lẫn dòng hashcat `-m 5600`.

Các giá trị thu được:

- **User / domain:** `bob` / `WINDOMAIN`
- **Server challenge:** `46f422cd882b169d`
- **NT proof:** `4837e8d20080f19cc2762798c9373a8e`
- **Blob:** `0101000000000000934f159ee807dc01...0000000000` (620 hex)

## Flag

```
XHM{bob::WINDOMAIN:46f422cd882b169d:4837e8d20080f19cc2762798c9373a8e:0101000000000000934f159ee807dc01c70a33e89710d3140000000002001200570049004e0044004f004d00410049004e0001000e00570049004e00310030002d00320004001e00770069006e0064006f006d00610069006e002e006c006f00630061006c0003002e00770069006e00310030002d0032002e00770069006e0064006f006d00610069006e002e006c006f00630061006c0005001e00770069006e0064006f006d00610069006e002e006c006f00630061006c0007000800934f159ee807dc0106000400020000000800300030000000000000000000000000200000d680c970ffd7be19f29a3b7d61c7d3353ee63fdfa4fd83344a83f7681a6b65980a001000000000000000000000000000000000000900140063006900660073002f00640063006300300032000000000000000000}
```

Kẻ phản bội: `WINDOMAIN\bob`, thông tin xác thực NTLMv2 bị bắt qua NBNS/SMB.
