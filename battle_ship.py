"""
COMP.CS.100 Programming 1
Group work by
Emma Kortekangas, emma.kortekangas@tuni.fi, student id K423388
and
Chu Duc Anh, anh.chu@tuni.fi, student id 050358922
Solution of task 12.5: Battleship.
"""

class Ship:
    def __init__(self, name, coordinates):
        """
        Constructor
        :param name: name/type of the ship
        :param coordinates: coordinates of the ship's location as set
        """
        self.__name = name
        self.__coordinates = coordinates
        self.__hits = set()  # set with coordinates that have been hit

    def ship_coordinates(self):
        """
        Return the ships coordinates as a set
        :return: set, coordinates of ship
        """
        return self.__coordinates

    def ship_hit(self, coordinate):
        """
        If the ship is hit, the coordinate at which it was hit is added to
         the set of hit coordinates
        :param coordinate: coordinate the user shot at
        """
        if coordinate in self.__coordinates:
            self.__hits.add(coordinate)

    def ship_sank(self):
        """
        Checks whether a ship has been sunk
        :return: True or False
        """
        if self.__hits == self.__coordinates:
            # checks whether the two sets with the ships coordinates and hit
            #  coordinates are identical
            print(f"You sank a {self.__name}!")
            return True
        else:
            return False

    def ship_name(self):
        """
        Returns the name of the ship
        :return: name of the ship
        """
        return self.__name


def initialize_coordinates():
    """
    Function that initializes a list of dictionaries with coordinates and
    their values
    :return: list of dictionaries where the coordinates (A0, B0 etc.) are
    keys and the payloads are initialized to "  ", these can later be updated
    to * or X (or battleship name initial) after the user makes the shots
    """
    list_coordinates = []  # initialize a nested list with strings A0, B0 etc.
    # there is one list for each line of the grid
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    for num in range(0, 10):
        num = str(num)
        list_num = []  # initialize the list for the number num
        list_coordinates.append(list_num)  # append the list to the nested list
        for let in letters:
            string = let + num
            list_num.append(string)

    list_coordinate_dictionaries = []  # initialize a list that will be filled
    # with dictionaries, there is one dictionary for each line in the grid
    for i in range(len(list_coordinates)):
        keys = list_coordinates[i]
        dict_coordinates = dict.fromkeys(keys, "  ")
        list_coordinate_dictionaries.append(dict_coordinates)

    return list_coordinate_dictionaries


def print_grid(coordinates_dictionaries):
    """
    Function that prints the grid taking as a parameter a list of dictionaries
    with coordinates as keys and symbol to be printed as payloads.
    :param coordinates_dictionaries: list with dictionaries of coordinates with
     fired shots as payloads
    """
    print("  A B C D E F G H I J  ")

    for i in range(len(coordinates_dictionaries)):
        print(i, end=" ")
        for key in coordinates_dictionaries[i]:
            print(coordinates_dictionaries[i][key], end="")
        print(i)

    print("  A B C D E F G H I J  ")


def update_coord_dict(coordinates_dictionaries, coordinate, symbol):
    """
    Function that updates the list of dictionaries that is used as a parameter
    for printing the grid.
    :param coordinates_dictionaries: list of dictionaries with all coordinates
    and corresponding symbols to be printed
    :param coordinate: the coordinate the user shot at or a set of coordinates
    if the user sank a whole ship
    :param symbol: symbol to which the payload of the coordinate (or
    coordinates) in question should be updated
    :return: updated list of coordinates dictionaries
    """
    for i in coordinates_dictionaries:
        if isinstance(coordinate, set):  # if a whole ship was sank, all
            # coordinates of that ship need to have the symbol updated
            for single_coordinate in coordinate:
                if single_coordinate in i:
                    i[single_coordinate] = symbol
        elif coordinate in i:
            i[coordinate] = symbol

    return coordinates_dictionaries

def main():

    filename = input("Enter file name: ")

    # Read the file while performing error checks, the ships in the file
    # are used as objects to the class Ship and appended to a list of ships
    try:
        file = open(filename, mode="r")
        check_list = []  # to check for overlapping coordinates
        list_of_ships = []
        for line in file:
            line = line.rstrip()
            list_of_data = line.split(";")
            ship_type = list_of_data[0]
            set_of_coordinates = set()  # coordinates of individual ship
            for i in range(1, len(list_of_data)):
                coordinate = list_of_data[i]
                if coordinate in check_list:
                    # Check if the coordinate overlaps
                    print("There are overlapping ships in the input file!")
                    return
                elif coordinate[0] in ["A", "B", "C", "D", "E", "F", "G", "H",
                                       "I", "J"] and int(coordinate[1]) in \
                        range(0, 10) and len(coordinate) == 2:
                    # Check if the coordinate is legit
                    # Create a list of coordinates to input to the class Ship
                    check_list.append(coordinate)
                    set_of_coordinates.add(coordinate)
                else:
                    print("Error in ship coordinates!")
                    return
            list_of_ships.append(Ship(ship_type, set_of_coordinates))

    # print error message if cannot open file
    except OSError:
        print("File can not be read!")
        return

    coordinates_dictionaries = initialize_coordinates()
    shoot_list = []  # initialize a list of coordinates already shot at
    ships_sank = 0  # initialize number that counts the number of ships that sank
    flag = True
    print()
    print_grid(coordinates_dictionaries)

    while flag == True:
        print()
        coordinate = input("Enter place to shoot (q to quit): ")
        coordinate = coordinate.title()  # capitalize coordinate
        if coordinate in ["q", "Q"]:
            print("Aborting game!")
            flag = False
        else:
            if len(coordinate) != 2 or \
                    coordinate[0] not in ["A", "B", "C", "D", "E", "F", "G",
                                          "H", "I", "J"] or \
                    int(coordinate[1]) not in range(0, 10):
                print("Invalid command!")
            elif coordinate in shoot_list:
                # Check if the coordinate has already been shot at
                print("Location has already been shot at!")
            else:
                shoot_list.append(coordinate)

            new_symbol = "* "  # default for new symbol is *

            for ship in list_of_ships:
                if coordinate in ship.ship_coordinates():
                    ship_name = ship.ship_name()
                    ship.ship_hit(coordinate)
                    if ship.ship_sank() == True:
                        new_symbol = ship_name[0].title() + " "
                        ships_sank += 1
                        coordinate = ship.ship_coordinates()
                    else:
                        new_symbol = "X "

            coordinate_dictionaries = \
                update_coord_dict(coordinates_dictionaries, coordinate,
                                  new_symbol)

            print()
            print_grid(coordinates_dictionaries)

            if ships_sank == len(list_of_ships):
                print()
                print("Congratulations! You sank all enemy ships.")
                flag = False


if __name__ == "__main__":
    main()
