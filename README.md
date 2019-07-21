# Collatz "main term" conjecture

## background

The Collatz conjecture is that for any positive integer n, the following
statement holds: for the sequece {a_i} defined by a_0=n,
a_k=a_{k-1}/2 if a_{k-1} is even or a_k=3a_{k-1}+1 if a_{k-1} is odd,
there exists K where a_K=1.  The conjecture is still open.

Now, let's consider a modification.  We define a sequence for any
positive rational (or even irrational real) number x.  Let b_0=x,
and b_k=b_{k-1}/2 if ceil(b_{k-1}) is even or b_k=3b_{k-1}/2 if
ceil(b_{k-1}) is odd.  Then, we conjecture that there exists K where
b_K is in range (0, 1], and call it 'Collatz "main term" conjecture.'

## the program

collatz_interval.prove_conjecture function will run until the given
open-closed interval satisfies the condition of Collatz "main term"
conjecture.  If you give an interval containing a counterexample, it
will never stop!

We observed with the program that up to 200, the "main term"
conjecture holds.

The program is written with python 3, and requires intervals module.
(see Pipfile)

## license
You can use the program without any restrictions, but if you find
something interesting, please let me know.

