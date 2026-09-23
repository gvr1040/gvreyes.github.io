#!/usr/bin/env python3

# Name: Gray Reyes
# Date: 04/09/2026
# File: shortcut.py
# Course: NSSA221 - System Administration I
# Purpose: Create, delete, and report symbolic links on the user's Desktop.

import os
from pathlib import Path


# Return the Desktop path for the current user.
def get_desktop():
    return Path.home() / "Desktop"


# Clear the terminal screen.
def clear_screen():
    os.system("clear")


# Display the menu in a readable format.
def show_menu():
    desktop = get_desktop()

    print("======================================")
    print("       Symbolic Link Manager")
    print("======================================")
    print("Current Working Directory: " + os.getcwd())
    print("Desktop Directory: " + str(desktop))
    print()
    print("[1] Create a symbolic link")
    print("[2] Delete a symbolic link")
    print("[3] Generate a symbolic link report")
    print("[4] Quit")
    print("======================================")


# Search the system for files with the given name.
def find_matching_files(filename):
    matches = []

    for root, dirs, files in os.walk("/"):

        if root == "/proc" or "/proc/" in root:
            continue

        if root == "/sys" or "/sys/" in root:
            continue

        if root == "/dev" or "/dev/" in root:
            continue

        if filename in files:
            matches.append(Path(root) / filename)

    return matches


# Let the user choose a file if more than one match exists.
def choose_match(matches):
    if len(matches) == 1:
        return matches[0]

    print("\nMultiple files with that name were found:\n")

    number = 1
    for match in matches:
        print("[" + str(number) + "] " + str(match))
        number += 1

    while True:
        choice = input("\nPlease select the file you want to create a shortcut for: ")

        if choice.isdigit():
            position = int(choice)

            if position >= 1 and position <= len(matches):
                return matches[position - 1]

        print("Error: Invalid selection. Please enter a valid number.")


# Ask the user for a file path or filename.
def get_target_file():
    print("\nCreate a Symbolic Link")
    print("----------------------")
    print("You may enter either:")
    print("- the full path to a file")
    print("- or just the file name to search for it")
    print()

    user_input = input("Enter the file path or file name: ").strip()

    if user_input == "":
        print("Error: Input cannot be empty.")
        return None

    possible_path = Path(user_input).expanduser()

    if "/" in user_input or user_input[0] == "~":
        if possible_path.exists() and possible_path.is_file():
            return possible_path

        print("Error: That file path does not exist or is not a regular file.")
        print("\nReturning to Main Menu...")
        return None

    matches = find_matching_files(user_input)

    if len(matches) == 0:
        print("Error: No file with that name was found on the system.")
        print("\nReturning to Main Menu...")
        return None

    return choose_match(matches)


# Create a symbolic link on the Desktop.
def create_symbolic_link():
    desktop = get_desktop()

    if not desktop.exists():
        print("\nError: Desktop directory does not exist.")
        print("\nReturning to Main Menu...")
        return

    target_file = get_target_file()

    if target_file is None:
        return

    link_path = desktop / target_file.name

    if link_path.exists() or link_path.is_symlink():
        print("\nError: A file or symbolic link with that name already exists on the Desktop.")
        print("\nReturning to Main Menu...")
        return

    try:
        os.symlink(str(target_file), str(link_path))
        print("\nSuccess: Symbolic link created.")
        print("Link:   " + str(link_path))
        print("Target: " + str(target_file))
        print("\nReturning to Main Menu...")
    except OSError as error:
        print("\nError: Could not create the symbolic link.")
        print(str(error))
        print("\nReturning to Main Menu...")


# Collect all symbolic links on the Desktop.
def get_desktop_links():
    desktop = get_desktop()
    links = []

    if not desktop.exists():
        return links

    for name in os.listdir(desktop):
        item = desktop / name

        if item.is_symlink():
            links.append(item)

    return links


# Delete a symbolic link from the Desktop.
def delete_symbolic_link():
    print("\nDelete a Symbolic Link")
    print("----------------------")

    links = get_desktop_links()

    if len(links) == 0:
        print("No symbolic links were found on the Desktop.")
        print("\nReturning to Main Menu...")
        return

    print("\nSymbolic links on the Desktop:\n")

    number = 1
    for link in links:
        print("[" + str(number) + "] " + link.name)
        number += 1

    while True:
        choice = input("\nEnter the number of the symbolic link to delete: ").strip()

        if choice.isdigit():
            position = int(choice)

            if position >= 1 and position <= len(links):
                selected_link = links[position - 1]

                try:
                    selected_link.unlink()
                    print("\nSuccess: Deleted " + selected_link.name)
                    print("\nReturning to Main Menu...")
                except OSError as error:
                    print("\nError: Could not delete the symbolic link.")
                    print(str(error))
                    print("\nReturning to Main Menu...")

                return

        print("Error: Invalid selection. Please enter a valid number.")


# Print a report of all symbolic links on the Desktop.
def generate_report():
    print("\nSymbolic Link Report")
    print("--------------------")

    links = get_desktop_links()

    if len(links) == 0:
        print("No symbolic links were found on the Desktop.")
        print("Total symbolic links on Desktop: 0")
        print("\nReturning to Main Menu...")
        return

    count = 0

    for link in links:
        count += 1

        try:
            target_path = link.resolve()
        except OSError:
            target_path = "Broken link or target unavailable"

        print("Link Name:    " + link.name)
        print("Link Path:    " + str(link))
        print("Target Path:  " + str(target_path))
        print()

    print("Total symbolic links on Desktop: " + str(count))
    print("\nReturning to Main Menu...")


# Run the program.
def main():
    while True:
        clear_screen()
        show_menu()

        choice = input("\nEnter your choice: ").strip().lower()

        if choice == "1":
            clear_screen()
            create_symbolic_link()

        elif choice == "2":
            clear_screen()
            delete_symbolic_link()

        elif choice == "3":
            clear_screen()
            generate_report()

        elif choice == "4" or choice == "quit":
            print("\nGoodbye!")
            break

        else:
            print("\nError: Invalid menu option.")


if __name__ == "__main__":
    main()

