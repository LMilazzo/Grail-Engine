def find_args(args: dict, arg_map: dict):
    
    args_lower = {k.lower(): v for k, v in args.items()}

    norm = {}

    for canonical, aliases in arg_map.items():
        value = None
        for key in aliases:
            if key in args_lower:
                value = args_lower[key]
                break

        if value is None:
            raise ValueError(
                f"Missing required argument '{canonical}'. "
                f"Expected one of {aliases}. Got {list(args.keys())}"
            )
    
        norm[canonical] = value

    return norm