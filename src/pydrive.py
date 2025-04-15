from parsing import Parser
from pydrive_manager import PyDriveManager

# main --------------------------------------------------------------------------------------------
def main() -> None:

    parser1 = Parser()
    args = parser1.parser.parse_args()

    PDM = PyDriveManager(args)                                               # we still need to change the user input 

    if args.command == 'init':
        PDM.pydrive_init()
    elif args.command == 'target':
        if args.subcommand == 'add':
            PDM.pydrive_target_add(args.init)                           # add flags integration
        elif args.subcommand == 'remove':
            PDM.pydrive_target_remove()                                 # add flags integration
        elif args.subcommand == 'list':                                 
            PDM.pydrive_target_list()                                   # add flags integration
        elif args.subcommand == 'switch':
            PDM.pydrive_target_switch(args)
        else:
            print('subcommand is not viable')
    else:
        print('Invalid command or missing argument. Try --help')
        sys.exit(1)



if __name__ == '__main__':
    main()