from argparse import ArgumentParser, Namespace
from typing import Dict, Any, Union, get_args

import yaml

__all__ = ["ConfigParser", "config_type"]
config_type = Dict[str, Any]


class ConfigParser:
    """
    Class responsible for parsing yaml config files and updating them if arguments are specified
    """
    def __init__(self, config_input: str):
        try:
            with open(config_input, 'r') as config_file:
                self._initial_config: config_type = yaml.load(config_file, Loader=yaml.FullLoader)
        except FileNotFoundError:
            self._initial_config: config_type = yaml.load(config_input, Loader=yaml.FullLoader)
        self._parser: ArgumentParser = ArgumentParser()
        self._config_arg_type = Union[str, int, float, bool]

    def parse_args(self, log_changes: bool = True) -> config_type:
        """
        Helper function for working with  configs.

        1. Loads yaml config from given 'config_input' within class initialization: string config or path to yaml file
        2. Parses arguments given to the script using argparse and if there are any replaces the corresponding values
            within config
        3. Logs/prints values changed by the user's input

        Note:
            configs can be written on-the-fly of the type: str, int, float, bool. Nested values are not supported now.

        Parameters
        ----------
        log_changes: bool, default True
            whether to print which values are updated (if so) within config file

        Returns
        -------
        config: Dict[str, Any]
            original if there weren't any arguments overwritten, updated one otherwise
        """
        initial_config: config_type = self._read_current_args(current_config=self._initial_config)
        config: config_type = self._merge_new_args(current_config=initial_config, log_changes=log_changes)

        return config

    def _read_current_args(self, current_config: config_type) -> config_type:
        config: config_type = current_config.copy()

        for key, value in config.items():
            if isinstance(value, get_args(self._config_arg_type)):
                not_bool: bool = not isinstance(value, bool)
                eval_: bool = "eval" in str(value)
                if eval_:
                    value = eval(value.replace("eval", ""))
                    config[key] = value
                self._parser.add_argument(
                    f"--{key}",
                    help=f"{key}, default value: {value}",
                    type=type(value) if not_bool else ConfigParser._str2bool
                )

        return config

    def _merge_new_args(self, current_config: config_type, log_changes: bool = True) -> config_type:
        config: config_type = current_config.copy()
        args: Namespace = self._parser.parse_args()
        arg_type = self._config_arg_type

        changed_values: Dict[str, arg_type] = {}
        max_arg_len: int = 0
        for arg, value in args.__dict__.items():
            if value is not None and value != config[arg]:
                config[arg]: arg_type = value
                changed_values[arg]: arg_type = value
                _len: int = len(arg)
                if max_arg_len:
                    max_arg_len: int = _len if _len > max_arg_len else max_arg_len
                else:
                    max_arg_len: int = _len

        if changed_values and log_changes:
            print("Running with altered default values:")
            for key, value in changed_values.items():
                print(f"\t{f'{key}:':{max_arg_len + 1}} {value}")

        return config

    @staticmethod
    def _str2bool(v: Union[str, bool]) -> bool:
        """
        Parse input string value to boolean
        """
        if isinstance(v, bool):
            return v
        if v.lower() in ("yes", "true", "t", "y", "1"):
            return True
        elif v.lower() in ("no", "false", "f", "n", "0"):
            return False
        else:
            raise ValueError("Boolean value expected")
