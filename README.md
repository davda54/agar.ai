# agar.ai (WIP)

A clone of the famous multiplayer game https://agar.io/ in python 3.6 that supports third-party AI controllers and can be easily used for reinforcement learning experiments.

![Alt text](/img/screenshot.png)

&nbsp;
## Usage

#### Play

To play a game with your mouse, start the program with tag `--play` and then list the controllers used by opponents, for example: `python main.py --play 3,coward_hungry_ai_controller 8,stupid_hungry_ai_controller 1,middle_ai_controller`

A left click on your mouse splits the blobs, a right click shoots a pellet from the main blob.

#### Create New Controller

Your new controller should be a class with the same name as its file and should be placed inside the 'controllers' folder. The class should implement `abstract_controller` and should have parameterless constructor and parameterless method `update()`. When correctly mentioned in command-line arguments, the class will be automatically registered and provided with an instance of `manipulator` class in `self.manipulator`. The `update()` function is automatically called each frame, inside you should use (only) `self.manipulator` to gather information about the environment and control your blobs.

#### Command Line Arguments

`main.py [-h] [--display] [--play] N,C [N,C ...]`

##### Positional Arguments:
- `N,C`         list of pairs where C is controller class name and N is the
              number of these controllers to instantiate

##### Optional Arguments:
- `-h`, `--help`  show this help message and exit
- `--display`   display the first controller from the first person view
- `--play`      play for one blob manually

##### Call Examples
```
python main.py 10,coward_hungry_ai_controller
python main.py --display 3,coward_hungry_ai_controller 8,stupid_hungry_ai_controller 1,middle_ai_controller
python main.py --play 3,coward_hungry_ai_controller 8,stupid_hungry_ai_controller 1,middle_ai_controller
```

#### Packages
- pygame

&nbsp;
## Rules

TODO

#### Reference on Parameter Settings
https://gamefaqs.gamespot.com/webonly/163063-agario/faqs/73510

&nbsp;
## TODO

- [ ] support fast play without graphical interface
- [ ] play a batch of games and output the statistics
- [ ] make a reasonable game mode (2 minute play with resurrection?) that can be better used for reinforcement learning
- [ ] team play
- [ ] add comments
- [ ] create an interface for reinforcement learning
- [ ] add leaderboard to GameboardView
