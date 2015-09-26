### Habitican Curse

* A Terminal Application for HabitRPG with basic terminal GUI features. Implemented using the curses library.

### Configuring Habitican Curse

* Create an rc file named .habiticarc in your home directory. Put your userID in the first line, followed by your key in the second. Please maintain this order. Don't forget to change read/write permissions accordingly.

* Launch habitica.py from the source directory using `python habitica.py`

### Common Commands

* Press `m` to mark an item for toggling its completion status. Press `+` and `-` for habits. Press the key again to unmark it. Similarly press `d` to toggle deletion status

* `:w` to write any changes to server. The `completed` status for the marked items changes. Health, Gold, XP are automatically updated. 

* `:r` to reload the tasks from the server - basically rebooting the interface.

* `c` to display the checklist(if any) for the highlighted task. Press arrow keys to navigate, `m` for marking, `d` for delete, and `ENTER` for changing name etc. Press enter on `Add an Item` to add a new checklist item.

### Party

* If you are a member of a party, you can type `:party` to display the chat messages and quest details (if any).

### Data-Display

* `:data-display` to display some basic details like "Est. Damage to You", "Est. Damage to Party", "Est. Damage to Boss" etc. The statistical functions used are borrowed from the excellent data-display tool by LadyAlys (https://github.com/Alys/tools-for-habitrpg)

### ScreenShots

![Main Task Menu](/img/TaskScreenShot.png)
![Party Details](/img/PartyScreenShot.png)
