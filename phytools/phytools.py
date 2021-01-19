"""Main class for handling the CLI commands and groups."""
import click


class Config:
    """Configuration class for storing installation configuration."""

    def __init__(self):
        self.verbose = False


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option("--verbose", is_flag=True)
@pass_config
def cli(config, verbose):
    """Command line utility to manage the most commonly used tools for material simulations."""
    config.verbose = verbose


@cli.group()
@click.option("--dest-dir", type=click.Path(), default=".",
              help="Destination directory where the tool should be "
                   "installed.")
@click.option("--log-file", type=click.File("w"), default="-",
              help="File to store the installation log.")
@pass_config
def install(config, dest_dir, log_file):
    """Install a simulation tool on your system."""
    config.dest_dir = dest_dir
    config.log_file = log_file


@install.command()
@click.option("--vasp-source", type=click.Path(), default=".",
              help="Path to vasp.5.4.4.tar.gz file.")
@pass_config
def vasp(config, vasp_source):
    """Installs the Vienna Ab-initio Simulation Package. We currently support VASP
    installation using MPICH library only. The source of VASP is not bundled due to licence
    restrictions. Please obtain a copy of vasp-5.4.4.tar.gz file
    and provide the path as configuration."""
    config.vasp_source = vasp_source
    from phytools.vasp.install import Installer
    vasp_installer = Installer(config)
    vasp_installer.install()
    click.echo("Installation of VASP completed.", file=config.log_file)
    click.echo("VASP binaries 'vasp_std', 'vasp_gam' and 'vasp_ncl' installed.",
               file=config.log_file)
    click.echo("Run 'source ~/.bashrc' or open a new terminal to start using VASP.",
               file=config.log_file)
