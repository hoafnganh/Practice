# Diagnostic only: byte-exact scan of rockyou for the Hamac HMAC target.
# Reports whether the password is present, plus the line numbers that break a
# naive open("r")/readline/strip() scan.
import hmac, hashlib

PATH = r"E:\Jeopardy\Practice\Hackropole\Hamac\rockyou.txt"
TARGET = "951bd9d2caae0d9e9a5665b4fc112809aac9f5f9ecbcfc5ad8e23cb1d020201d"

found_line = found_ascii = found_len = None
first_blank = None
utf8_fail_line = None

with open(PATH, "rb") as f:
    raw = f.read()
lines = raw.split(b"\n")
del raw

for i, line in enumerate(lines, 1):
    p = line.rstrip(b"\r")
    if p == b"" and first_blank is None:
        first_blank = i
    if utf8_fail_line is None:
        try:
            line.decode("utf-8")
        except UnicodeDecodeError:
            utf8_fail_line = i
    if found_line is None and hmac.new(p, b"FCSC2022", hashlib.sha256).hexdigest() == TARGET:
        found_line, found_ascii, found_len = i, p.isascii(), len(p)

print("total lines:", len(lines))
print("FOUND at line:", found_line, "| ascii:", found_ascii, "| len:", found_len)
print("first blank line:", first_blank)
print("first non-utf8 line:", utf8_fail_line)
