### Habitican Curse

* A Terminal Application for HabitRPG with basic terminal GUI features. Implemented using the curses library.

### Configuring Habitican Curse

* Habitican Curse uses the amazing `requests` library to connect to Habitica. Please install it first using `pip install requests`.

* You will need to have a 256-color terminal, with support for basic unicode symbols. The shell used in the screenshots is the simple GNOME shell and will suffice.

* Create an rc file named .habiticarc in your home directory. Put your userID in the first line, followed by your key in the second. Please maintain this order. Don't forget to change read/write permissions accordingly.

* Launch habitica.py from the source directory using `python habitica.py`

* WARNING: There can be undefined behavior if your supplied UUID and KEY are incorrect. Also please do not use Ctrl-C to exit. Exception handling has not been implemented completely. Only use `:q` to exit.

### Common Commands

* `:help` - View detailed description of all the commands.

* Use arrow keys for movement. You can also the Vim-style h, j, k, l bindings for movement.

* Press `m` to mark an item for toggling its completion status. Press `+` and `-` for habits. Press the key again to unmark it. Similarly press `d` to toggle deletion status

* `:w` to write any changes to server. The `completed` status for the marked items changes. Health, Gold, XP are automatically updated. 

* `:r` to reload the tasks from the server - basically rebooting the interface.

* `c` to display the checklist(if any) for the highlighted task. Press arrow keys to navigate, `m` for marking, `d` for delete, and `ENTER` for changing name etc. Press enter on `Add an Item` to add a new checklist item.

* `:q` to exit.

* `:et`, `:ed`, `:eh` to create a TODO, Daily and a Habit respectively.

### Party

* If you are a member of a party, you can type `:party` to display the chat messages and quest details (if any).

### Data-Display

* `:data-display` to display some basic details like "Est. Damage to You", "Est. Damage to Party", "Est. Damage to Boss" etc. The statistical functions used are borrowed from the excellent data-display tool by LadyAlys (https://github.com/Alys/tools-for-habitrpg)

### ScreenShots

#### Main Task Menu
![Main Task Menu](/img/TaskScreenShot.png)

#### Task Marking
![Party Details](/img/MarkingScreenShot.png)

#### Party Details
![Party Details](/img/PartyScreenShot.png)

#### Checklist Example
![Party Details](/img/ChecklistScreenShot.png)
