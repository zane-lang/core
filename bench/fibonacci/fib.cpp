#include <cstdint>
#include <iostream>

// constexpr permits (but does not require) compile-time evaluation.
constexpr std::int64_t fib(std::int64_t n) {
    if (n < 2) return n;
    return fib(n - 1) + fib(n - 2);
}

int main() {
    std::cout << fib(35) << '\n';
}
