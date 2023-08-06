#! /usr/bin/env python3
import argparse
import os
import shutil
import sys

other_loc = "/media/merk/Internal_SSD/Shared/Games/Yuzu/nand.bac/user/save/0000000000000000"

shared_nand_loc = "/media/merk/Internal_SSD/Shared/Games/Yuzu/nand/user/save/0000000000000000"
linux_nand_file_loc = "/home/merk/snap/yuzu/common/.local/share/yuzu/nand/user/save/0000000000000000"

linux_test_nand_loc = "/home/merk/YUZU TEST/LINUX_NAND_TEST/nand/user/save/0000000000000000"
yuzu_shared_nand_loc = "/home/merk/YUZU TEST/YUZU_SHARED_TEST/nand/user/save/0000000000000000"

ubuntu = linux_test_nand_loc
shared_drive = yuzu_shared_nand_loc


def handle_prints(loc):
    fixed_loc = loc.split("/")
    loc_part_1 = fixed_loc[-2]
    loc_part_2 = fixed_loc[-1]
    fixed_loc = "/".join([loc_part_1, loc_part_2])
    return fixed_loc


def compare_file_names(shared: list, unshared: list):
    for file_name in shared:
        if file_name not in unshared:
            return False
    return True


def check_for_files(files: list):
    if len(files) > 0:
        return True


def get_sub_dirs(the_dirname, number_wanted):
    num = number_wanted * -1
    return "/".join(the_dirname.split("/")[num:])


def compare_dir_names(shared: str, unshared: str):
    last_2_unshared_loc_dirs = get_sub_dirs(shared, 2)
    last_2_shared_loc_dirs = get_sub_dirs(unshared, 2)

    if last_2_shared_loc_dirs == last_2_unshared_loc_dirs:
        for i in range(2):
            print()
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.")
        print("================= DIRS MATCH ===================")
        print('last 2 unshared: ', last_2_unshared_loc_dirs)
        print('last 2 shared: ', last_2_shared_loc_dirs)
        print("^^^^^^^^^^^^^^^^^ DIRS MATCH ^^^^^^^^^^^^^^^^^^^")
        print()

        return True
    return False


def check_match(shared_files, shared_path, unshared_files, unshared_path):
    if compare_file_names(shared_files, unshared_files) and compare_dir_names(shared_path, unshared_path):
        return True
    return False


def get_first_uncommon_paths(path1: str, path2: str):
    path1 = path1.split("/")
    path2 = path2.split("/")
    word1 = ""
    word2 = ""

    for num, word in enumerate(path1):
        word1 = word
        word2 = path2[num]
        if word1 != word2:
            break

    return word1, word2


def update_shared_loc(shared_loc, unshared_loc, unshared_files):
    main_dir1 = None
    main_dir2 = None
    for file in unshared_files:
        unshared_file_dest = os.path.join(unshared_loc, file).strip()
        shared_file_dest = os.path.join(shared_loc, file).strip()

        u_root, s_root = get_first_uncommon_paths(unshared_file_dest, shared_file_dest)
        u_dir = get_sub_dirs(unshared_file_dest, 2)
        s_dir = get_sub_dirs(shared_file_dest, 2)

        u_file_dest = f"{u_root}.../{u_dir}"
        s_file_dest = f"{s_root}.../{s_dir}"
        if main_dir1 is None:
            main_dir1 = u_root
        if main_dir2 is None:
            main_dir2 = s_root

        print(f"Moving: {u_file_dest} >> {s_file_dest}")

        # ================================================================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # shutil.move(unshared_file_dest, shared_file_dest)
        # shutil.copy(shared_file_dest, unshared_file_dest)
        # ================================================================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    print(f"Finished Moving {main_dir1} to {main_dir2}")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.")


def sift_dirs(shared, unshared):
    for shared_loc, dirs, shared_files in shared:
        file_info = check_for_files(shared_files)
        if file_info:
            matches = sift_dir2(unshared, shared_files, shared_loc)


def sift_dir2(unshared_path, shared_files, shared_loc):
    unshared_walker = os.walk(unshared_path)
    for loc, dirs, files in unshared_walker:
        file_info = check_for_files(files)
        if file_info:
            if check_match(shared_files, shared_loc, files, loc):
                update_shared_loc(shared_loc, loc, files)

    return True


def handle_choice(choices_to_chose):
    chosen = False

    option = ""
    while not chosen:

        for num, choice_ in enumerate(choices_to_chose):
            print(f"{num + 1}. {choice_}")

        choice_ = input("Please choose one of the options above using a number.\n\n")
        try:
            choice_ = int(choice_)
        except ValueError:
            print("That was not a number and so is not a valid entry.\n\n")
            continue

        if choice_ > len(choices_to_chose) or choice_ < 1:
            print(f"The number chosen must be between 1 and {len(choices_to_chose)}. Please try again.\n\n")
            continue

        option = choices_to_chose[choice_ - 1]
        chosen = True
    return option


def handle_dirs():
    # start_dir = input("Please enter the path to the os directory.")
    # end_dir = input("Please enter the path to the backup directory.")
    start_dir = linux_test_nand_loc
    end_dir = yuzu_shared_nand_loc

    if start_dir is None:
        start_dir = input("Please enter the path to the root directory of all the files that will be backed up.\n\n")
    if end_dir is None:
        end_dir = input("Please enter the path to the root directory of all the files you want to update.\n\n")

    return start_dir, end_dir


if __name__ == "__main__":
    starting_dir, update_dir = handle_dirs()
    print(starting_dir)
    print(update_dir)
    print()

    correct = input("Are you sure these are the correct locations? (y/n)\n\n")
    if correct:
        choices = ['Backup', 'Recover']
        choice = handle_choice(choices)
        print(f"Choice: ", choice)

        if choice == choices[0]:
            print("UPDATING: ", update_dir)
            sift_dirs(os.walk(update_dir), starting_dir)
        if choice == choices[1]:
            print("UPDATING: ", starting_dir)
            sift_dirs(os.walk(starting_dir), update_dir)
        else:
            Exception("An unavailable choice was given for unexpected reasons. Exiting now.")
            exit(1)
