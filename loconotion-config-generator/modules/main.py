import sys
import argparse
import copy
import logging
from pathlib import Path
from modules.generator import Generator

log = logging.getLogger("loconotion-config-generator")

try:
        import colorama
        import toml

except ModuleNotFoundError as e:
        log.critical(f"ModuleNotFoundError:{e}. Please install the requirements with 'pip install -r requirements.txt'")

def get_args():
        argparser = argparse.ArgumentParser("Generate a loconotion config from Notion.so API"
        )
        argparser.add_argument(
            "meta_config_path",
            help = "The path of the config file for generating a loconotion config file. "
        )
        argparser.add_argument(
            "-v", "--verbose", action="store_true", help="Increase output log verbosity"
        )
        return argparser.parse_args()

def setup_logging(args):
    # set up some pretty logs
    log = logging.getLogger("loconotion-config-generator")
    log.setLevel(logging.INFO if not args.verbose else logging.DEBUG)
    log_screen_handler = logging.StreamHandler(stream=sys.stdout)
    log.addHandler(log_screen_handler)
    log.propagate = False
    try:
        LOG_COLORS = {
            logging.DEBUG: colorama.Fore.GREEN,
            logging.INFO: colorama.Fore.BLUE,
            logging.WARNING: colorama.Fore.YELLOW,
            logging.ERROR: colorama.Fore.RED,
            logging.CRITICAL: colorama.Back.RED,
        }

        class ColorFormatter(logging.Formatter):
            def format(self, record, *args, **kwargs):
                # if the corresponding logger has children, they may receive modified
                # record, so we want to keep it intact
                new_record = copy.copy(record)
                if new_record.levelno in LOG_COLORS:
                    new_record.levelname = "{color_begin}{level}{color_end}".format(
                        level=new_record.levelname,
                        color_begin=LOG_COLORS[new_record.levelno],
                        color_end=colorama.Style.RESET_ALL,
                    )
                return super(ColorFormatter, self).format(new_record, *args, **kwargs)

        log_screen_handler.setFormatter(
            ColorFormatter(
                fmt="%(asctime)s %(levelname)-8s %(message)s",
                datefmt="{color_begin}[%H:%M:%S]{color_end}".format(
                    color_begin=colorama.Style.DIM, color_end=colorama.Style.RESET_ALL
                ),
            )
        )
    except ModuleNotFoundError as identifier:
        pass

    return log

def init_generator(args, log):
    if Path(args.meta_config_path).is_file():
        with open(args.meta_config_path, encoding="utf-8") as f:
            parsed_meta_config = toml.loads(f.read())
            log.info("Initialising generator with meta configuration file")
            log.debug(parsed_meta_config)
            generator = Generator(meta_config=parsed_meta_config, args=vars(args))
            generator.generate()

    else:
        log.critical(f"meta_config_file '{args.meta_config_path}' does not exist")
        raise FileNotFoundError(args.meta_config_path)

    return generator
