import argparse
import pathlib as pl
import toml
import typing as tp
import tempfile

from stests.core.utils import args_validator
from stests.core.utils import env
from stests.core.utils import cli as utils
from sh.scripts.svc_utils import remote_node_ssh_copy
from sh.scripts.svc_utils import remote_node_ssh_invoke

class Semver(tp.NamedTuple):
    major: int
    minor: int
    patch: int

    def snake_str(self) -> str:
        return f'{self.major}_{self.minor}_{self.patch}'

    def dotted_str(self) -> str:
        return f'{self.major}.{self.minor}.{self.patch}'

def push_update_to_node(
    ssh_user: str,
    ssh_host: str,
    ssh_key_path: pl.Path,
    semver: Semver,
    local_bin_repo_dir: pl.Path,
    local_cfg_repo_dir: pl.Path,
    activation_era: int,
    public_address: str=None,
    public_port: int=35000,
    remote_bin_repo_dir: pl.Path=pl.Path('/var/lib/casper/bin'),
    remote_cfg_repo_dir: pl.Path=pl.Path('/etc/casper'),
):
    if not public_address:
        utils.log(f'Using SSH address as public address ({ssh_host})')
        public_address = ssh_host

    semver_snake_str = semver.snake_str()
    semver_dotted_str = semver.dotted_str()

    local_bin_dir = local_bin_repo_dir / semver_snake_str
    local_cfg_dir = local_cfg_repo_dir / semver_snake_str

    # Construct the expected remote repo paths to copy the new version dirs to.
    # A "repo dir" is a directory that contains subdirs of the form "X_Y_Z",
    # where X, Y, Z are major, minor, patch numbers, respectively.
    utils.log(f'Remote target bin repo dir `{remote_bin_repo_dir}`')
    utils.log(f'Remote target cfg repo dir `{remote_cfg_repo_dir}`')

    # Copy over casper-node binary dir.
    utils.log('Copying over casper-node binary')
    remote_node_ssh_copy(
        source_path=local_bin_dir,
        ssh_user=ssh_user,
        ssh_host=ssh_host,
        target_dir=remote_bin_repo_dir,
        ssh_key_path=ssh_key_path,
    )

    # Need to edit some config files, so create a temp dir.
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir = pl.Path(tmp_dir)

        tmp_semver_dir = tmp_dir / semver_snake_str
        tmp_semver_dir.mkdir()

        # Edit node config.
        utils.log('Customizing `config.toml`')
        config_toml = toml.load(local_cfg_dir / 'config-example.toml')

        config_toml['network']['public_address'] = f'{public_address}:{public_port}'

        with (tmp_semver_dir / 'config.toml').open('w') as fp:
            toml.dump(config_toml, fp)

        # Edit launcher state.
        utils.log('Customizing `casper-node-launcher-state.toml`')
        launcher_state_toml = toml.load(local_cfg_dir / 'casper-node-launcher-state.toml')

        launcher_state_toml['version'] = semver_dotted_str
        launcher_state_toml['binary_path'] = str(remote_bin_repo_dir / semver_snake_str / 'casper-node')
        launcher_state_toml['config_path'] = str(remote_cfg_repo_dir / semver_snake_str / 'config.toml')

        with (tmp_semver_dir / 'casper-node-launcher-state.toml').open('w') as fp:
            toml.dump(launcher_state_toml, fp)

        # Edit chainspec.
        utils.log('Customizing `chainspec.toml`')
        chainspec_toml = toml.load(local_cfg_dir / 'chainspec.toml')

        chainspec_toml['protocol']['version'] = semver_dotted_str
        chainspec_toml['protocol']['activation_point'] = activation_era

        with (tmp_semver_dir / 'chainspec.toml').open('w') as fp:
            toml.dump(chainspec_toml, fp)

        # Copy over modified configs.
        utils.log('Copying over modified configs')
        remote_node_ssh_copy(
            source_path=tmp_semver_dir,
            ssh_user=ssh_user,
            ssh_host=ssh_host,
            target_dir=remote_cfg_repo_dir,
            ssh_key_path=ssh_key_path,
        )

    # TODO: Continue here.

def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        f"Upgrades a node to its next available version, via semver."
    )

    parser.add_argument(
        "--net",
        default=env.get_network_name(),
        dest="network",
        help="Network name {type}{id}, e.g. nctl1.",
        type=args_validator.validate_network,
    )

    parser.add_argument(
        "--node",
        default=1,
        dest="node",
        help="Node index, e.g. 1.",
        type=args_validator.validate_node_index
    )

    parser.add_argument(
        "--update-cache-dir",
        dest="update_cache_dir",
        required=True,
        help="Path to directory containing semver folders with casper binaries "
            "(e.g. '1_0_0', '1_1_0', etc). Note this this should be local on "
            "the stest control box.",
        type=pl.Path,
    )

    parser.add_argument(
        "--remote-casper-dir",
        dest="remote_casper_dir",
        required=True,
        help="Remote path to casper-node installation dir.",
        type=pl.Path,
    )

    parser.add_argument(
        "--ssh-user",
        default='cladmin',
        dest="ssh_user",
        help="SSH username.",
        type=str,
    )

    parser.add_argument(
        "--ssh-key-path",
        default=None,
        dest="ssh_key_path",
        help="Path to SSH key.",
        type=pl.Path,
    )
