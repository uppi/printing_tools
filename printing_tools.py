# -*- coding: utf-8 -*-

import subprocess, os.path, sys, itertools, traceback

IS_UNIT_TEST = False
IS_WIN = sys.platform.lower().startswith('win')

if IS_WIN:
    import win32print
    import win32api

class PrintError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return unicode(self.msg)

class WinPrinter(object):
    def printers(self):
        return [name for (_, _, name, _) in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)]

    def print_file(self, filename, printer_name=None):
        try:
            with open(filename):
                pass
        except (OSError, IOError) as err:
            raise PrintError('Error: %s' % (err))
        exec_args = [0, 'print', filename]
        if not printer_name:
            printer_name = win32print.GetDefaultPrinterW()
        exec_args.append(u'/d:"{0}"'.format(printer_name))
        exec_args += ['.', 0]
        print "ARGS"
        for arg in exec_args:
            print arg
        print "END"
        if IS_UNIT_TEST:
            return exec_args
        win32api.ShellExecute(*exec_args)

    def print_text(self, text, printer_name=None):
        if not printer_name:
            printer_name = win32print.GetDefaultPrinterW()
        try:
            print printer_name
            printer = win32print.OpenPrinter(printer_name)
            try:
                job = win32print.StartDocPrinter(printer, 1, ('PrintText', None, 'RAW'))
                try:
                    win32print.StartPagePrinter(printer)
                    if not IS_UNIT_TEST:
                        win32print.WritePrinter(printer, text)
                    win32print.EndPagePrinter(printer)
                finally:
                    win32print.EndDocPrinter(printer)
            finally:
                win32print.ClosePrinter(printer)
        except Exception as err:
            traceback.print_exc()
            for elem in err:
                try:
                    print elem.decode("cp1251")
                except:
                    print elem
            if IS_UNIT_TEST:
                return False
            else:
                raise PrintError(unicode(err))
        return True

class UnixPrinter(object):
    def printers(self):
        lpstat_results = subprocess.check_output(['lpstat','-p'], universal_newlines=True)
        return [line.split()[1] for line in lpstat_results.split('\n') if line.startswith('printer')]

    def print_file(self, filename, printer_name=None):
        try:
            with open(filename):
                pass
        except (OSError, IOError) as err:
            raise PrintError('Error: %s' % unicode(err))
        popen_args = ['lpr']
        if printer_name:
            popen_args.append('-P%s' % printer_name)
        popen_args.append(filename)
        if IS_UNIT_TEST:
            return popen_args
        popen = subprocess.Popen(popen_args, stdin=subprocess.PIPE)
        popen.communicate(text)
        p.stdin.close()
        
    def print_text(self, text, printer_name=None):
        popen_args = ['lpr']
        if printer_name:
            popen_args.append('-P%s' % printer_name)
        if IS_UNIT_TEST:
            return popen_args
        popen = subprocess.Popen(popen_args, stdin=subprocess.PIPE)
        popen.communicate(text)
        p.stdin.close()

print_engine = None
if IS_WIN:
    print_engine = WinPrinter()
else:
    print_engine = UnixPrinter()

def print_file(filename, printer_name=None):
    return print_engine.print_file(filename, printer_name)

def print_text(text, printer_name=None):
    return print_engine.print_text(text, printer_name)

def printers():
    return print_engine.printers()