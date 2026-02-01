#!/usr/bin/env python

import secrets
import argparse


""" 
Miller-Rabin Test

Where 'n' is a candidate prime number and k is the number of bases to try (default to 40 where probability of a false prime is 2^-80):

    1) Find n-1 = (2^s)(d)
    2) Choose a random 'a' such that 1<a<n-1
    3) Compute b_0 = a^d (mod n), ..., b_i = (b_i-1)^2 (mod n)
        if b_i = 1  -> Composite        : Return False
        if b_i = -1 -> (probably) Prime : Return True
    4) Repeat steps 2 and 3 'k' times
"""
def miller_rabin(n, k=40):
    if n < 2 or n % 2 == 0:
        return False

    if n in (2,3):
        return True

    # Step 1
    # We set d to n - 1 as d = (n-1)/(2^s). Then keep dividing n-1 by 2^s, incrementing s until d is no longer divisible by 2
    d = n - 1
    s = 0

    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        # Step 2
        # Choose a random base, 'a' to test with
        a = secrets.randbelow(n - 3) + 2  # Ensures 2 <= a <= n-2

        # Compute b_0 = a^d (mod n)
        b = pow(a, d, n)

        # Step 3
        # If b_0 is 1 or n - 1, pass, n could be prime
        if b == 1 or b == n - 1:
            continue

        # If not, calculate b_1 to b_i, where i = s-1.
        # If we find n - 1, pass, this number could be prime
        # If we find b_i == 1 before b_i-1 == n - 1, or never find a b_i == n - 1, this number is composite
        for _ in range(s - 1):
            b = pow(b, 2, n)

            if b == n - 1:
                break

        else:
            return False

    return True


"""
Returns a randomly genereated odd number with 'len' bits
"""
def random_odd(len):
    n = secrets.randbits(len)
    n |= (1 << len - 1) # Force top bit to ensure a 'len' bit number
    n |= 1 # Force last bit to make number odd
    return n


"""
Generate a random prime number with 'len' bits
"""
def generate_prime(len, k=40):
    while True:
        candidate = random_odd(len)
        if miller_rabin(candidate):
            return candidate


def main():
    parser = argparse.ArgumentParser(prog='Miller-Rabin Test', description='Generate a random prime number with the Miller-Rabin Primality Test')

    parser.add_argument('-l', '--length', type=int, default=512, help='Length of the prime number to be generated. Default=512')
    parser.add_argument('-k', '--num-tries', type=int, default=40, help='Number of bases to check against the candidate before determining primality. Default=40')

    args = parser.parse_args()

    prime = generate_prime(args.length, args.num_tries)
    confidence = 100*(1 - .25**args.num_tries)

    print(f'Prime: {prime}')
    print(f'with confidence: {confidence}%')


if __name__ == '__main__':
    main()

