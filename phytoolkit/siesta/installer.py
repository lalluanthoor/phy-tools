"""Install Siesta and dependencies."""
import os

import click

from phytoolkit.base.installer import BaseInstaller
from phytoolkit.exception.installationexception import InstallationException


class Directories:
    """Class for storing directories of all packages installed."""

    def __init__(self, config):
        self.base = config.dest_dir
        self.siesta = os.path.join(self.base, "siesta")
        self.openblas = os.path.join(self.base, "openblas")
        self.scalapack = os.path.join(self.base, "scalapack")

        self.siesta_doc = ""


class Versions:
    """Class for storing versions of all packages installed."""

    def __init__(self, config):
        self.siesta = config.siesta_version
        self.flook = ""
        self.zlib = ""
        self.hdf = ""
        self.netcdf_c = ""
        self.netcdf_fortran = ""

    @property
    def siesta_mini(self):
        """Return the major.minor version of Siesta."""
        return self.siesta.split("-")[0]

    @property
    def hdf_mini(self):
        """Return the major.minor version of HDF."""
        return ".".join(self.hdf.split(".")[:2])

    def __str__(self):
        return """Siesta: %s
Siesta Mini: %s
Flook: %s
ZLib: %s
HDF: %s
HDF Mini: %s
NetCDF C: %s
NetCDF Fortran: %s""" % (
            self.siesta, self.siesta_mini, self.flook, self.zlib, self.hdf, self.hdf_mini,
            self.netcdf_c, self.netcdf_fortran)


class SiestaInstaller(BaseInstaller):
    """Installs Siesta suite."""

    def __init__(self, config):
        super().__init__(config)
        self.required_os_packages = ["python", "curl", "unzip", "hwloc", "sysstat",
                                     "build-essential", "g++", "gfortran", "libreadline-dev",
                                     "m4", "xsltproc", "mpich", "libmpich-dev"]
        self.versions = Versions(config)
        self.dirs = Directories(config)
        self.dirs.siesta_doc = os.path.join(config.dest_dir, "siesta", "siesta-%s" %
                                            self.versions.siesta, "Docs")

    def pre_installation(self):
        """Pre-installation logic for Siesta"""
        os.makedirs(self.dirs.siesta)
        os.makedirs(self.dirs.openblas)
        os.makedirs(self.dirs.scalapack)
        self.osh.run_shell_command(["sudo", "chmod", "-R", "777", self.dirs.base])

        self.net.download_file(
            "https://ufpr.dl.sourceforge.net/project/openblas/v0.3.3/OpenBLAS%200.3.3%20version"
            ".tar.gz", os.path.join(self.dirs.openblas, "OpenBLAS.tar.gz"))
        self.net.download_file(
            "https://launchpad.net/siesta/%s/%s/+download/siesta-%s.tar.gz" % (
                self.versions.siesta_mini, self.versions.siesta, self.versions.siesta),
            os.path.join(self.dirs.siesta, "siesta-%s.tar.gz" % self.versions.siesta))
        archives_to_extract = {
            "OpenBLAS.tar.gz": self.dirs.openblas,
            "siesta-%s.tar.gz" % self.versions.siesta: self.dirs.siesta
        }
        for file in archives_to_extract:
            if not self.osh.extract_tar_file(file, archives_to_extract[file]):
                raise InstallationException("Unable to extract tar file %s" % file)
        self.populate_versions()
        self.console.verbose_info(self.versions.__str__())

        flook_url = "https://github.com/ElectronicStructureLibrary/flook/releases/download/v%s/flook-%s.tar.gz" % (
            self.versions.flook, self.versions.flook)
        flook_file = os.path.join(self.dirs.siesta_doc, "flook-%s.tar.gz" % self.versions.flook)
        self.net.download_file(flook_url, flook_file)

        zlib_url = "https://zlib.net/zlib-%s.tar.gz" % self.versions.zlib
        zlib_file = os.path.join(self.dirs.siesta_doc, "zlib-%s.tar.gz" % self.versions.zlib)
        self.net.download_file(zlib_url, zlib_file)

        hdf_url = "https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-%s/hdf5-%s/src/hdf5-%s.tar.bz2" % (
            self.versions.hdf_mini, self.versions.hdf, self.versions.hdf)
        hdf_file = os.path.join(self.dirs.siesta_doc, "hdf5-%s.tar.bz2" % self.versions.hdf)
        self.net.download_file(hdf_url, hdf_file)

        nc_url = "https://github.com/Unidata/netcdf-c/archive/v%s.tar.gz" % self.versions.netcdf_c
        nc_file = os.path.join(self.dirs.siesta_doc, "netcdf-c-%s.tar.gz" % self.versions.netcdf_c)
        self.net.download_file(nc_url, nc_file)

        nf_url = "https://github.com/Unidata/netcdf-fortran/archive/v%s.tar.gz" % self.versions.netcdf_fortran
        nf_file = os.path.join(self.dirs.siesta_doc,
                               "netcdf-fortran-%s.tar.gz" % self.versions.netcdf_fortran)
        self.net.download_file(nf_url, nf_file)

        for file in [flook_file, zlib_file, hdf_file, nc_file, nf_file]:
            if not self.osh.extract_tar_file(file.split("/")[-1], self.dirs.siesta_doc):
                raise InstallationException("Unable to extract tar file %s" % file)

    def installation(self):
        """Main installation logic."""
        self.console.verbose_success("Installation completed.")

    def post_installation(self):
        """Post installation steps including cleanup and path updates."""
        click.echo("Installation of Siesta suite completed.", file=self.config.log_file)
        click.echo(
            "Siesta binaries siesta, transiesta and tbtrans installed to /usr/local/bin.",
            file=self.config.log_file)

    def populate_versions(self):
        """Populate the version of dependent packages."""
        self.versions.flook = self.osh.run_shell_command(
            ["cat install_flook.bash | grep f_v= | cut -d'=' -f 2", ], cwd=self.dirs.siesta_doc,
            shell=True).strip()
        self.versions.zlib = self.osh.run_shell_command(
            ["cat install_netcdf4.bash | grep z_v= | cut -d'=' -f 2"], self.dirs.siesta_doc,
            shell=True).strip()
        self.versions.hdf = self.osh.run_shell_command(
            ["cat install_netcdf4.bash | grep h_v= | cut -d'=' -f 2"], self.dirs.siesta_doc,
            shell=True).strip()
        self.versions.netcdf_c = self.osh.run_shell_command(
            ["cat install_netcdf4.bash | grep nc_v= | cut -d'=' -f 2"], self.dirs.siesta_doc,
            shell=True).strip()
        self.versions.netcdf_fortran = self.osh.run_shell_command(
            ["cat install_netcdf4.bash | grep nf_v= | cut -d'=' -f 2"], self.dirs.siesta_doc,
            shell=True).strip()
