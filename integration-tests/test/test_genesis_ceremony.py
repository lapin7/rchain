from random import Random

import pytest
from docker.client import DockerClient

from .conftest import (
    testing_context,
    temporary_wallets_file,
)
from .common import (
    KeyPair,
    CommandLineOptions,
)
from .rnode import (
    started_peer,
    ready_bootstrap,
)
from .wait import (
    wait_for_sent_unapproved_block,
    wait_for_block_approval,
)



CEREMONY_MASTER_KEYPAIR = KeyPair(private_key='80366db5fbb8dad7946f27037422715e4176dda41d582224db87b6c3b783d709', public_key='1cd8bf79a2c1bd0afa160f6cdfeb8597257e48135c9bf5e4823f2875a1492c97')
VALIDATOR_A_KEYPAIR = KeyPair(private_key='120d42175739387af0264921bb117e4c4c05fbe2ce5410031e8b158c6e414bb5', public_key='02ab69930f74b931209df3ce54e3993674ab3e7c98f715608a5e74048b332821')
VALIDATOR_B_KEYPAIR = KeyPair(private_key='1f52d0bce0a92f5c79f2a88aae6d391ddf853e2eb8e688c5aa68002205f92dad', public_key='043c56051a613623cd024976427c073fe9c198ac2b98315a4baff9d333fbb42e')


def test_successful_genesis_ceremony(command_line_options: CommandLineOptions, random_generator: Random, docker_client: DockerClient) -> None:
    """
    https://docs.google.com/document/d/1Z5Of7OVVeMGl2Fw054xrwpRmDmKCC-nAoIxtIIHD-Tc/
    """
    bootstrap_cli_options = {
        '--deploy-timestamp':   '1',
        '--required-sigs':      '2',
        '--duration':           '5min',
        '--interval':           '10sec',
    }
    peers_cli_flags = set(['--genesis-validator'])
    peers_cli_options = {
        '--deploy-timestamp':   '1',
        '--required-sigs':      '2',
    }
    peers_keypairs = [
        VALIDATOR_A_KEYPAIR,
        VALIDATOR_B_KEYPAIR,
    ]
    with testing_context(command_line_options, random_generator, docker_client, bootstrap_keypair=CEREMONY_MASTER_KEYPAIR, peers_keypairs=peers_keypairs) as context:
        with temporary_wallets_file(context.random_generator, [context.bootstrap_keypair] + context.peers_keypairs) as wallets:
            with ready_bootstrap(context=context, cli_options=bootstrap_cli_options, wallets_file=wallets) as bootstrap:
                with started_peer(context=context, network=bootstrap.network, bootstrap=bootstrap, name='validator-a', keypair=VALIDATOR_A_KEYPAIR, wallets_file=wallets, cli_flags=peers_cli_flags, cli_options=peers_cli_options) as validator_a:
                    with started_peer(context=context, network=bootstrap.network, bootstrap=bootstrap, name='validator-b', keypair=VALIDATOR_B_KEYPAIR, wallets_file=wallets, cli_flags=peers_cli_flags, cli_options=peers_cli_options) as validator_b:
                        wait_for_sent_unapproved_block(context, bootstrap)
                        wait_for_block_approval(context, validator_a)
                        wait_for_block_approval(context, validator_b)


@pytest.mark.xfail
def test_successful_genesis_ceremony_with_read_only(docker_client: DockerClient) -> None:
    assert False


@pytest.mark.xfail
def test_not_successful_genesis_ceremony(docker_client_session: DockerClient) -> None:
    assert False


@pytest.mark.xfail
def test_validator_catching_up(docker_client_session: DockerClient) -> None:
    assert False
