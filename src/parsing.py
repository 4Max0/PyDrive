import argparse

class Parser:

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description='parses the input to PyDrive')
        subparser = self.parser.add_subparsers(dest='command', required=True)

        # init parser ---------------------------------------------------------------------------------
        p_init = subparser.add_parser('init', help='init the pydrive system')

        # ---------------------------------------------------------------------------------------------
        # target parser
        p_target = subparser.add_parser('target', help='This tell the programm that we are trying to interact with a target')
        p_target_sub = p_target.add_subparsers(dest='subcommand', required=True)

        # Parser for add function of target
        p_target_add = p_target_sub.add_parser('add', help='parses the add function of target')
        p_target_add.add_argument('-i', '--init', action='store_true', help='init flag for target add if you need to initialise the the drive location')
        p_target_add.add_argument('name', type=str, help='name of the drive we want to add')
        p_target_add.add_argument('location', type=str, help='Location of the drive we want to add') # this is a path, we still do not have a support for external locations 

        # Parser for remove function of target
        p_target_remove = p_target_sub.add_parser('remove', help='parses the remove function of target')
        p_target_remove.add_argument('-d', '--delete', action='store_true', help="delete flag for target add if want to delete the drive and it's contents")
        p_target_remove.add_argument('name', type=str, help='name of the drive we want to remove')
        
        # Parser for list function of target
        p_target_list = p_target_sub.add_parser('list', help='parses the list function of target')
        p_target_list.add_argument('-n','--numbered', action='store_true', help='if you want the output to be numbered')

        # Parser for switch function of target
        p_target_switch = p_target_sub.add_parser('switch', help='parses the switch function of target')
        p_target_switch.add_argument('name', type=str, help='name of the drive we want to switch to')
