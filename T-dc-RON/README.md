`Rev`
This is the source code which is the exact same in Binary Ninja except this has symbols.
```
        ; Decrypt the flag using and xor mod flag len
        mov si, flag_contents
        mov di, [points]
        and di, 15
        add si, di
        mov byte ch, [si]
        mov byte dh, [pellet_x]
        xor ch, dh
        mov byte [si], ch

        ; Increment the points
        inc byte [points]
```
After some reversing you should see that the flag is decrypted using the pellet's X-coordinate. However, how are the pellets generated?
```
    get_pellet:
        inc byte [pellets]

        call random
        mov cx, [rand_value]
        and cx, 255
        mov word [pellet_x], cx

        call random
        mov dx, [rand_value]
        and dx, 63
        mov word [pellet_y], dx

        mov al, 0x05

        mov ah, 0x0C
        mov bh, 0x00	    

        int 0x10	            

        ret
```
This calls random:
```
    random:
        mov ax, 75
        mov bx, [rand_value]

        mul bx

        add ax, 74
        and ax, 0xffff
        inc ax

        mov [rand_value], ax

        ret
```
We can make a python script to recover the flag based on this deterministic RNG:
```python
r = 1

def rng():
    global r
    r = r * 0x4b + 0x4b
    return r

flag = bytearray(b"TDCNET{" +
    bytes([
        48, 4, 132, 153, 159, 113, 117, 31, 51, 112, 240, 31, 38, 149, 142, 225,
    ]) + b"}")

at = 0
next = 1
while True:
    if at == 0x1a4:
        break
    if at != next:
        at += 1
        x = rng() & 0xff
        y = rng() & 0x3f
    else:
        flag[7 + (next & 0xf)] ^= x
        next += 1

print(flag)
```

Flag:
`TDCNET{pRnG_15_s00_fUN!}`
