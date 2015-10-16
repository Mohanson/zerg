# -*- coding: utf-8 -*-

import os
import winreg
import re

from saika.utils import Paramscheck, Accept


assert os.name == 'nt'


@Paramscheck(iter=Accept.Lambda('type(_) in [str, list, tuple]'))
def trans_to_strandard_string(input):
    if type(input) == str:
        if input[-1:] != ';':
            input += ';'
    else:
        input = ';'.join(input) + ';'
    return input


def trans_string_to_list(string, symbol=';'):
    return [i.strip() for i in string.split(symbol) if i]


class EnvironmentPath:
    def __init__(self, env):
        self.env = env
        env_path_value = self.env.get('path')
        env_path_value_list = trans_string_to_list(env_path_value)
        env_path_value_list.sort()
        self.paths = env_path_value_list

    @classmethod
    def from_user(cls):
        return EnvironmentPath(Environment.from_user())

    @classmethod
    def from_system(cls):
        return EnvironmentPath(Environment.from_system())

    @property
    def paths_string(self):
        return ';'.join(self.paths) + ';'

    def cleanup(self):
        """cleanup not exist path info"""
        for path in set(self.paths):
            try:
                tpath = self.env._replace_constant(path)
            except WindowsError:
                tpath = None
            if not tpath or not os.path.isdir(tpath):
                self.paths.remove(path)
        self.env.set('path', self.paths_string)

    def enums(self, truth=False):
        if truth:
            return [self.env._replace_constant(i) for i in self.paths]
        else:
            return self.paths

    def add(self, path):
        path = self.env._replace_constant(path)
        if not os.path.isdir(self.env._replace_constant(path)):
            raise FileNotFoundError
        self.paths.append(path)
        self.paths.sort()
        self.env.set('path', self.paths_string)

    def delete(self, index):
        self.paths.pop(index)
        self.env.set('path', self.paths_string)


class Environment:
    @Paramscheck(scope=Accept.Lambda('_.lower() in ["user", "system"]'))
    def __init__(self, scope):
        if scope == 'user':
            self.root = winreg.HKEY_CURRENT_USER
            self.subkey = 'Environment'
        else:
            self.root = winreg.HKEY_LOCAL_MACHINE
            self.subkey = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'

    @classmethod
    def from_user(cls):
        return Environment('user')

    @classmethod
    def from_system(cls):
        return Environment('system')

    def enums(self, truth=False):
        key = winreg.OpenKey(self.root, self.subkey, 0, winreg.KEY_READ)
        return_list = list()
        try:
            index = 0
            while True:
                name, value, type = winreg.EnumValue(key, index)
                if truth:
                    value = self._replace_constant(value)
                return_list.append((name, value, type))
                index += 1
        except WindowsError:
            pass
        finally:
            winreg.CloseKey(key)
        return return_list

    def get(self, name, truth=False):
        key = winreg.OpenKey(self.root, self.subkey, 0, winreg.KEY_READ)
        try:
            value, _ = winreg.QueryValueEx(key, name)
        except WindowsError as e:
            raise e
        finally:
            winreg.CloseKey(key)
        if truth:
            value = self._replace_constant(value)
        return value

    def set(self, name, value):
        key = winreg.OpenKey(self.root, self.subkey, 0, winreg.KEY_ALL_ACCESS)
        try:
            winreg.SetValueEx(key, name, 0, winreg.REG_EXPAND_SZ, value)
            return True
        except WindowsError as e:
            raise e
        finally:
            winreg.CloseKey(key)

    def delete(self, name):
        key = winreg.OpenKey(self.root, self.subkey, 0, winreg.KEY_ALL_ACCESS)
        try:
            winreg.DeleteValue(key, name)
        except WindowsError as e:
            raise e
        finally:
            winreg.CloseKey(key)

    def _replace_constant(self, input):
        """if there is constants in string, reploace the constants with it's truth value

        Usage example:

            path = '%JAVA_HOMT%/bin;'
            _replace_constant(path) == 'C:/programs/java/bin'
        """
        rule = re.compile('%(?P<var>.*?)%')
        matcher = rule.findall(input)
        for i in matcher:
            try:
                value = self.get(i)
            except FileNotFoundError:
                continue
            else:
                input = input.replace('%%%s%%' % i, self._replace_constant(value))
        return input