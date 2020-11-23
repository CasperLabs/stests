import typing

from stests.core.types.orchestration import ExecutionContext
from stests.core.types.infra import NodeIdentifier
from stests.generators.meta import GENERATOR_MAP as WORKFLOWS



class WorkflowStep():
    """A step with a phase of a broader workflow.
    
    """
    def __init__(self, index: int, container):
        """Constructor.
        
        :param index: Ordinal position within set of steps.
        :param container: Module containing step related functions.

        """
        # Index within the set of phase steps.
        self.index: int = index

        # A flag indicating whether this is an asynchronous step - i.e. relies upon chain events to complete.
        self.is_async = hasattr(container, "verify_deploy")

        # Flag indicating whether this is the last step within the phase.
        self.is_last: bool = False

        # A flag indicating whether this is a synchronous step.
        self.is_sync = not self.is_async

        # Python module in which the step is declared.
        self.container = container

        # Execution error.
        self.error: typing.Union[str, Exception] = None

        # Execution result.
        self.result: typing.Union[None, typing.Callable] = None

    @property
    def has_verifer(self) -> bool:
        try:
            self.container.verify
        except AttributeError:
            return False
        else:
            return True

    @property
    def has_verifer_for_deploy(self) -> bool:
        try:
            self.container.verify_deploy
        except AttributeError:
            return False
        else:
            return True

    @property
    def label(self) -> str:
        return self.container.LABEL


    def execute(self, ctx):
        """Performs step execution.
        
        :param ctx: Execution context information.

        """
        try:
            self.result = self.container.execute(ctx)
        except Exception as err:
            self.error = err


    def verify(self, ctx):
        """Performs step verification.
        
        :param ctx: Execution context information.
        
        """
        self.container.verify(ctx)


    def verify_deploy(self, ctx: ExecutionContext, node_id: NodeIdentifier, block_hash: str, deploy_hash: str):
        """Performs step deploy verification.
        
        :param ctx: Execution context information.
        :param node_id: Identifier of node emitting chain event.
        :param block_hash: Hash of block in which deploy was batched.
        :param deploy_hash: Hash of deploy being processed.

        """
        self.container.verify_deploy(ctx, node_id, block_hash, deploy_hash)


    def verify_deploy_batch_is_complete(self, ctx: ExecutionContext, deploy_index: int):
        """Performs step deploy batch is complete verification.
        
        :param ctx: Execution context information.
        :param deploy_index: Index of a finalized deploy in relation to the deploys dispatched during this step.

        """
        try:
            self.container.verify_deploy_batch_is_complete
        except AttributeError:
            pass
        else:
            self.container.verify_deploy_batch_is_complete(ctx, deploy_index)


class WorkflowPhase():
    """A phase within a broader workflow.
    
    """
    def __init__(self, index: int, container):
        """Constructor.
        
        :param index: Ordinal position within set of phases.
        :param container: Module or tuple containing phase steps.

        """
        # Index within the set of phases.
        self.index: int = index

        # Flag indicating whether this is the last phase within the workflow.
        self.is_last: bool = False

        # Set steps.
        if isinstance(container, tuple):
            self.steps = [WorkflowStep(i, s) for i, s in enumerate(container)]
        else:
            self.steps = [WorkflowStep(i, s) for i, s in enumerate(container.STEPS)]

        # Set last step flag.
        if self.steps:
            self.steps[-1].is_last = True


    def get_step(self, step_index: int) -> WorkflowStep:
        """Returns a step within managed collection.
        
        """
        return self.steps[step_index - 1]


class Workflow():
    """A workflow executed in order to test a scenario.
    
    """
    def __init__(self, meta):
        """Constructor.

        :param ctx: Execution context information.
        :param meta: Workflow metadata module.

        """
        # Set phases.
        self.phases = [WorkflowPhase(i, p) for i, p in enumerate(meta.PHASES)]

        # Set last phase flag.
        if self.phases:
            self.phases[-1].is_last = True

    
    def get_phase(self, phase_index: int) -> WorkflowPhase:
        """Returns a phase within managed collection.
        
        """
        return self.phases[phase_index - 1]


    def get_step(self, phase_index: int, step_index: int) -> WorkflowStep:
        """Returns a step within managed collection.
        
        """
        phase = self.get_phase(phase_index) 

        return phase.get_step(step_index)


    @staticmethod
    def create(ctx: ExecutionContext):
        """Simple factory method.
        
        :param ctx: Workflow execution context information.

        :returns: Workflow wrapper instance.

        """
        try:
            WORKFLOWS[ctx.run_type]
        except KeyError:
            raise ValueError(f"Unsupported workflow type: {ctx.run_type}")
        else:
            return Workflow(WORKFLOWS[ctx.run_type])


    @staticmethod
    def get_phase_(ctx: ExecutionContext, phase_index: int) -> WorkflowPhase:
        """Simple factory method.
        
        :param ctx: Workflow execution context information.

        :returns: Workflow wrapper instance.

        """
        try:
            wflow = Workflow.create(ctx)
        except:
            return None
        else:
            return wflow.get_phase(phase_index)


    @staticmethod
    def get_phase_step(ctx: ExecutionContext, phase_index: int, step_index: int) -> WorkflowStep:
        """Simple factory method.
        
        :param ctx: Workflow execution context information.

        :returns: Workflow wrapper instance.

        """
        try:
            wflow = Workflow.create(ctx)
        except:
            return None
        else:
            return wflow.get_step(phase_index, step_index)
