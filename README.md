# Redis from Scratch

I'm building Redis in C to deepen my understanding of computer science fundamentals and become better at building systems. This project explores networking, memory, data structures, and how a database works beneath its public interface.

Based on the [CodeCrafters Redis challenge](https://app.codecrafters.io/courses/redis/overview).

## Status

C starter configured. No exercises implemented yet; the first-stage code in `src/main.c` remains commented out.

## Run locally

Requires a C compiler and CMake. On macOS, install the Xcode Command Line Tools. The starter has no external library dependencies.

```sh
./your_program.sh
```

The script builds into `build/` and runs the starter, which currently prints a diagnostic message and exits. Once implemented, the server will listen on port 6379.

## Project layout

- `src/main.c`: starter and implementation entry point.
- `CMakeLists.txt`: C23 build configuration.
- `your_program.sh`: local build and launch script.
- `.codecrafters/`: hosted build and launch scripts.

## Exercise workflow

Keep one commit per exercise. When an exercise is ready:

```sh
codecrafters test
codecrafters submit -m "Implement <stage name>"
git push github master
```

`origin` is the CodeCrafters submission remote; `github` is the public repository. Setup changes are published to GitHub without submitting an exercise.
