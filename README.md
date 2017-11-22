# i3wm Per-Monitor Workspaces

Allows switching all your outputs at once to a major.minor workspace syntax, where you
give the major number, and minor numbers are determined by your outputs.  e.g. switch to
workspace 3, your outputs will be switched to 3.1, 3.2, and 3.3.

i3pmw will attempt to determine your output order left-to-right in a simplistic fashion 
(sorting by `x`). Submit issues if broken.

## TODO

- stick dummy i3wm containers on blank workspaces so they will stay in bar

## Installation

You're on your own for setting up a virtualenv - calling this script from i3wm is unlikely 
to have your PATH/etc setup properly.

Requires [click](http://click.pocoo.org) and [i3ipc-python](github.com/acrisci/i3ipc-python)

```bash
$ pip install -r requirements.txt
```

## Usage

Supports two commands, `switch` and `move`.

### `switch`

Switches all outputs to workspaces of the major number passed.

Configure your switch keybinds in i3wm like this:

```
bindsym $mod+1 exec i3pmw switch 1
bindsym $mod+2 exec i3pmw switch 2
...
```

### `move`

Moves the currently focused item (container?) to the major workspace number passed, on the same
minor number as the current workspace.

Configure your move to workspace keybinds in i3wm like this:

```
bindsym $mod+Shift+1 exec i3pmw move 1
bindsym $mod+Shift+2 exec i3pmw move 2
...
```

