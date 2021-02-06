import click


class ConsoleHelper:

    def __init__(self, log_file, verbose):
        self.log_file = log_file
        self.verbose = verbose

    def print(self, message, fg_color):
        click.secho(message, file=self.log_file, fg=fg_color)

    def verbose_print(self, message, fg_color):
        if self.verbose:
            self.print(message, fg_color)

    def info(self, message):
        self.print(message, 'blue')

    def verbose_info(self, message):
        self.verbose_print(message, 'blue')

    def success(self, message):
        self.print(message, 'green')

    def verbose_success(self, message):
        self.verbose_print(message, 'green')

    def error(self, message):
        click.secho(message, file=self.log_file, fg='red', err=True)

    def verbose_error(self, message):
        if self.verbose:
            click.secho(message, file=self.log_file, fg='red', err=True)
