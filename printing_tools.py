import subprocess, os.path, sys, itertools

IS_UNIT_TEST = False

class PrintError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

class WinPrinter(object):
    def __init__(self):
        import win32print

    def list_printers(self):
        raise NotImplementedError()

    def print_file(self, filename, printer_name=None):
        raise NotImplementedError()

    def print_text(self, text, printer_name=None):
        raise NotImplementedError()

class UnixPrinter(object):
    def list_printers(self):
        lpstat_results = subprocess.check_output(['lpstat','-p'], universal_newlines=True)
        return [line.split()[1] for line in lpstat_results.split('\n') if line.startswith("printer")]

    def print_file(self, filename, printer_name=None):
        try:
            with open(filename):
                pass
        except (OSError, IOError) as err:
            raise PrintError("Error: %s"%str(err))
        popen_args = ['lpr']
        if printer_name:
            popen_args.append('-P%s'%printer_name)
        popen_args.append(filename)
        if IS_UNIT_TEST:
            return popen_args
        else:
            popen = subprocess.Popen(popen_args, stdin=subprocess.PIPE)
            popen.communicate(text)
            p.stdin.close()
        
    def print_text(self, text, printer_name=None):
        popen_args = ['lpr']
        if printer_name:
            popen_args.append('-P%s'%printer_name)
        if IS_UNIT_TEST:
            return popen_args
        else:
            popen = subprocess.Popen(popen_args, stdin=subprocess.PIPE)
            popen.communicate(text)
            p.stdin.close()

print_engine = None
if sys.platform.lower().startswith('win'):
    print_engine = WinPrinter()
else:
    print_engine = UnixPrinter()

def print_file(filename, printer_name=None):
    return print_engine.print_file(filename, printer_name)

def print_text(text, printer_name=None):
    return print_engine.print_text(text, printer_name)

def list_printers():
    return print_engine.list_printers()


