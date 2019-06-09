def binary(s):
    return str(s) if s<=1 else bin(s>>1) + str(s&1)