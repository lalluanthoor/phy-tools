import click
import os
import requests


class NetHelper(object):

    def __init__(self, config):
        self.config = config

    def download_file(self, url, target_file):
        if not str.startswith(target_file, self.config.dest_dir):
            target_file = os.path.join(self.config.dest_dir, target_file)
        if self.config.verbose:
            click.echo("Downloading file %s from url %s." % (target_file, url), file=self.config.log_file)
        response = requests.get(url)
        if response.status_code not in [200, "200"]:
            if self.config.verbose:
                click.echo("Download failed. Status %s." % response.status_code, file=self.config.log_file)
            raise Exception("Unable to download file from URL %s." % url)
        with open(target_file, "wb") as file_handle:
            if self.config.verbose:
                click.echo("Download completed. Writing to file %s." % target_file, file=self.config.log_file)
            file_handle.write(response.content)
        if self.config.verbose:
            click.echo("Download of %s completed." % target_file, file=self.config.log_file)
