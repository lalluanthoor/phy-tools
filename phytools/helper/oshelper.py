import click
import os
import platform
import subprocess


class OsHelper(object):

    def __init__(self, config):
        self.config = config
        self.current_dir = os.getcwd()
        self.system = platform.system()
        self.release = platform.release()
        self.version = platform.version()

    def get_as_string(self):
        return "%s - %s - %s" % (self.system, self.release, self.version)

    def validate(self):
        supported_platforms = ["Linux", ]
        if self.config.verbose:
            click.echo("Validating against supported platforms %s." % ", ".join(supported_platforms),
                       file=self.config.log_file)
        if self.system not in supported_platforms:
            raise Exception("Unsupported platform %s" % self.system)
        if self.config.verbose:
            click.echo("Checking for variant 'Ubuntu' in version.", file=self.config.log_file)
        if "Ubuntu" not in self.version:
            raise Exception("Unsupported variant %s. Only 'Ubuntu' supported." % self.version)

        if not os.path.exists(self.config.dest_dir):
            os.makedirs(self.config.dest_dir)

    def run_shell_command(self, command, cwd=""):
        if cwd == "":
            cwd = self.config.dest_dir
        if self.config.verbose:
            click.echo("Running command %s from %s." % (" ".join(command), cwd), file=self.config.log_file)
        output = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.config.log_file.write(output.stdout.decode("UTF-8"))
        self.config.log_file.write(output.stderr.decode("UTF-8"))
        if self.config.verbose:
            click.echo("Command exited with status %s." % output.returncode, file=self.config.log_file)
        return output.returncode == 0

    def install_packages(self, packages, cwd=""):
        if self.config.verbose:
            click.echo("Installing packages %s." % ", ".join(packages), file=self.config.log_file)
        return self.run_shell_command(["sudo", "apt", "install", "-y"] + packages, cwd)

    def extract_tar_file(self, file, cwd=""):
        if self.config.verbose:
            click.echo("Extracting tar file %s." % file, file=self.config.log_file)
        return self.run_shell_command(["tar", "xf", file], cwd)

    def write_file(self, file, content):
        if self.config.verbose:
            click.echo("Writing contents\n %s \nto file %s." % (content, file), file=self.config.log_file)
        with open(file, "w") as file_handle:
            file_handle.write(content)

    def append_file(self, file, content):
        if self.config.verbose:
            click.echo("Appending contents\n %s \nto file %s." % (content, file), file=self.config.log_file)
        with open(file, "a") as file_handle:
            file_handle.write(content)
