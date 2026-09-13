# Why the arithmetic mean minimizes squared error

## Statement
For an integer n ≥ 1 and fixed real numbers x₁,…,xₙ, let
\(\bar x=n^{-1}\sum_i x_i\) and \(F(a)=n^{-1}\sum_i(x_i-a)^2\).
For every real a,
\[F(a)=F(\bar x)+(a-\bar x)^2.\]
Consequently, the unique global minimizer is a=\bar x.
This is an original exposition of a standard elementary result, not a claim of novelty.

## Accepted background and notation
Finite sums distribute over addition. A factor independent of the summation
index can be moved outside the sum. For real A,B, (A+B)²=A²+2AB+B².
A real square is nonnegative, with equality exactly when its base is zero.
No differentiation, probability, or asymptotic argument is required.

## P1. The signed deviations sum to zero
From the definition, n\bar x=Σᵢxᵢ. Therefore
Σᵢ(xᵢ−\bar x)=Σᵢxᵢ−Σᵢ\bar x=Σᵢxᵢ−n\bar x=0.
The middle equality uses that the same constant \bar x appears n times.

## P2. Expand each square
For each i, xᵢ−a=(xᵢ−\bar x)+(\bar x−a). Apply the square identity:
(xᵢ−a)²=(xᵢ−\bar x)²+2(xᵢ−\bar x)(\bar x−a)+(\bar x−a)².
This is an exact equality of real numbers for every a.

## P3. Sum and cancel the cross term
Multiply P2 by 1/n and sum over i. The cross term is
(2/n)(\bar x−a)Σᵢ(xᵢ−\bar x)=0 by P1.
The factor \bar x−a is independent of i; no statistical independence is involved.

## P4. Simplify the remaining terms
The first averaged sum is F(\bar x). The last is
(1/n)Σᵢ(\bar x−a)²=(1/n)n(\bar x−a)²=(a−\bar x)².
Division by n is legitimate because n≥1. This proves the displayed identity.

## P5. Conclude global optimality and uniqueness
For every real a, F(a)−F(\bar x)=(a−\bar x)²≥0, so the mean is a global
minimizer. Equality requires (a−\bar x)²=0, hence a=\bar x. There is no
second minimizer. The n=1 and all-equal-data cases satisfy the same argument.

## Worked example and computational check
For (1,3,5), \bar x=3 and F(3)=(4+0+4)/3=8/3. Thus
F(a)=8/3+(a−3)²=a²−6a+35/3. `simulation.py` verifies this identity on
fixed-seed examples including n=1. Numerical checks illustrate the algebra;
they do not prove the universal theorem.

## Review
The assumptions, factorization, division, equality case, and edge cases were
checked against P1–P5. No open mathematical issues were found. This is a
model-assisted review, not a machine-checked proof.
