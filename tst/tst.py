from enum import Enum


class A(Enum):
    hicham = 1
    darwin = 2


for e in A:
    print(f"name: {A.hicham}")
    print(f"value: {e.value}")
