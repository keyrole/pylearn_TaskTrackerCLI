import json
import sys
from argparse import ArgumentParser
from datetime import datetime
from typing import Literal, Generator, Callable
from tabulate import tabulate

PATH = "./tasks3.json"
cmd = dict()

def get_quires():
    supported_command = {
        "add": {
            "target": add_task,
            "help": "Add a new task to your task list",
            "args": [
                {"name_or_flags": ["description"], "help": "Description of the task"}
            ],
        },
        "list": {
            "target": list_task,
            "help": "List all tasks or filter them by status",
            "args": [
                {
                    "name_or_flags": ["status"],
                    "help": "Filter tasks by status (default is 'all')",
                    "choices": ["all", "done", "new", "in-progress", "undone"],
                    "type": str.lower,
                    "default": "all",
                    "nargs": '?',
                }
            ]
        },
        "update": {
            "target": update_task,
            "help": "Update the status of a task",
            "args": [
                {
                    "name_or_flags": ["id"],
                    "help": "ID of the task to update",
                    "type": str,
                },
                {
                    "name_or_flags": ["status"],
                    "help": "Update the status to",
                    "choices": ["done", "new", "in-progress"],
                    "type": str.lower,
                }
            ]
        },
        "delete": {
            "target": delete_task,
            "help": "Delete a task",
            "args": [
                {
                    "name_or_flags": ["id"],
                    "help": "ID of the task to update",
                    "type": str,
                }
            ]
        }
    }

    return  supported_command

def delete_task(database, id):
    if id in database.keys():
        del database[id]

def update_task(database, id, status):
    if id in database.keys():
        database[id]['status'] = status

def save_database(database):
    with open(PATH, "w") as f:
        json.dump(database, f)

def load_database():
    try:
        with open(PATH, "r") as f:
            content = json.load(f)
    except FileNotFoundError:
        content = {}
    return content

def add_task(database, description):
    today = datetime.today().isoformat()
    id = str(int(max("0", *database.keys())) + 1)
    database[id] = {
        "description": description,
        "status": "new",
        "createdAt": today,
        "updatedAt": today,
    }

def list_task(database, status: Literal["all", "new", "in-progress", "done"] = "all"):
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    table: Generator = (
        {
            "id": id,
            "description": properties["description"],
            "status": properties["status"],
            "createdAt": properties["createdAt"],
            "updatedAt": properties["updatedAt"],
        }
        for id, properties in sorted(database.items(), key=lambda t: t[0])
    )
    print(
        tabulate(table, tablefmt="simple", headers="keys") or "Nothing to display"
    )

def main():
    myparser = ArgumentParser()
    subparser = myparser.add_subparsers(dest="command")
    supported_command = get_quires()
    for s_cmd, properties in supported_command.items():
        p = subparser.add_parser(s_cmd, help = properties['help'])
        for arg in properties['args']:
            p.add_argument(*arg.pop('name_or_flags'), **arg)
    args = myparser.parse_args().__dict__

    querie: Callable = supported_command[args.pop('command')]['target']

    database = load_database()
    try:
        querie(database, **args)
    except KeyError:
        sys.exit("No task found with the provided ID")
    if querie != list_task:
        list_task(database)
    save_database(database)

if __name__ == "__main__":
    main()