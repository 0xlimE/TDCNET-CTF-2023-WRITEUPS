
# r0ll
`Crypto`
I made a `custom` commitment scheme for this challenge. It's based on Pedersen commitment. I tried hinting this very subtly in the description `Hans Peter`. A commitment scheme is a cryptographic primitive that allows one to commit to a chosen value (or chosen statement) while keeping it hidden to others, with the ability to reveal the committed value later. (Wikipedia). This can be very useful for online casinos for example, such that customers know that they're not getting tricked. The specifically suspicious thing about this code should be the `verify()` function:
```python
def verify(param, c, r, x):
    q, g, h = param
    return pow(c, (q-1)//2, q) == pow((pow(g,x,q) * pow(h,r,q) % q), (q-1)//2, q)
```
We're using Legendres Symbol to check if both of the parameters are quadratic residues. We take a quick look at the numbers being given to `verify`:
```python
if verify(keygen, c, r, secret_roll) == verify(keygen, c, r, your_roll):
```
We see that the first part is:
```python
pow(c, (q-1)//2, q)
```
And we already know `c`. This is generated as such:
```python
c,r = commit(keygen, secret_roll)
print(f"Here's my commitment, so you'll trust me!")
print(f"{c = }")
```
We have 6 possible options here for the commit:
```
commit(keygen, 1)
commit(keygen, 2)
commit(keygen, 3)
...
commit(keygen, 6)
```
Let's go back to the following code:
```python
pow(c, (q-1)//2, q)
```
A fun fact is that whenever `c` is a quadratic residue the result of the above calculation will also always yield a quadratic residue. This means that we can do some really sneaky stuff. What if ALL the rolls are quadratic residues? That means that whenever you guess the verify will always pass. My solve script looks something like this:
```python
while True:
    q, g, h = get_q(), get_g(), get_h()
    param = q,g,h

    commit_r = get_com()
    commit_qr = pow(commit_r, (q-1)//2, q)

    A = pow(commit(param, 1)[0], (q-1)//2, q)
    B = pow(commit(param, 2)[0], (q-1)//2, q)
    C = pow(commit(param, 3)[0], (q-1)//2, q)
    D = pow(commit(param, 4)[0], (q-1)//2, q)
    E = pow(commit(param, 5)[0], (q-1)//2, q)
    F = pow(commit(param, 6)[0], (q-1)//2, q)

    if A != 1 or B != 1 or C != 1 or D != 1 or E != 1 or F != 1:
        io.sendline(b"G")
        continue

    if commit_qr == 1:
        io.sendline(b"Y")
    else:
        io.sendline(b"G")

io.interactive()
```

And then there's a flag:
`TDCNET{th3y_s33_me_r0ll1n_th3Y_h4t!nG}`
