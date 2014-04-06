#!/usr/bin/python
# coding=utf-8

from __future__ import division, print_function, unicode_literals
import logging


class InfoUpdater(object):
    def __init__(self, experiment, monitors=None):
        self.ex = experiment
        self.monitors = monitors if monitors is not None else dict()

    def __call__(self, epoch, net, training_errors, validation_errors, **_):
        info = self.ex.description['info']

        info['epochs_needed'] = epoch
        info['training_errors'] = training_errors
        info['validation_errors'] = validation_errors
        if 'nr_parameters' not in info:
            info['nr_parameters'] = net.get_param_size()

        if self.monitors and 'monitor' not in info:
            monitors = {}
            for mon_name, mon in self.monitors.items():
                if not hasattr(mon, 'log') or len(mon.log) == 0:
                    continue

                if len(mon.log) == 1:
                    log_name = mon.log.keys()[0]
                    monitors[mon_name + '.' + log_name] = mon.log[log_name]
                else:
                    monitors[mon_name] = mon.log

            info['monitor'] = monitors

        self.ex._emit_info_updated()


def create_basic_stream_logger(name, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers = []
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

NO_LOGGER = logging.getLogger('ignore')
NO_LOGGER.disabled = 1