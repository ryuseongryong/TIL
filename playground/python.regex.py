import re

ip = "127.0.0.1:6443 127.0.0.1:6444"
pattern = "127.0.0.1:6443"

result = re.findall(pattern, ip)
print(result)
