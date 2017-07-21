#coding=utf-8

def splitList(ls, n):
    if not isinstance(ls, list) or not isinstance(n, int):
        return []
    ls_len = len(ls)
    if n <= 0 or 0 == ls_len:
        return []
    if n > ls_len:
        return splitList(ls,ls_len)
    elif n == ls_len:
        return [[i] for i in ls]
    else:
        j = ls_len / n
        k = ls_len % n
        ls_return = []
        for i in xrange(0, (n - 1) * j, j):
            ls_return.append(ls[i:i + j])
        ls_return.append(ls[(n - 1) * j:])
        return ls_return