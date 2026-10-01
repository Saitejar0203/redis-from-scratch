# Redis from Scratch

I'm building Redis in C to deepen my understanding of computer science fundamentals and become better at building systems. This project explores networking, memory, data structures, and how a database works beneath its public interface.

Based on the [CodeCrafters Redis challenge](https://app.codecrafters.io/courses/redis/overview).

## Status

The first stage, Bind to a port, is implemented in `src/main.c`. It listens on TCP port 6379, accepts one connection, and exits. No Redis commands are implemented yet.

## Run locally

Requires a C compiler and CMake. On macOS, install the Xcode Command Line Tools. The starter has no external library dependencies.

```sh
./your_program.sh
```

The script builds into `build/` and runs the starter. It listens on port 6379, accepts one client connection, and exits without reading a command or sending a response.

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
