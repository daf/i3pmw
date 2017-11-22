#!/usr/bin/env python3

import sys

import click
import i3ipc

i3 = i3ipc.Connection()

def _get_monitor_map():
    outputs = [o for o in i3.get_outputs() if o['active']]
    outputs.sort(key=lambda x: x['rect']['x'])

    monmap = {}
    for i, o in enumerate(outputs):
        monmap[o['name']] = str(i+1)

    return monmap

@click.group()
def cli():
    pass

def _make_workspaces(workspace):
    # get current workspace
    cur_workspaces = i3.get_workspaces()
    cur_workspace = next(w for w in cur_workspaces if w['focused'])
    cwnsplit = cur_workspace['name'].rsplit('.')

    monmap = _get_monitor_map()

    if len(cwnsplit) > 1:
        cur_workspace_subnum = cwnsplit[-1]
    else:
        # whatever's currently focused's output
        cur_workspace_subnum = monmap[cur_workspace['output']]

    # create new workspaces if we need to
    cur_workspace_names = [w['name'] for w in cur_workspaces]

    for output, subnum in monmap.items():
        new_ws = "{}.{}".format(workspace, subnum)

        i3.command("focus output {}".format(output))
        i3.command("workspace --no-auto-back-and-forth {}".format(new_ws))

    # what should be focused?
    target_ws = "{}.{}".format(workspace, cur_workspace_subnum)

    return target_ws

@click.command()
@click.argument('workspace')
def switch(workspace):
    """
    Switch it to the base workspace passed in, creating workspaces as needed
    """
    target_ws = _make_workspaces(workspace)
    i3.command("workspace {}".format(target_ws))

cli.add_command(switch)

@click.command()
@click.argument('workspace')
def move(workspace):
    """
    Move selected item to base workspace, same monitor it's currently on
    """
    cur_con = i3.get_tree().find_focused()

    # call helper
    target_ws = _make_workspaces(workspace)

    # move container
    i3.command("[con_id=\"{}\"] move container to workspace {}".format(cur_con.id, target_ws))
    i3.command("workspace {}".format(target_ws))

cli.add_command(move)

if __name__ == "__main__":
    cli()
