### Habitican Curse

* A Terminal Application for HabitRPG with basic terminal GUI features. Implemented using the curses library.

### Common Commands

* Press `m` to mark an item for toggling its completion status. Press `+` and `-` for habits. Press the key again to unmark it

* `:w` to write any changes to server. The `completed` status for the marked items changes. Health, Gold, XP are automatically updated. 

* `:r` to reload the tasks from the server - basically rebooting the interface.

### Checklist Feature

* The tasks marked with a downward triangle have checklists associated with them. Press `c` to display them. You can navigate using arrow keys

* Press `m` to mark an item. It will toggle the done status (It won't write it though). Press `m` again to toggle mark status.

* Press `d` to mark an item for deletion. You cannot mark this item as long as it is marked for deletion. Press `d` again to toggle deletion status.

* When you've made your changes, you can quit either by pressing `q` or `c`. Pressing `q` will undo all changes. Pressing `c` will keep the changes

* You can also add a checklist item by navigating down to the dummy checklist item titled `Add Item`. Press ENTER to enable string input. After inputting the name, press Enter again to save it.

* However you still have to do `:w` to write changes to the server

### Modifying Items (Current Features)

* Currently, changing the difficulty of a task is supported.

* Type `:set d 0.1` or `:set d trivial` to change difficulty to trivial

* Type `:set d 1` or `:set d easy` to change difficulty to easy

* Type `:set d 1.5` or `:set d medium` to change difficulty to medium

* Type `:set d 2` or `:set d hard` to change difficulty to hard

* As always, you have to `:w` to push changes to the server.

### Quests

* If you are involved in a quest, you can type `:boss` to display the boss's health as well as the chat messages from the party.
