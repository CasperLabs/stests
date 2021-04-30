import argparse
import pathlib as pl
import toml
import typing as tp
import tempfile

from stests.core.utils import args_validator
from stests.core.utils import env
from stests.core.utils import cli as utils
from sh.scripts.svc_utils import remote_node_ssh_copy, remote_node_ssh_invoke
from sh.scripts.svc_utils import remote_node_ssh_rsync
from sh.scripts.arg_utils import get_network_node

class Semver(tp.NamedTuple):
    major: int
    minor: int
    patch: int

    def snake_str(self) -> str:
        return f'{self.major}_{self.minor}_{self.patch}'

    def dotted_str(self) -> str:
        return f'{self.major}.{self.minor}.{self.patch}'

    @staticmethod
    def from_str(s: str) -> 'Semver':
        major_str, minor_str, patch_str = s.split('.')
        return Semver(
            major=int(major_str),
            minor=int(minor_str),
            patch=int(patch_str),
        )

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
    semver_snake_str = semver.snake_str()
    semver_dotted_str = semver.dotted_str()

    utils.log(f'Desired semver: {semver_dotted_str}')

    if not public_address:
        utils.log(f'Using SSH address as public address ({ssh_host})')
        public_address = ssh_host

    local_bin_dir = local_bin_repo_dir / semver_snake_str
    local_cfg_dir = local_cfg_repo_dir / semver_snake_str

    # Construct the expected remote repo paths to copy the new version dirs to.
    # A "repo dir" is a directory that contains subdirs of the form "X_Y_Z",
    # where X, Y, Z are major, minor, patch numbers, respectively.
    utils.log(f'Remote target bin repo dir `{remote_bin_repo_dir}`')
    utils.log(f'Remote target cfg repo dir `{remote_cfg_repo_dir}`')

    # A "transient" directory to copy files to, to then be moved to their final
    # location. This is needed because `scp` can't copy files to dirs it does
    # not have permissions for.
    transient_remote_repo = pl.Path('./')
    transient_remote_dir = transient_remote_repo / semver_snake_str

    # Copy over casper-node binary dir.
    utils.log('Copying over casper-node binary')
    remote_node_ssh_copy(
        source_path=local_bin_dir,
        ssh_user=ssh_user,
        ssh_host=ssh_host,
        target_dir=transient_remote_repo,
        ssh_key_path=ssh_key_path,
    )

    utils.log(f'Running `chown` on copied bin dir: {transient_remote_dir}')
    remote_node_ssh_invoke(
        ssh_user=ssh_user,
        ssh_host=ssh_host,
        to_run=f'sudo chown -R casper:casper {transient_remote_dir}',
        ssh_key_path=ssh_key_path,
    )

    utils.log(f'Moving copied bin dir to final location @ {remote_bin_repo_dir}')
    remote_node_ssh_invoke(
        ssh_user=ssh_user,
        ssh_host=ssh_host,
        to_run=f'sudo mv --no-clobber --update {transient_remote_dir} {remote_bin_repo_dir}/',
        ssh_key_path=ssh_key_path,
    )

    # Need to edit some config files, so create a temp dir.
    utils.log('Creating temp dir')
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
        launcher_state_toml['binary_path'] = str(
            remote_bin_repo_dir / semver_snake_str / 'casper-node'
        )
        launcher_state_toml['config_path'] = str(
            remote_cfg_repo_dir / semver_snake_str / 'config.toml'
        )

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
            target_dir=transient_remote_repo,
            ssh_key_path=ssh_key_path,
        )

        utils.log(f'Running `chown` on copied cfg dir: {transient_remote_dir}')
        remote_node_ssh_invoke(
            ssh_user=ssh_user,
            ssh_host=ssh_host,
            to_run=f'sudo chown -R casper:casper {transient_remote_dir}',
            ssh_key_path=ssh_key_path,
        )

        utils.log(f'Moving copied cfg dir to final location @ {remote_cfg_repo_dir}')
        remote_node_ssh_invoke(
            ssh_user=ssh_user,
            ssh_host=ssh_host,
            to_run=f'sudo mv --no-clobber --update {transient_remote_dir} {remote_cfg_repo_dir}/',
            ssh_key_path=ssh_key_path,
        )

    utils.log('Destroying temp dir')

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
        "--local-bin-repo",
        dest="local_bin_repo",
        required=True,
        help="Path to directory containing semver folders with casper binaries "
            "(e.g. '1_0_0', '1_1_0', etc). Note this this should be local on "
            "the stest control box.",
        type=pl.Path,
    )

    parser.add_argument(
        "--local-cfg-repo",
        dest="local_cfg_repo",
        required=True,
        help="Path to directory containing semver folders with casper configs "
            "(e.g. '1_0_0', '1_1_0', etc). Note this this should be local on "
            "the stest control box.",
        type=pl.Path,
    )

    parser.add_argument(
        "--remote-bin-repo",
        dest="remote_bin_repo",
        default=pl.Path('/var/lib/casper/bin'),
        help="Remote path to casper binary repo dir.",
        type=pl.Path,
    )

    parser.add_argument(
        "--remote-cfg-repo",
        dest="remote_cfg_repo",
        default=pl.Path('/etc/casper'),
        help="Remote path to casper config repo dir.",
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

    parser.add_argument(
        "--semver",
        required=True,
        dest="semver",
        help="Semver (in X.Y.Z format) for desired version to install.",
        type=Semver.from_str,
    )

    parser.add_argument(
        "--activation-era",
        required=True,
        dest="activation_era",
        help="Future era id at which upgrade is inteded to become active.",
        type=int,
    )

    return parser

if __name__ == '__main__':
    parser = get_arg_parser()

    args = parser.parse_args()

    _, node = get_network_node(args)

    # # TODO: For testing, remove once smoke tested.
    # push_update_to_node(
    #     ssh_user='stest',
    #     ssh_host=node.host,
    #     ssh_key_path=args.ssh_key_path,
    #     semver=Semver(major=1, minor=1, patch=0),
    #     local_bin_repo_dir=pl.Path('/home/stest/upgrade_queue/bin'),
    #     local_cfg_repo_dir=pl.Path('/home/stest/upgrade_queue/cfg'),
    #     activation_era=272727,
    #     public_address=None,
    #     public_port=35000,
    #     # remote_bin_repo_dir=pl.Path('/var/lib/casper/bin'),
    #     # remote_cfg_repo_dir=pl.Path('/etc/casper'),
    #     remote_bin_repo_dir=pl.Path('/tmp/bin_tmp'),
    #     remote_cfg_repo_dir=pl.Path('/tmp/cfg_tmp'),
    # )

    push_update_to_node(
        ssh_user=args.ssh_user,
        ssh_host=node.host,
        ssh_key_path=args.ssh_key_path,
        semver=args.semver,
        local_bin_repo_dir=args.local_bin_repo,
        local_cfg_repo_dir=args.local_cfg_repo,
        activation_era=args.activation_era,
        public_address=None,
        public_port=35000,
        remote_bin_repo_dir=pl.Path('/var/lib/casper/bin'),
        remote_cfg_repo_dir=pl.Path('/etc/casper'),
    )
