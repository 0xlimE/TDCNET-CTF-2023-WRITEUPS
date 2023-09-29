`Crypto`
This challenge is inspired by an LLL challenge on Cryptohack. 
I ran this command:
```
llc -filetype=obj source.ll -o hello-world.o -opaque-pointers
```
And opened the `.o` file in Binary Ninja, and began reversing. I managed after some manual patching to get `llvm2c` (https://github.com/staticafi/llvm2c). This gave me really poor results though, because I had to remove a bunch of instructions that it weren't happy with. After a bunch of playing around, I got ChatGPT to give me some python code that resembled source a lot, and I think I got survivor bias and was like "Sure, this is solvable!" - It's essentially a Knapsack Cryptosystem (I thought you might be able to tell this by the LLL part and the fact that the numbers are so large in the output, and had someone solve it from a korean team as a test run). 

My solve script looks like this: 
```python
# doit.sage
from Crypto.Util.number import long_to_bytes
from math import log2

with open("output.txt") as f:
    data = f.read().split("\n")

p = eval(data[0])
enc = eval(data[1])

"""
pt = plaintext
pk = public key
enc = pt_0 * pk_0 + pt_1 * pk_1 + pt_2 * pk_2 + ... pt_n * pk_n

Attack implemented: https://eprint.iacr.org/2009/537.pdf
(Low Density Attack)
"""

n = len(p)
d = n/(log2(max(p)))
print(f"{d = }")

N = ceil(sqrt(n) / 2)

b = []
for i in range(n):
    vec = [0 for _ in range(n+1)]
    vec[i] = 1
    vec[-1] = N * p[i]
    b.append(vec)

b.append([1 / 2 for _ in range(n)] + [N * enc])

BB = matrix(QQ, b)
l_sol = BB.LLL()

for e in l_sol:
    if e[-1] == 0:
        msg = []
        isValidMsg = True
        for i in range(len(e) - 1):
            ei = 1 - (e[i] + (1 / 2))
            if ei != 1 and ei != 0:
                isValidMsg = False
                break

            msg.append(ei)

        if isValidMsg:
            msg = msg[::-1]
            print(long_to_bytes(int(str(msg)[1:-1].replace(", ", ""), 2)))
            break
```

Flag:
`TDCNET{LlL_t0_s0lv3_kn4ps4ck_crypt0syst3m}`
