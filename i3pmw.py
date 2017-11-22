#!/usr/bin/env python3

import sys

import click
import i3ipc

i3 = i3ipc.Connection()

monmap = {
    'DP-0': '3',
    'DP-2': '1',
    'DP-4': '2',
}

@click.group()
def cli():
    pass

@click.command()
@click.argument('workspace')
def switch(workspace):
    """
    Switch it to the base workspace passed in, creating workspaces as needed
    """

    # get current workspace
    cur_workspaces = i3.get_workspaces()
    cur_workspace = next(w for w in cur_workspaces if w['focused'])
    cwnsplit = cur_workspace['name'].rsplit('.')

    if len(cwnsplit) > 1:
        cur_workspace_subnum = cwnsplit[-1]
    else:
        # hardcode to dave's setup
        cur_workspace_subnum = monmap[cur_workspace['output']]

    # create new workspaces if we need to
    cur_workspace_names = [w['name'] for w in cur_workspaces]

    for output, subnum in monmap.items():
        new_ws = "{}.{}".format(workspace, subnum)

        print(new_ws)

        if new_ws not in cur_workspace_names:
            print(i3.command("focus output {}".format(output)))
            print(i3.command("workspace {}".format(new_ws)))

    # always switch to the subnum
    i3.command("workspace {}.{}".format(workspace, cur_workspace_subnum))

cli.add_command(switch)

if __name__ == "__main__":
    cli()
