import argparse
import sys
from pathlib import Path

from .store import TaskStore

DEFAULT_FILE = Path.home() / ".tasky.json"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="tasky", description="A tiny task tracker.")
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE, help="task file (default: ~/.tasky.json)")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="show tasks")
    p = sub.add_parser("add", help="add a task")
    p.add_argument("title", nargs="+")
    for name in ("done", "rm"):
        p = sub.add_parser(name, help=f"{'complete' if name == 'done' else 'remove'} a task")
        p.add_argument("id", type=int)
    args = parser.parse_args(argv)

    store = TaskStore(args.file)
    try:
        if args.cmd == "list":
            if not store.tasks:
                print("No tasks.")
            for t in store.tasks:
                print(f"[{'x' if t.done else ' '}] {t.id}: {t.title}")
            return 0
        if args.cmd == "add":
            t = store.add(" ".join(args.title))
            print(f"Added {t.id}: {t.title}")
        elif args.cmd == "done":
            t = store.complete(args.id)
            print(f"Completed {t.id}: {t.title}")
        elif args.cmd == "rm":
            t = store.remove(args.id)
            print(f"Removed {t.id}: {t.title}")
    except KeyError as e:
        print(f"error: {e.args[0]}", file=sys.stderr)
        return 1
    store.save()
    return 0


if __name__ == "__main__":
    sys.exit(main())
