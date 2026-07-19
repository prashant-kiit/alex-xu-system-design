# https://github.com/ArjanCodes/examples/blob/main/2024/func/6_composition.py

from functools import partial, reduce
from typing import Callable

def multiply_by_n(data: list[int], n: int) -> list[int]:
    for m in data:
        yield m * n

def add_n(data: list[int], n: int) -> list[int]:
    for m in data:
        yield m + n

type Composable[T] = Callable[[T], T]

def compose[T](*converters: Composable[T]) -> Composable[T]:
    def apply(value, fn) -> T:
        return fn(value)
    return lambda data: reduce(apply, converters, data)


def main() -> None:
    data = [1, 5, 3, 4, 2]
    print(f"Data before sorting: {data}")

    multiply_by_2 = partial[list[int]](multiply_by_n, n=2)
    add_10 = partial[list[int]](add_n, n=10)

    do_operations = compose(multiply_by_2, add_10)

    result_gen = do_operations(data)
    for value in result_gen:
        print(value)

    # result_gen = multiply_by_2(add_10(data))
    # print(next(result_gen))
    # print(next(result_gen))
    # print(next(result_gen))
    # for value in result_gen:
    #     print(value)
    # # output: 22 30 26 28 24 

if __name__ == "__main__":
    main()