# Minecraft Mazes (MakeCode)

I created this code for my two kids who loving playing with Minecraft and coding with Scratch. So, when [Microsoft made Minecraft Education Edition available to parents](https://education.minecraft.net/en-us/get-started/parents?utm_source=github-minecraft-mazes-makecode), it seemed like a perfect opportunity to show them how [MakeCode](https://minecraft.makecode.com/setup) can be used to create (and solve) random mazes.

### Contents 
- [What mazes can I make?](#what-mazes-can-i-make-with-the-code)
- [How do I import and use the code?](#how-do-i-import-and-use-the-code)
- [How can I change the maze blocks?](#how-can-i-change-the-maze-blocks)
- [How does the buildMaze function work?](#how-does-the-buildmaze-function-work)
- [How does the solveMaze function work?](#how-does-the-solvemaze-function-work)
- [How can I buy you a coffee?](#how-can-i-buy-you-a-coffee) ☕️
- [Frequently asked questions](#frequently-asked-questions)

### Notes
- This code can be used with [Minecraft Education Edition](https://minecraft.makecode.com/setup/minecraft-education-edition) or [Minecraft for Windows 10](https://minecraft.makecode.com/setup/minecraft-windows10).
- If you're looking for a Python version of this code, don't worry... it's coming soon!
- I deliberately wrote this code in a way that would make it as easy as possible for kids to understand what's going on. This means that there’s some deliberate repetition of code blocks so that they can easily compare how the different mazes are built.

***

## What mazes can I make with the code?

- A simple maze with [n] rows x [n] columns
- A tower maze with [n] rows x [n] columns x [n] layers
- A pyramid maze with [n] layers
- A diamond maze with [n] layers

***

## How do I import and use the code?

- Load [Minecraft Education Edition](https://minecraft.makecode.com/setup/minecraft-education-edition) or [Minecraft for Windows 10](https://minecraft.makecode.com/setup/minecraft-windows10).
- Create a new world or join an existing one.
- Open the Code Builder window.
- Import the code using this URL: `link`
- Close the Code Builder window.
- Open the Chat and Commands window.
- Type `maze 5 5` for a simple maze with 10 rows and 10 columns.
- Type `tower 5 5 5` for a tower maze with 5 rows, 5 columns, and 5 maze layers.
- Type `pyramid 5` for a pyramid maze with 5 maze layers.
- Type `diamond 5` for a diamond maze with 5 maze layers.

By default, the code will build the maze and then try to solve it. You can’t build a second maze until it’s finished solving the first one, as the code is still running. If you’re feeling impatient and you want to build lots of mazes quickly, then you have two options:

- **Option 1:** Open and the close the Code Builder window. This will stop the current code from running and you can then start building a new maze. However, it sometimes takes a few seconds after closing the Code Builder window until Minecraft is actually ready to run the code.

- **Option 2:** Open the Code Builder window and change the `solve_maze` variable to `false` in one or more of the following functions:
  - `initialiseMazeVariables`
  - `initialiseTowerVariables`
  - `initialisePyramidVariables`
  - `initialiseDiamondVariables`

***

## How can I change the maze blocks?

You can experiment with different styles of mazes by changing the `wall_block` variable in the following functions:
- `initialiseMazeVariables`
- `initialiseTowerVariables`
- `initialisePyramidVariables`
- `initialiseDiamondVariables`

Try building mazes out of wood, stone, bricks, slime, or even glass. However, beware of trying to build mazes from sand or vegetation, as they will collapse or change shape. Also, building a maze from ice is not a great idea if you then put torches inside... 

If you want to experiment with really large mazes, you can change the `maze_size_maximum` variables in the above functions. Just be careful when building large mazes close to things that your kids have spent hours creating, as the mazes will destroy everything in their path... 🦖

***

## How does the buildMaze function work?

The mazes are built using a **recursive backtracker algorithm**. 

Imagine a maze grid with unlinked cells. Pick a random cell in the maze and add it to a working list. 

Now, repeat the following loop until there are no cells left in the working list:
- Use the cell at the end of the working list as the current cell.
- If the current cell has not been visited before, then mark it as visited.
- If the current cell has unvisited neighbours then:
  - Pick one of them at random.
  - Link a path to it through the wall.
  - Add that neighbouring cell to the end of the working list.
- If the current cell has no unvisited neighbours then: 
  - Remove the current cell from the end of the working list.

Try building a large maze (20 x 20) and watch how the algorithm backtracks when it gets itself into a dead end with no unvisited neighbours. Every cell in the maze will eventually get visited and linked to a neighbour.

You can learn more about the recursive backtracker algorithm (and many other wonderful maze algorithms) in Jamis Buck’s amazing book [Maze for Programmers](http://www.mazesforprogrammers.com?utm_source=github-minecraft-mazes-makecode). 🥁

***

## How does the solveMaze function work?

The mazes are solved using a simple **left hand on the wall algorithm**. 

Imagine that you’re in the maze and that it’s dark with no torches. You must keep your left hand on the wall at all times by following these simple rules:

- If you can turn left, then turn left.
- If you can’t turn left but you can go straight ahead, then go straight ahead.
- If you can’t turn left or go straight ahead but you can turn right, then turn right.
- If you can’t turn left, go straight ahead, or turn right, then you must turn around.

The block, pyramid, and diamond mazes include one additional rule at the beginning to move down through the layers:
- If you can go down to the next layer, then go down.

The `solveMaze` function also implements a shortest path algorithm so that you can see the quickest route through the maze. You can learn more about path shortening [here](https://patrickmccabemakes.com/tutorials/Maze_Solving?utm_source=github-minecraft-mazes-makecode). 

If you’re looking for some fun, try racing the maze solver (or your friends) by following the rules above and seeing if you can get to the exit first.🥇

*** 

## How can I buy you a coffee? 

☕️ If you find this code useful or inspiring, then feel free to **[buy me a coffee](https://www.buymeacoffee.com/crux)** (or two, or three). 

😊 Many thanks in advance! 

***

## Frequently asked questions

**What’s the most difficult maze to solve?**
A glass maze with no torches. Seriously, try it…

**Can I use the code with my students in a lesson?**
Please, please do. You can have a lot of fun talking about how the mazes are built and solved without needing to understand every line of code.

**Can I share the code with others?**
Sure. Please give them the link to this GitHub page and then they’ll always be able to download the latest version with any updates.

**Can I modify the code slightly, call it my own, and then sell it?**
Er, no. Please read the license. ✌️

***

