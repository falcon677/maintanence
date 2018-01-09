from argparse import ArgumentParser

def arg(*args, **kwargs):
    """Decorator for CLI args."""
    def _decorator(func):
        add_arg(func, *args, **kwargs)
        return func
    return _decorator


def add_arg(f, *args, **kwargs):
    """Bind CLI arguments to a shell.py `do_foo` function."""

    if not hasattr(f, 'arguments'):
        f.arguments = []

    # NOTE(sirp): avoid dups that can occur when the module is shared across
    # tests.
    if (args, kwargs) not in f.arguments:
        # Because of the sematics of decorator composition if we just append
        # to the options list positional options will appear to be backwards.
        f.arguments.insert(0, (args, kwargs))


@arg('server', metavar='<server>', help='Name or ID of server.')
@arg('host', metavar='<host>', help='Name or ID of target host.')
@arg('--password',
    dest='password',
    metavar='<password>',
    default=None,
    help="Set the provided password on the evacuated instance. Not applicable "
            "with on-shared-storage flag")
@arg('--on-shared-storage',
    dest='on_shared_storage',
    action="store_true",
    default=False,
    help='Specifies whether instance files located on shared storage')


def do_evacuate(cs, args):
    """Evacuate server from failed host to specified one."""
    print("---------------")
    for var in args:
        print var


if __name__ == "__main__":

    parser = ArgumentParser(
        #prog='nova',
        description="gemlllllllll",
        epilog='See "nova help COMMAND" '
               'for help on a specific command.',
        add_help=False,
    )

    parser.add_argument('-h', '--help',
        action='help',
        help='ddddddddddd',
    )
    arguments = getattr(do_evacuate, 'arguments', [])
    for (args, kwargs) in arguments:
        parser.add_argument(*args, **kwargs)
    args = parser.parse_args()
    print vars(args)
    do_evacuate('aa', vars(args))
