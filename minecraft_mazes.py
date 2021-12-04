# MINECRAFT MAZES v1.0
# Copyright 2021, David Bailey / Crux
# Looking for instructions or more info? Try here:
# https://github.com/crux888/minecraft-mazes-makecode


# Do you want your mazes to look different?
# If so, then try changing these values...
maze_blocks = COBBLESTONE
tower_blocks = STONE_BRICKS
pyramid_blocks = CHISELED_SANDSTONE
diamond_blocks = GOLD_BLOCK
add_torches = True
solve_maze = True
wall_height = 2


# Hmmm, I wouldn't recommend changing any of these values though...
# They're global constants and variables used throughout the code
maze_type = ""
maze_rows = 0
maze_columns = 0
maze_layers = 0
player_position: Position = None
maze_position: Position = None
entrance_position: Position = None
exit_position: Position = None
robot_position: Position = None
robot_orientation = ""
maze_solve_path: List[str] = []
blocks_used = 0
torches_used = 0
wall_blocks = 0
time_start = 0
current_layer = 0
middle_layer = 0
x_offset = 0
z_offset = 0
searched_steps = 0
solution_steps = 0
path_block = LIME_CARPET
maximum_maze_rows_columns = 25
maximum_maze_layers = 1
minimum_maze_rows_columns = 3
minimum_maze_layers = 3


###############
# SIMPLE MAZE #
###############

def on_on_chat(rows, columns):
    # Define global variables
    global maze_type, maze_rows, maze_columns, maze_layers
    # Set global variables for this type of maze
    maze_type = "maze"
    maze_rows = rows
    maze_columns = columns
    maze_layers = 1
    # Run the main loop to build and solve the maze
    mainLoop()


player.on_chat("maze", on_on_chat)


##############
# TOWER MAZE #
##############

def on_on_chat2(rows, columns, layers):
    # Define global variables
    global maze_type, maze_rows, maze_columns, maze_layers
    # Set global variables for this type of maze
    maze_type = "tower"
    maze_rows = rows
    maze_columns = columns
    maze_layers = layers
    # Run the main loop to build and solve the maze
    mainLoop()


player.on_chat("tower", on_on_chat2)


################
# PYRAMID MAZE #
################

def on_on_chat3(layers):
    # Define global variables
    global maze_type, maze_layers
    # Set global variables for this type of maze
    maze_type = "pyramid"
    maze_layers = layers
    # Run the main loop to build and solve the maze
    mainLoop()


player.on_chat("pyramid", on_on_chat3)


################
# DIAMOND MAZE #
################

def on_on_chat4(layers):
    # Define global variables
    global maze_type, maze_layers
    # Set global variables for this type of maze
    maze_type = "diamond"
    maze_layers = layers
    # Run the main loop to build and solve the maze
    mainLoop()


player.on_chat("diamond", on_on_chat4)


#############
# MAIN LOOP #
#############

def mainLoop():
    # Define global variables
    global maze_type, maze_rows, maze_columns, maze_layers, current_layer, middle_layer
    # Initialise maze variables
    initialiseMazeVariables()
    # Draw a foundation layer underneath the maze
    drawMazeFoundations()
    # Build the maze layers
    current_layer = maze_layers
    for index in range(maze_layers):
        if maze_type == "pyramid":
            # Set maze_rows and maze_columns for a pyramid maze
            maze_rows = current_layer * 2 + 1
            maze_columns = maze_rows
        elif maze_type == "diamond":
            # Set maze_rows and maze_columns for a diamond maze
            if current_layer >= middle_layer:
                maze_rows = (maze_layers - current_layer + 1) * 2 + 1
            else:
                maze_rows = (maze_layers - middle_layer + 1) * 2 + \
                    1 - ((middle_layer - current_layer) * 2)
            maze_columns = maze_rows
        # Draw the maze grid
        drawMazeGrid()
        # Build the maze, dude
        buildMaze()
        # Add a roof for tower, pyramid, or diamond mazes
        if (maze_type in ["tower", "pyramid", "diamond"]):
            drawMazeRoof()
        current_layer -= 1
    # Draw the maze doors
    drawMazeDoors()
    # Show the maze information
    showMazeInfo()
    # Solve the maze, babe
    if solve_maze:
        solveMaze()


def initialiseMazeVariables():
    # Define global variables
    global maze_type, maze_rows, maze_columns, player_position, maze_position, maze_blocks
    global blocks_used, torches_used, wall_blocks, time_start, middle_layer
    global tower_blocks, pyramid_blocks, diamond_blocks
    # Check if the maze needs resizing
    checkMazeSize()
    # Set additional variables for diamond mazes
    if maze_type == "diamond":
        maze_rows = 3
        maze_columns = 3
        middle_layer = Math.ceil(maze_layers / 2)
    # Display a status message
    if (maze_type == "maze"):
        player.say("Creating maze...")
    else:
        player.say("Creating " + maze_type + " maze...")
    # Save the original position of the player in case they move while the maze is being built
    player_position = player.position()
    # Set the corner position of the maze so that the player will be facing the entrance/exit
    if (maze_type == "pyramid"):
        maze_position = positions.add(player_position,
                                      pos(maze_layers * -2, 0, 3))
    else:
        maze_position = positions.add(player_position,
                                      pos((Math.ceil(maze_columns / 2) - 1) * -2, 0, 3))
    # Check if the maze_blocks variable needs updating for tower, pyramid, or diamond mazes
    if (maze_type == "tower"):
        wall_blocks = tower_blocks
    elif (maze_type == "pyramid"):
        wall_blocks = pyramid_blocks
    elif (maze_type == "diamond"):
        wall_blocks = diamond_blocks
    else:
        wall_blocks = maze_blocks
    # Reset maze counters and timer
    blocks_used = 0
    torches_used = 0
    time_start = gameplay.time_query(GAME_TIME)


def checkMazeSize():
    # Define global variables
    global maze_type, maze_rows, maze_columns, maze_layers, wall_height, add_torches
    # Set the message flag to false
    show_resize_message = False
    # Check maze_rows and maze_columns
    if (maze_type in ["maze", "tower"]):
        if (maze_rows < minimum_maze_rows_columns):
            maze_rows = minimum_maze_rows_columns
            show_resize_message = True
        elif (maze_rows > maximum_maze_rows_columns):
            maze_rows = maximum_maze_rows_columns
            show_resize_message = True
        if (maze_columns < minimum_maze_rows_columns):
            maze_columns = minimum_maze_rows_columns
            show_resize_message = True
        elif (maze_columns > maximum_maze_rows_columns):
            maze_columns = maximum_maze_rows_columns
            show_resize_message = True
    # Check maze_layers
    if (maze_type in ["tower", "pyramid", "diamond"]):
        if (maze_layers < minimum_maze_layers):
            maze_layers = minimum_maze_layers
            show_resize_message = True
        elif (maze_layers > maximum_maze_layers):
            maze_layers = maximum_maze_layers
            show_resize_message = True
    # Make sure that maze_layers is an odd number for diamond mazes
    if maze_type == "diamond":
        if Math.round(maze_layers / 2) == maze_layers / 2:
            maze_layers += 1
            show_resize_message = True
    # Check wall_height
    if wall_height < 2:
        if maze_type == "maze":
            wall_height = 1
            add_torches = False
        else:
            wall_height = 2
    # Display a status message if the maze has been resized
    if (show_resize_message):
        if (maze_type == "maze"):
            player.say("Resized maze (" + str(maze_rows) +
                       " x " + str(maze_columns) + ")")
        elif (maze_type == "tower"):
            player.say("Resized tower maze (" + str(maze_rows) + " x " +
                       str(maze_columns) + " x " + str(maze_layers) + ")")
        elif (maze_type in ["pyramid", "diamond"]):
            player.say("Resized " + maze_type +
                       " maze (" + str(maze_layers) + " layers)")


def drawMazeFoundations():
    # Define global variables
    global maze_rows, maze_columns, maze_layers, maze_position, maze_blocks, blocks_used
    # Check if maze_rows and maze_columns need calculating for a pyramid or diamond maze_columns
    if (maze_type == "pyramid"):
        maze_rows = maze_layers * 2 + 1
        maze_columns = maze_layers * 2 + 1
    elif (maze_type == "diamond"):
        maze_rows = 3
        maze_columns = 3
    # Draw a foundation layer underneath the maze
    blocks.fill(wall_blocks,
                positions.add(maze_position, pos(-1, -1, -1)),
                positions.add(maze_position,
                              pos(maze_columns * 2 - 1, -1, maze_rows * 2 - 1)),
                FillOperation.REPLACE)
    # Update the blocks_used variable based on the size of the foundation layer
    blocks_used += (maze_rows * 2 + 1) * (maze_columns * 2 + 1)


def drawMazeGrid():
    # Define global variables
    global maze_rows, maze_columns, maze_layers, maze_position, maze_blocks, blocks_used, wall_height
    # Initialise local variables/constants
    x_coordinate = maze_position.get_value(Axis.X) - 1
    y_coordinate = maze_position.get_value(Axis.Y)
    z_coordinate = maze_position.get_value(Axis.Z) - 1
    # Clear space for the maze by filling the area with air
    blocks.fill(AIR,
                world(x_coordinate, y_coordinate, z_coordinate),
                world(x_coordinate + maze_columns * 2,
                      y_coordinate + wall_height - 1,
                      z_coordinate + maze_rows * 2),
                FillOperation.REPLACE)
    # Draw the maze rows
    line_length = maze_columns * 2
    for index in range(maze_rows + 1):
        blocks.fill(wall_blocks,
                    world(x_coordinate, y_coordinate, z_coordinate),
                    world(x_coordinate + line_length,
                          y_coordinate + wall_height - 1,
                          z_coordinate),
                    FillOperation.REPLACE)
        z_coordinate += 2
    # Draw the maze columns
    line_length = maze_rows * 2
    z_coordinate = maze_position.get_value(Axis.Z) - 1
    for index in range(maze_columns + 1):
        blocks.fill(wall_blocks,
                    world(x_coordinate, y_coordinate, z_coordinate),
                    world(x_coordinate,
                          y_coordinate + wall_height - 1,
                          z_coordinate + line_length),
                    FillOperation.REPLACE)
        x_coordinate += 2
    # Update the blocks_used variable based on the size of maze grid
    blocks_used += ((maze_rows + 1) * (maze_columns * 2 + 1)
                    + maze_columns * (maze_rows + 1)) * wall_height


def buildMaze():
    # Define global variables
    global maze_rows, maze_columns, maze_layers, maze_position, maze_blocks, blocks_used, torches_used, wall_height
    # Intialise local variables
    unvisited_neighbours: List[str] = []
    current_cell_row = 0
    current_cell_column = 0
    current_cell_position_in_list = 0
    connection_direction = ""
    x_coordinate = 0
    y_coordinate = 0
    z_coordinate = 0
    # Create a list of unvisited cells
    cell_unvisited: List[number] = []
    for index in range(maze_rows * maze_columns):
        cell_unvisited.append(1)
    # Create the empty stack
    stack_rows: List[number] = []
    stack_columns: List[number] = []
    # Add a random cell to the top of the stack
    stack_rows.append(randint(1, maze_rows) - 1)
    stack_columns.append(randint(1, maze_columns) - 1)
    # Main loop that keeps running until there are no cells left in the stack
    while len(stack_rows) > 0:
        # Get the current cell from the top of the stack
        current_cell_row = stack_rows[len(stack_rows) - 1]
        current_cell_column = stack_columns[len(stack_columns) - 1]
        # Calculate the x, y, and z coordinates of the current cell
        x_coordinate = maze_position.get_value(
            Axis.X) + (maze_columns - current_cell_column - 1) * 2
        y_coordinate = maze_position.get_value(Axis.Y) + 0
        z_coordinate = maze_position.get_value(
            Axis.Z) + (maze_rows - current_cell_row - 1) * 2
        # Mark the current cell as "visited"
        cell_unvisited[current_cell_row *
                       maze_columns + current_cell_column] = 0
        # Get a list of unvisited neighbours for the current cell
        unvisited_neighbours = []
        current_cell_position_in_list = current_cell_row * \
            maze_columns + current_cell_column
        if current_cell_row != 0:
            if (cell_unvisited[current_cell_position_in_list - maze_columns] == 1):
                unvisited_neighbours.append("N")
        if current_cell_row != maze_rows - 1:
            if (cell_unvisited[current_cell_position_in_list + maze_columns] == 1):
                unvisited_neighbours.append("S")
        if current_cell_column != maze_columns - 1:
            if (cell_unvisited[current_cell_position_in_list + 1] == 1):
                unvisited_neighbours.append("E")
        if current_cell_column != 0:
            if (cell_unvisited[current_cell_position_in_list - 1] == 1):
                unvisited_neighbours.append("W")
        # Check if there are unvisited neighbours
        if len(unvisited_neighbours) == 0:
            # There are no unvisited neighbours, so remove the current cell from the top of the stack
            stack_rows.pop()
            stack_columns.pop()
        else:
            # There are unvisited neighbours, so choose one at random, and add it to the top of the stack
            x_offset = 0
            z_offset = 0
            connection_direction = unvisited_neighbours._pick_random()
            if connection_direction == "N":
                z_offset = 1
                stack_rows.append(current_cell_row - 1)
                stack_columns.append(current_cell_column)
            elif connection_direction == "S":
                z_offset = -1
                stack_rows.append(current_cell_row + 1)
                stack_columns.append(current_cell_column)
            elif connection_direction == "E":
                x_offset = -1
                stack_rows.append(current_cell_row)
                stack_columns.append(current_cell_column + 1)
            elif connection_direction == "W":
                x_offset = 1
                stack_rows.append(current_cell_row)
                stack_columns.append(current_cell_column - 1)
            else:
                player.say("Error: Unknown connection_direction")
            # Carve a path between the current cell and the new, unvisited neighbour
            blocks.fill(AIR,
                        world(x_coordinate + x_offset,
                              y_coordinate + 0,
                              z_coordinate + z_offset),
                        world(x_coordinate + x_offset,
                              y_coordinate + wall_height - 1,
                              z_coordinate + z_offset),
                        FillOperation.REPLACE)
            # Update the blocks_used variable to account for the blocks that have been removed
            blocks_used = blocks_used - wall_height
            # Add torches to the maze
            if (add_torches):
                if randint(1, 3) == 1:
                    blocks.place(TORCH, world(x_coordinate + 0,
                                              y_coordinate + 1, z_coordinate + 0))
                    torches_used += 1


def drawMazeRoof():
    # Define global variables
    global maze_type, maze_rows, maze_columns, maze_layers, maze_position, wall_height
    global wall_blocks, blocks_used, current_layer, entrance_position, middle_layer
    # Initialise local variables
    x_offset = 0
    z_offset = 0
    roof_position1: Position = None
    roof_position2: Position = None
    # Draw a roof on the maze layer
    if maze_type == "tower":
        # Set the roof coordinates for a tower maze
        roof_position1 = positions.add(maze_position,
                                       pos(-1, wall_height, -1))
        roof_position2 = positions.add(maze_position,
                                       pos(maze_columns * 2 - 1, wall_height * 2 - 1, maze_rows * 2 - 1))
        # Set the entrance position for a tower maze
        if current_layer == 1:
            x_offset = (Math.ceil(maze_columns / 2) - 1) * 2
            z_offset = (Math.ceil(maze_rows / 2) - 1) * 2
        else:
            x_offset = randint(0, maze_columns - 1) * 2
            z_offset = randint(0, maze_rows - 1) * 2
        entrance_position = positions.add(
            maze_position, pos(x_offset, 0, z_offset))
        # Move the tower maze up to the next layer
        maze_position = positions.add(
            maze_position, pos(0, wall_height * 2, 0))

    elif maze_type == "pyramid":
        # Set the roof coordinates for a pyramid maze (roof is smaller than current layer)
        roof_position1 = positions.add(maze_position,
                                       pos(0, wall_height, 0))
        roof_position2 = positions.add(maze_position,
                                       pos(maze_columns * 2 - 2, wall_height * 2 - 1, maze_rows * 2 - 2))
        # Set the entrance offsets for a pyramid maze (roof is smaller than current layer)
        x_offset = randint(1, maze_columns - 2) * 2
        z_offset = randint(1, maze_rows - 2) * 2
        entrance_position = positions.add(
            maze_position, pos(x_offset, 0, z_offset))
        # Move the pyramid maze up to the next layer (decreasing in size)
        maze_position = positions.add(
            maze_position, pos(2, wall_height * 2, 2))

    elif maze_type == "diamond":
        if current_layer > middle_layer:
            # Lower half of a diamond maze...
            # Set the roof coordinates for a diamond maze (roof is larger than current layer)
            roof_position1 = positions.add(maze_position,
                                           pos(-2, wall_height, -2))
            roof_position2 = positions.add(maze_position,
                                           pos(maze_columns * 2 + 0, wall_height * 2 - 1, maze_rows * 2 + 0))
            # Set the entrance offsets for a diamond maze (roof is larger than current layer)
            x_offset = randint(0, maze_columns - 1) * 2
            z_offset = randint(0, maze_rows - 1) * 2
            entrance_position = positions.add(
                maze_position, pos(x_offset, 0, z_offset))
            # Move the diamond maze up to the next layer (increasing in size)
            maze_position = positions.add(
                maze_position, pos(-2, wall_height * 2, -2))
        else:
            # Upper half of a diamond maze...
            # Set the roof coordinates for a diamond maze (roof is smaller than current layer)
            roof_position1 = positions.add(maze_position,
                                           pos(0, wall_height, 0))
            roof_position2 = positions.add(maze_position,
                                           pos(maze_columns * 2 - 2, wall_height * 2 - 1, maze_rows * 2 - 2))
            # Set the entrance offsets for a diamond maze (roof is smaller than current layer)
            x_offset = randint(1, maze_columns - 2) * 2
            z_offset = randint(1, maze_rows - 2) * 2
            entrance_position = positions.add(
                maze_position, pos(x_offset, 0, z_offset))
            # Move the diamond maze up to the next layer (decreasing in size)
            maze_position = positions.add(
                maze_position, pos(2, wall_height * 2, 2))

    # Draw the floor
    blocks.fill(wall_blocks, roof_position1,
                roof_position2, FillOperation.REPLACE)
    blocks_used += ((roof_position2.get_value(Axis.X) - roof_position1.get_value(Axis.X) + 1) *
                    (roof_position2.get_value(Axis.Y) - roof_position1.get_value(Axis.Y) + 1) *
                    (roof_position2.get_value(Axis.Z) - roof_position1.get_value(Axis.Z) + 1))
    # Draw the entrance
    for index in range(3):
        blocks.fill(SEA_LANTERN, entrance_position,
                    positions.add(entrance_position, pos(
                        0, wall_height * 2 - 1, 0)),
                    FillOperation.REPLACE)
        loops.pause(100)
        blocks.fill(AIR, entrance_position,
                    positions.add(entrance_position, pos(
                        0, wall_height * 2 - 1, 0)),
                    FillOperation.REPLACE)
        loops.pause(100)
    blocks_used -= wall_height


def drawMazeDoors():
    # Define global variables
    global player_position, exit_position, entrance_position, blocks_used
    # Set the exit_position and entrance_position variables
    if maze_type == "maze":
        exit_position = positions.add(
            player_position, pos(0, 0, maze_rows * 2 + 2))
        entrance_position = positions.add(player_position, pos(0, 0, 2))
    else:
        exit_position = positions.add(player_position, pos(0, 0, 2))
    # Draw the exit/entrance
    for count in range(3):
        blocks.fill(SEA_LANTERN,
                    exit_position,
                    positions.add(exit_position, pos(0, wall_height - 1, 0)),
                    FillOperation.REPLACE)
        if maze_type == "maze":
            blocks.fill(SEA_LANTERN,
                        entrance_position,
                        positions.add(entrance_position, pos(
                            0, wall_height - 1, 0)),
                        FillOperation.REPLACE)
        loops.pause(100)
        blocks.fill(AIR,
                    exit_position,
                    positions.add(exit_position, pos(0, wall_height - 1, 0)),
                    FillOperation.REPLACE)
        if maze_type == "maze":
            blocks.fill(AIR,
                        entrance_position,
                        positions.add(entrance_position, pos(
                            0, wall_height - 1, 0)),
                        FillOperation.REPLACE)
        loops.pause(100)
    # Update the blocks_used variable to account for the blocks that have been removed
    blocks_used = blocks_used - wall_height
    if maze_type == "maze":
        blocks_used = blocks_used - wall_height


def showMazeInfo():
    # Define global variables
    global maze_type, time_start, add_torches, blocks_used, torches_used
    # Initialise local variables
    time_seconds = Math.round(
        (gameplay.time_query(GAME_TIME) - time_start) / 20)
    # Display maze information
    if maze_type == "maze":
        player.say("Finished creating maze")
    else:
        player.say("Finished creating " + maze_type + " maze")
    if time_seconds == 1:
        player.say("...Time taken: " + str(time_seconds) + " second")
    elif time_seconds < 60:
        player.say("...Time taken: " + str(time_seconds) + " seconds")
    else:
        time_minutes = Math.round(time_seconds / 60)
        if time_minutes == 1:
            player.say("...Time taken: " + str(time_minutes) + " minute")
        else:
            player.say("...Time taken: " + str(time_minutes) + " minutes")
    player.say("...Blocks used: " + str(blocks_used))
    if add_torches:
        player.say("...Torches used: " + str(torches_used))


def solveMaze():
    # Define global variables
    global robot_position, robot_orientation, maze_solve_path, entrance_position, exit_position
    global searched_steps, solution_steps
    # Initialise local variables
    robot_position = entrance_position
    robot_orientation = "N"
    maze_solve_loop = True
    maze_solve_path = []
    searched_steps = 0
    solution_steps = 0
    time_start = gameplay.time_query(GAME_TIME)
    # Display status message
    if maze_type == "maze":
        player.say("Solving maze...")
    else:
        player.say("Solving " + maze_type + " maze...")
    # Solve the maze, baby...
    while maze_solve_loop:
        # Rule 1: If there's air underneath the (invisible) robot, move it down to the next layer
        if blocks.test_for_block(AIR, positions.add(robot_position, pos(0, -1, 0))):
            robot_position = positions.add(robot_position, pos(0, -1, 0))
            maze_solve_path = []
        # Rule 2: If the (invisible) robot can turn left, then it must turn left
        elif robotTestForAir("Left"):
            robotTurn("Left")
            addToSolvePath("L")
            moveRobotForward()
        # Rule 3: If the (invisible) robot can go straight/forward, then it must go straight/forward
        elif robotTestForAir("Forward"):
            if robotTestForAir("Right"):
                addToSolvePath("S")
            moveRobotForward()
        # Rule 4: If the (invisible) robot can turn right, then it must turn right
        elif robotTestForAir("Right"):
            robotTurn("Right")
            addToSolvePath("R")
            moveRobotForward()
        # Rule 5: If the (invisible) robot is in a dead end, then it must turn back
        else:
            blocks.place(path_block, robot_position)
            loops.pause(200)
            robotTurn("Back")
            addToSolvePath("B")
            moveRobotForward()
        # Rule 6: If the (invisible) robot is at the exit, then stop solving the maze
        if robot_position.get_value(Axis.X) == exit_position.get_value(Axis.X):
            if robot_position.get_value(Axis.Y) == exit_position.get_value(Axis.Y):
                if robot_position.get_value(Axis.Z) == exit_position.get_value(Axis.Z):
                    maze_solve_loop = False
                    moveRobotForward()
    # Display status messages
    if maze_type == "maze":
        player.say("Finished solving maze")
    else:
        player.say("Finished solving " + maze_type + " maze")
    time_seconds = Math.round(
        (gameplay.time_query(GAME_TIME) - time_start) / 20)
    if time_seconds < 60:
        player.say("...Time taken: " + str(time_seconds) + " seconds")
    else:
        time_minutes = Math.round(time_seconds / 60)
        if time_minutes == 1:
            player.say("...Time taken: " + str(time_minutes) + " minute")
        else:
            player.say("...Time taken: " + str(time_minutes) + " minutes")
    player.say("...Path searched: " + str(searched_steps) + " steps")
    player.say("...Path found: " + str(solution_steps) + " steps")


def robotTestForAir(direction: str):
    # Define global variables
    global robot_position, x_offset, z_offset
    robotGetXZOffsets(direction)
    if blocks.test_for_block(wall_blocks,
                             positions.add(robot_position, pos(x_offset, 0, z_offset))):
        return False
    else:
        return True


def robotGetXZOffsets(direction: str):
    # Define global variables
    global x_offset, z_offset, robot_orientation
    # Reset x_offset and z_offset variables
    x_offset = 0
    z_offset = 0
    if robot_orientation == "N":
        if direction == "Left":
            x_offset = 1
        elif direction == "Right":
            x_offset = -1
        else:
            z_offset = 1
    elif robot_orientation == "S":
        if direction == "Left":
            x_offset = -1
        elif direction == "Right":
            x_offset = 1
        else:
            z_offset = -1
    elif robot_orientation == "E":
        if direction == "Left":
            z_offset = 1
        elif direction == "Right":
            z_offset = -1
        else:
            x_offset = -1
    elif robot_orientation == "W":
        if direction == "Left":
            z_offset = -1
        elif direction == "Right":
            z_offset = 1
        else:
            x_offset = 1
    else:
        player.say("Unknown robot orientation")


def robotTurn(direction: str):
    # Define global variables
    global robot_orientation
    if robot_orientation == "N":
        if direction == "Left":
            robot_orientation = "W"
        elif direction == "Right":
            robot_orientation = "E"
        else:
            robot_orientation = "S"
    elif robot_orientation == "S":
        if direction == "Left":
            robot_orientation = "E"
        elif direction == "Right":
            robot_orientation = "W"
        else:
            robot_orientation = "N"
    elif robot_orientation == "E":
        if direction == "Left":
            robot_orientation = "N"
        elif direction == "Right":
            robot_orientation = "S"
        else:
            robot_orientation = "W"
    elif robot_orientation == "W":
        if direction == "Left":
            robot_orientation = "S"
        elif direction == "Right":
            robot_orientation = "N"
        else:
            robot_orientation = "E"
    else:
        player.say("Unknown robot orientation")


def addToSolvePath(text: str):
    # Define global variables
    global maze_solve_path
    # Add the last step to the solution path
    maze_solve_path.append(text)
    # Check if the solution path can be shortened
    if len(maze_solve_path) >= 3:
        last_three_steps = ""
        index = len(maze_solve_path) - 3
        for counter in range(3):
            last_three_steps = last_three_steps + maze_solve_path[index]
            index += 1
        if last_three_steps == "LBR":
            replaceLastThreeSteps("B")
        elif last_three_steps == "LBS":
            replaceLastThreeSteps("R")
        elif last_three_steps == "RBL":
            replaceLastThreeSteps("B")
        elif last_three_steps == "SBL":
            replaceLastThreeSteps("R")
        elif last_three_steps == "SBS":
            replaceLastThreeSteps("B")
        elif last_three_steps == "LBL":
            replaceLastThreeSteps("S")


def replaceLastThreeSteps(text: str):
    # Define global variables
    global maze_solve_path
    # Shorten the solution path by replacing the last three steps
    for index in range(3):
        maze_solve_path.pop()
    maze_solve_path.append(text)


def moveRobotForward():
    # Define global variables
    global maze_solve_path, robot_position, searched_steps, solution_steps
    # Move the (invisible) robot forward 1 step
    if len(maze_solve_path) > 1 and maze_solve_path[len(maze_solve_path) - 1] == "B":
        # Retracing steps, so remove the path behind the (invisible) robot
        blocks.place(AIR, robot_position)
        solution_steps -= 1
    else:
        # Not retracing steps, so leave a path behind the (invisible) robot
        blocks.place(path_block, robot_position)
        solution_steps += 1
    robotGetXZOffsets("Move Forward")
    robot_position = positions.add(robot_position, pos(x_offset, 0, z_offset))
    searched_steps += 1
