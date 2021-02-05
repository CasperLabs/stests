import dataclasses
import typing
from datetime import datetime

from stests.core.types.chain.enums import DeployStatus
from stests.core.types.chain.enums import DeployType



@dataclasses.dataclass
class Deploy:
    """Encapsulates information pertaining to a deploy dispatched to a test network.
    
    """
    # Account under which deploy was dispatched.
    account: str

    # Index of account with which the deploy is associated.
    account_index: int

    # An account associated with the deploy - e.g. transfer target.
    associated_account: typing.Optional[str]

    # Index of account associated with the deploy - e.g. transfer target.
    associated_account_index: typing.Optional[int]

    # Associated block hash in event of finalization. 
    block_hash: typing.Optional[str]

    # Cost of deploy (in motes).
    deploy_cost: typing.Optional[int]    

    # Deploy's payload signature hash (blake). 
    deploy_hash: str

    # Number of times dispatcher had to try before deploy dispatch suceeded.
    dispatch_attempts: int

    # Time taken to dispatch deploy.
    dispatch_duration: float

    # Index of node to which deploy was dispatched.
    dispatch_node_index: str

    # Moment in time when deploy dispatched to CSPR network.
    dispatch_timestamp: datetime

    # Consensus era identifier.
    era_id: int

    # Time between dispatch & deploy finality.
    finalization_duration: typing.Optional[float]

    # Index of node which emitted finalization event of the block in which deploy was included.
    finalization_node_index: typing.Optional[str]
    
    # Moment in time when deploy was finalized by CSPR network.
    finalization_timestamp: typing.Optional[datetime]    

    # # Numerical index to distinguish between multiple phase within a generator.
    # generator_phase_index: typing.Optional[int]

    # # Numerical index to distinguish between multiple runs of the same generator.
    # generator_run_index: int

    # # Type of generator, e.g. WG-100 ...etc.
    # generator_type: str    

    # # Numerical index to distinguish between multiple steps within a generator.
    # generator_step_index: typing.Optional[int]

    # # Label to disambiguate a step within the context of a phase.
    # generator_step_label: typing.Optional[str]    

    # Numerical index to distinguish between multiple phase within a generator.
    phase_index: typing.Optional[int]

    # Consensus round identifier.
    round_id: int

    # Numerical index to distinguish between multiple runs of the same generator.
    run_index: typing.Optional[int]

    # Type of generator, e.g. WG-100 ...etc.
    run_type: typing.Optional[str]    

    # Root hash of chain state at point of block proposal.
    state_root_hash: typing.Optional[str]

    # Numerical index to distinguish between multiple steps within a generator.
    step_index: typing.Optional[int]

    # Label to disambiguate a step within the context of a phase.
    step_label: typing.Optional[str]

    # Associated network.
    network: str

    # Deploy's processing status.
    status: DeployStatus

    # Deploy's type so as to disambiguate.
    typeof: DeployType
        
    @property
    def is_from_network_faucet(self):
        return self.account_index == 0

    @property
    def label_finalization_duration(self):
        if self.finalization_duration:
            return format(self.finalization_duration, '.4f')
        return "--"

    @property
    def label_account_index(self):
        return f"A-{str(self.account_index).zfill(6)}"

    @property
    def label_run_index(self):
        return f"R-{str(self.run_index).zfill(3)}"




