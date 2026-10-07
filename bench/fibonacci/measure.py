#!/usr/bin/env python3
"""Reproducible build/runtime comparison; constant fib(35), no memoization."""
import os
import platform
import statistics
import subprocess
import tempfile
import time
from pathlib import Path

root = Path(__file__).resolve().parents[2]
out = Path(tempfile.mkdtemp(prefix="fib-bench-"))
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
expected = "9227465"
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
for rep in range(20):
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
print("Note: wall-clock runtime includes process startup and stdout; compile time includes CLI/build startup.", flush=True)
