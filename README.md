### Habitican Curse

* A Terminal Application for HabitRPG with basic terminal GUI features. Implemented using the curses library.

### Common Commands

* `:w` to write any changes to server. `:r` to reload the tasks from the server - basically rebooting the interface.

### Checklist Feature

* The tasks marked with a downward triangle have checklists associated with them. Press `c` to display them. You can navigate using arrow keys

* Press `m` to mark an item. It will toggle the done status (It won't write it though)

* When you've made your changes, you can quit either by pressing `q` or `c`. Pressing `q` will undo all changes. Pressing `c` will keep the changes

* However you still have to do `:w` to write changes to the server

### Modifying Items (Current Features)

* Currently, changing the difficulty of a task is supported.

* Type `:set d 0.1` or `:set d trivial` to change difficulty to trivial

* Type `:set d 1` or `:set d easy` to change difficulty to easy

* Type `:set d 1.5` or `:set d medium` to change difficulty to medium

* Type `:set d 2` or `:set d hard` to change difficulty to hard

* As always, you have to `:w` to push changes to the server.
