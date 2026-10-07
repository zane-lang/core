#!/usr/bin/env python3
"""Reproducible build/runtime comparison; constant fib(42), no memoization."""
import os
import platform
import statistics
import subprocess
import time
from pathlib import Path

root = Path(__file__).resolve().parents[2]
out = root / "out" / "fib-bench-inspection"
out.mkdir(parents=True, exist_ok=True)
binaries = {
    "Zane": out / "fib-zane",
    "C++": out / "fib-cpp",
    "Go": out / "fib-go",
}
builds = {
    "Zane": ["zane", "build", "fib", "-o", str(binaries["Zane"])],
    "C++": ["g++", "-O3", "-std=c++20", "-DNDEBUG", str(root / "bench/fibonacci/fib.cpp"), "-o", str(binaries["C++"])],
    "Go": ["go", "build", "-trimpath", "-o", str(binaries["Go"]), str(root / "bench/fibonacci/fib.go")],
}
expected = "267914296"
print("Host:", platform.platform(), flush=True)
print("Architecture:", platform.machine(), flush=True)
print("CPU:", next((line.split(":", 1)[1].strip() for line in Path("/proc/cpuinfo").read_text().splitlines() if line.startswith("model name")), "unknown"), flush=True)
for command in [["zane", "--version"], ["g++", "--version"], ["go", "version"]]:
    p = subprocess.run(command, capture_output=True, text=True)
    print(command[0] + ":", p.stdout.strip().splitlines()[0] if p.returncode == 0 else p.stderr.strip(), flush=True)

for language, command in builds.items():
    print("BUILD", language, " ".join(command), flush=True)
    start = time.perf_counter()
    result = subprocess.run(command, cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=720)
    elapsed = time.perf_counter() - start
    print("BUILD_LOG", language, result.stdout[-5000:], flush=True)
    print(f"METRIC|{language}|compile_seconds|{elapsed:.6f}|exit={result.returncode}", flush=True)
    if result.returncode:
        raise SystemExit(f"{language} compilation failed")
    p = subprocess.run([str(binaries[language])], capture_output=True, text=True, timeout=60)
    print("CHECK", language, repr(p.stdout.strip()), "exit", p.returncode, flush=True)
    if p.returncode != 0 or p.stdout.strip() != expected:
        raise SystemExit(f"{language} output unexpected (wanted {expected!r})")

# Round-robin measurements to avoid first-run ordering effects.
samples = {lang: [] for lang in binaries}
for rep in range(5):
    for language, executable in binaries.items():
        start = time.perf_counter_ns()
        p = subprocess.run([str(executable)], capture_output=True, timeout=60)
        elapsed = (time.perf_counter_ns() - start) / 1e6
        if p.returncode or p.stdout.strip() != expected.encode():
            raise SystemExit(f"Bad output in repetition {rep} for {language}")
        samples[language].append(elapsed)
for language, durations in samples.items():
    print(f"METRIC|{language}|run_median_ms|{statistics.median(durations):.6f}|runs={len(durations)}", flush=True)
    print(f"METRIC|{language}|run_min_ms|{min(durations):.6f}|runs={len(durations)}", flush=True)
    print(f"METRIC|{language}|run_max_ms|{max(durations):.6f}|runs={len(durations)}", flush=True)
# Store binaries and disassemblies for independent verification of compile-time folding.
for language, executable in binaries.items():
    key = language.lower().replace("+", "p").replace(" ", "-")
    for suffix, command in [
        ("symbols.txt", ["nm", "-C", str(executable)]),
        ("disassembly.txt", ["objdump", "-d", "-C", "-M", "intel", str(executable)]),
    ]:
        result = subprocess.run(command, capture_output=True, text=True, timeout=60)
        output_file = out / f"{key}.{suffix}"
        output_file.write_text(result.stdout if result.returncode == 0 else result.stderr)
        print(f"INSPECT|{language}|{suffix}|{output_file}|bytes={output_file.stat().st_size}", flush=True)
    symbols = (out / f"{key}.symbols.txt").read_text().splitlines()
    fib_symbols = [line for line in symbols if "fib" in line.lower() and "fib-bench" not in line]
    print(f"FIB_SYMBOLS|{language}|{fib_symbols[:16]}", flush=True)
    if language == "C++":
        asm = (out / f"{key}.disassembly.txt").read_text()
        import re
        m = re.search(r"^[0-9a-f]+ <main>:\\n(.*?)(?=^\\S.*? <[^>]+>:\\n|\\Z)", asm, re.M | re.S)
        print("MAIN_ASM_CPP_BEGIN", flush=True)
        print((m.group(0) if m else "could not locate main")[:8000], flush=True)
        print("MAIN_ASM_CPP_END", flush=True)
    if language == "Go":
        go = subprocess.run(["go", "tool", "objdump", "-s", r"^main\\.(main|fib)$", str(executable)], capture_output=True, text=True, timeout=60)
        (out / "go.entry-disassembly.txt").write_text(go.stdout)
        print("GO_ENTRY_ASM", go.stdout[:6500], flush=True)
print("Note: wall-clock runtime includes process startup and stdout; compile time includes CLI/build startup.", flush=True)
