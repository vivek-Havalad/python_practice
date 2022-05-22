import os, sys
import collections

def shifter(Q): 
    Q.append(Q.pop(0))
    return Q

def comparator(P, Q):
    compare_cnt = 0
    if len(P) >= len(Q):
        for c1 in P:
            for c2 in Q:
                if c1 != c2:
                    return  compare_cnt
                compare_cnt += 1
    else:
        for c1 in Q:
            for c2 in P:
                if c1 != c2:
                    return  compare_cnt
                compare_cnt += 1

def TheEngine(P, Q):
    compared_prefix = 0
    rotated = 0
    till_rotated = 0
    for x in range(len(Q)):
        compared_prefix_result = comparator(P, Q)
        if compared_prefix_result > compared_prefix:
            compared_prefix = compared_prefix_result
            till_rotated = rotated
        Q = shifter(Q)
        rotated += 1
    return till_rotated

if __name__ == "__main__":
    P = "ccadd"
    Q = "bddcc"
    print(TheEngine(list(P), list(Q)))