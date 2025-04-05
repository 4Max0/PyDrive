import os
import sys
import stat
import pathlib
import shutil
from DatabaseInfo import DatabaseInfo
from Database import Database
from parsing import Parser



# helper functions --------------------------------------------------------------------------------
def pydrive_init_check() -> None:
    # Check if already initialised
    if not os.path.exists('drive.db') and not os.path.exists('.temp'):
        print("Not initialised.\nCancelling...")
        sys.exit(-1)



def rm_dir_readonly(func, path, _) -> None:
    # give write rights on the folder and file
    # call the function again
    os.chmod(path, stat.S_IWRITE)
    func(path)



# program functions -------------------------------------------------------------------------------
def pydrive_init() -> None:
    # Check if already initialised
    if os.path.exists('drive.db') and os.path.exists('.temp'):
        print("Already initialised\nCancelling...")
        sys.exit(-1)
    # create the empty file where the drive locations are gonna saved
    
    dbi = DatabaseInfo()
    dbi.config_init()
    del dbi
    # directory for temporary files
    
    try:
        os.mkdir('.temp')
    except Exception as e:
        print(f"An error occured: {e}\nCancelling...")
        os.remove('drive.db')
        sys.exit(-1)
    sys.exit(0)



def pydrive_target_add() -> None:
    # Ask for confirmation of user
    print("You are about to initialise a new Drive instance. This will initialise a new drive instance at the target you provided.\nStill willing to Proceed? (Type 'YES' if you want to change the target)")
    answer = input().strip()
    if answer != 'YES':
        print('Cancelling request')
        sys.exit(1)

    # check if initialised
    pydrive_init_check()

    # check if provided path already exists
    dir_path = pathlib.Path(sys.argv[4])
    if os.path.exists(dir_path):
        print("Provided destination path already existent\nCancelling...")
        sys.exit(-1)

    # create folder where data is gonna get saved
    db_path = dir_path / '.drive'
    db_path.mkdir(parents=True, exist_ok=True)

    db = Database()
    # init the database
    db.init_database(db_path)
    del db

    # write the given directorypath into the info database  
    dbi = DatabaseInfo()
    dbi.config_add(sys.argv[3], str(dir_path))
    del dbi
    print("Finished.")                



# Safety on fail should be added
def pydrive_target_remove() -> None:
    # Ask for confirmation of user
    print("You are about to delete a drive. This will DELETE YOUR DATA PERMANENTLY IN THAT DRIVE.\nYOU WILL NOT BE ABLE TO RECOVER YOUR DATA.\nStill willing to Proceed? (Type 'YES' if you want to delete the target)")
    answer = input().strip()
    if answer != 'YES':
        print('Cancelling request')
        sys.exit(-1)
    
    # check if initialised
    pydrive_init_check()

    # fetch data of provided drive
    dbi = DatabaseInfo()
    data = dbi.config_fetch_specific(sys.argv[3])

    if not data:
        print("Drive was not found.\nCancelling...")
        sys.exit(-1)

    pwd = dbi.get_password(data[4])
    dbi.encryption.load_password(pwd)
    path_decrypted = dbi.encryption.decrypt_data(data[2])

    # delete the path of provided drive
    try:
        shutil.rmtree(path_decrypted, onexc=rm_dir_readonly)
    except Exception as e:
        print("Drive couldn't be deleted.\nCancelling...")
        sys.exit(-1)
    
    # delete reference from drive
    dbi.config_remove(data[0])
    if dbi.config_fetch_specific(data[0]):
        print("Error removing drive.\nCancelling...")
        sys.exit(-1)
    
    print("Finished.")
    sys.exit(0)



def pydrive_target_list() -> None:
    # check if initialised
    pydrive_init_check()

    # fetch all the drives in the database and use the pretty print method
    dbi = DatabaseInfo()
    dbi.pretty_print_names()
    sys.exit(0)



def pydrive_target_switch() -> None:
    # check if init
    pydrive_init_check()

    # get the current (if it exists) and the new current
    dbi = DatabaseInfo()
    current = dbi.config_fetch_current()
    new_current = dbi.config_fetch_specific(sys.argv[3])

    # we switch the current if it exists else we exit
    if new_current:
        dbi.config_switch_current(new_current[1])
    else:
        print(f'Drive was not found under the name: {sys.argv[3]}')
        sys.exit(-1)
    # if there is a current that already existed, we set the current value to 0
    if current:
        dbi.config_switch_current(current[1])    

    # WE exit normally
    print(f'Switched to {new_current[1]}')
    sys.exit(0)



# main --------------------------------------------------------------------------------------------
def main() -> None:

    parser1 = Parser()

    args = parser1.parser.parse_args()
    if args.command == 'init':
        pydrive_init()
    elif args.command == 'target':
        if args.subcommand == 'add':
            pydrive_target_add()
        elif args.subcommand == 'remove':
            pydrive_target_remove()
        elif args.subcommand == 'list':
            pydrive_target_list()
        elif args.subcommand == 'switch':
            pydrive_target_switch()
        else:
            print('subcommand is not viable')
    else:
        print('Invalid command or missing argument')
        sys.exit(1)



if __name__ == '__main__':
    main()