#!/usr/bin/env python
from argparse import ArgumentParser

import matplotlib.pyplot as plt

from config import read_config
from electrode import Electrode, Ink, Catalyst, Solvent
from experiment import Experiment
from reader import read_directory


def get_args(argv=''):
    parser = ArgumentParser()
    # argument definition
    parser.add_argument('configfile', nargs='?', default='config.ini')
    # read arguments
    if argv:
        if isinstance(argv, str):
            argv = argv.split()
        elif not hasattr(argv, '__iter__'):
            raise ValueError(f'argv must be iterable.')
        args = parser.parse_args(argv)
    else:
        args = parser.parse_args()
    return args


def get_electrode(config):
    catalyst = Catalyst(name=config.catalyst.name,
                        mass=config.ink.catalyst_mass,
                        active_center_name=config.catalyst.active_metal,
                        active_center_percentage=config.catalyst.active_metal_percentage,
                        support_name=config.catalyst.support)

    solvent = Solvent(name=config.ink.solvent, volume=config.ink.solvent_volume)

    ink = Ink(catalyst, solvent)

    catalyst_sample = ink.sample(volume=config.electrode.ink_volume_deposited)

    electrode = Electrode(catalyst=catalyst_sample,
                          area=config.electrode.get('area'),
                          diameter=config.electrode.get('diameter'))
    return electrode


def get_data(config):
    data = read_directory(directory=config.general.path,
                          extension=config.general.ext,
                          delimiter=config.general.delimiter,
                          filenames=config.general.filenames)
    return data


def run(argv=''):
    args = get_args(argv)

    config = read_config(args.configfile)

    electrode = get_electrode(config)
    data = get_data(config)

    experiment = Experiment(data=data,
                            electrode=electrode,
                            analysis_params=config.analysis)

    return experiment


if __name__ == '__main__':
    res = run()
    print(res)
    plt.show()
