# Redis from Scratch — Python

I'm building Redis to deepen my understanding of computer science fundamentals and become better at building systems. This Python implementation focuses on TCP connections, protocol framing, and concurrency.

Based on the CodeCrafters Redis challenge. Each exercise has its own commit.

Run with `./your_program.sh` (Python 3.14 and uv), or `python3 -m app.main`.

The preserved C implementation is on the [master branch](https://github.com/Saitejar0203/redis-from-scratch/tree/master). Python development lives on the `python` branch.

## Current progress

Implemented through **ECHO**, including binary-safe bulk-string responses. The next exercise is **SET & GET**.

`app/main.py` contains the server. Each client gets a worker thread and a buffered reader; complete RESP commands are consumed individually even when TCP splits or combines their bytes. Responses use `sendall`. Command dispatch supports PING and ECHO, with errors for unknown commands or invalid ECHO arguments. Threads are daemon threads, so stopping the process stops them as well.

Run the socket integration checks with `python3 -m unittest discover -s tests -v`. They cover repeated and combined commands, fragmented input, idle concurrent clients, half-close, and malformed input isolation.

## Submit an exercise

```sh
codecrafters submit -m "Describe the completed exercise"
git push github HEAD:python
```

The local `master` branch submits to CodeCrafters; GitHub's `python` branch contains the same commits. The C checkout is separate and unchanged.
