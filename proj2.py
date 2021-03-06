"""
File:    proj2.py
Author:  Nicholas Perry
Date:    10/29/2019
Section: 25
E-mail:  nperry2@umbc.edu
Description: The main code for the pen and paper game sim.
Sim is a game where two users make lines between numbers. The first
person to make a triangle between the points loses.
"""
from proj2_ui import print_board


def validate_input(user_input):
    """
    :param user_input: some list of numbers
    :return: False if length of the list is not 2 or does not have all numbers
    in the list on the interval 1 - 6, true for all else
    """
    if len(user_input) != 2:
        return False
    for i in range(len(user_input)):
        if user_input[i] > 6 or user_input[i] < 1:
            return False
    return True


def in_order(user_list):
    """
    Makes the given list into numerical order
    :param user_list: a list from the user
    :return: the list in numerical order
    """
    if len(user_list) != 2:
        return user_list
    if user_list[1] < user_list[0]:
        temp = user_list[1]
        user_list[1] = user_list[0]
        user_list[0] = temp
    return user_list


def input_to_list(standard_input):
    """
    Changes the standard user_input into a standard list
    :param standard_input: the user input
    :return: a standard list
    """
    user_list_str = standard_input.split()
    user_list_int = []
    for i in range(len(user_list_str)):
        user_list_int.append(int(user_list_str[i]))
    return in_order(user_list_int)


def check_is_valid_line(used_lines, user_list):
    """
    Checks to see if the user_list matches any lists already covered
    :param used_lines: all of the already covered lines
    :param user_list: the list trying to cover a line
    :return: true if the line has not been covered already, false for all else
    """
    if len(used_lines) > 0:
        for i in range(len(used_lines)):
            if used_lines[i] == user_list:
                return False
    return True


def combine_lists(list_one, list_two):
    """
    Combines the values of two 2D lists into one 2D list
    :param list_one: the first 2D list
    :param list_two: the second 2D list
    :return: one 2D list
    """
    combined = []
    for i in list_one:
        combined.append(i)
    for i in list_two:
        combined.append(i)

    return combined


def check_for_triangle(player_list):
    """
    Checks to see if the list makes a triangle
    :param player_list: the list of moves the player has made
    :return: true if the list does make a triangle, false for all else
    """
    # first value in the list
    first_num = []
    # a list of coordinates that are last needed to make a triangle
    target_points = []

    # appends all the values of the first coordinates which are all the smaller number
    for i in range(len(player_list)):
        first_num.append(player_list[i][0])
    # loops through the first values
    for i in range(len(first_num)):
        for j in range(len(first_num) - 1):
            # Checks to see if any of the first numbers match each other
            if first_num[j + 1] == first_num[i]:
                # makes a ordered coordinate pair that contains the second values
                # of those numbers that equal each other
                target_list = [player_list[i][1], player_list[j + 1][1]]
                target_list = in_order(target_list)
                # appends the values only if they are valid
                if target_list[0] != target_list[1] and check_is_valid_line(target_points, target_list):
                    target_points.append(target_list)
    # checks to see if any of the coordinates in target_points are also in the player_list
    for i in target_points:
        for j in player_list:
            if i == j:
                return True
    return False


if __name__ == '__main__':
    player_one_char = input("Hello, what character would player 1 like to use?")
    player_two_char = input("Hello, what character would player 2 like to use?")

    player_one_moves = []
    player_two_moves = []
    combined_list = []

    is_game_over = False
    player_turn = 1

    while not is_game_over:
        is_skip_section = False
        print_board(player_one_moves, player_one_char, player_two_moves, player_two_char)
        line = input("Enter a line for player %d:" % player_turn)

        list_of_line = input_to_list(line)
        if validate_input(list_of_line):
            # Checks players moves and if valid continues the program
            # If not, skips back to the start of the loop and the same player tries again
            if player_turn == 1 and check_is_valid_line(combined_list, list_of_line):
                player_one_list = player_one_moves.append(list_of_line)
                player_turn = 2
            elif player_turn == 2 and check_is_valid_line(combined_list, list_of_line):
                player_two_list = player_two_moves.append(list_of_line)
                player_turn = 1
            else:
                print("Not a valid line")
                is_skip_section = True
        else:
            # The players input was not valid and the loop starts over again
            print("Not a valid input")
            is_skip_section = True

        if not is_skip_section:
            combined_list = combine_lists(player_one_moves, player_two_moves)

            # checks the players turn specifically if they made a triangle
            # if the player did, the boolean flag stops the loop
            if player_turn == 2 and check_for_triangle(player_one_moves):
                print_board(player_one_moves, player_one_char, player_two_moves, player_two_char)
                is_game_over = True
                print("Game over. player %d loses." % 1)
            if player_turn == 1 and check_for_triangle(player_two_moves):
                print_board(player_one_moves, player_one_char, player_two_moves, player_two_char)
                is_game_over = True
                print("Game over. player %d loses." % 2)
