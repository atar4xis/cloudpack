#!/usr/bin/env python3

import argparse
from pathlib import Path

import cloudpack.vault as vault


def main():
    # === command parser ===
    commands = [
        {
            "name": "init",
            "help": "initialize a new vault",
            "func": vault.init,
            "args": [
                {
                    "name": "path",
                    "kwargs": {
                        "nargs": "?",
                        "type": Path,
                        "help": "optional path to the vault directory",
                        "default": ".",
                    },
                }
            ],
        },
        {
            "name": "config",
            "help": "configure the vault",
            "func": vault.configure,
            "args": [],
        },
        {
            "name": "add",
            "help": "add a file to the vault",
            "func": vault.add,
            "args": [
                {"name": "file", "kwargs": {"help": "path to the file to add"}},
            ],
        },
        {
            "name": "unlock",
            "help": "unlock the vault using the master password",
            "func": vault.unlock,
            "args": [
                {
                    "name": "path",
                    "kwargs": {
                        "nargs": "?",
                        "type": Path,
                        "help": "optional path to the vault directory",
                        "default": ".",
                    },
                }
            ],
        },
        {
            "name": "upload",
            "help": "upload the vault to the cloud",
            "func": vault.upload,
            "args": [],
        },
    ]

    # define --path so it works globally (before or after subcommands)
    # e.g. `cloudpack init --path myVault` and `cloudpack --path myVault init`
    path_arg = {
        "flags": ("-p", "--path"),
        "kwargs": {
            "type": Path,
            "default": ".",
            "help": "path to the vault directory",
        },
    }

    parser = argparse.ArgumentParser(prog="cloudpack")
    parent_parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(*path_arg["flags"], **path_arg["kwargs"])
    parent_parser.add_argument(*path_arg["flags"], **path_arg["kwargs"])
    subparsers = parser.add_subparsers(title="commands", dest="command")

    for cmd in commands:
        sp = subparsers.add_parser(
            cmd["name"], parents=[parent_parser], help=cmd["help"]
        )
        for arg in cmd["args"]:
            sp.add_argument(arg["name"], **arg.get("kwargs", {}))
        sp.set_defaults(func=cmd["func"])

    # === command handler ===
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
