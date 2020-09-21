import random
from uuid import uuid4

from dramatiq import group
from dramatiq import pipeline
from dramatiq import  middleware
from dramatiq.rate_limits import Barrier



class MessageGroup(group):
    """Extends dramatiq group composition primitive.
    
    """
    def run(self, *, delay=None, dispatch_window=None):
        """Run the actors in this group over a dispatch window.

        Parameters:
          delay(int): The minimum amount of time, in milliseconds,
            each message in the group should be delayed by.
        """

        if self.completion_callbacks:
            from dramatiq.middleware.group_callbacks import GROUP_CALLBACK_BARRIER_TTL, GroupCallbacks

            rate_limiter_backend = None
            for middleware in self.broker.middleware:
                if isinstance(middleware, GroupCallbacks):
                    rate_limiter_backend = middleware.rate_limiter_backend
                    break
            else:
                raise RuntimeError(
                    "GroupCallbacks middleware not found! Did you forget "
                    "to set it up? It is required if you want to use "
                    "group callbacks."
                )

            # Generate a new completion uuid on every run so that if a
            # group is re-run, the barriers are all separate.
            # Re-using a barrier's name is an unsafe operation.
            completion_uuid = str(uuid4())
            completion_barrier = Barrier(rate_limiter_backend, completion_uuid, ttl=GROUP_CALLBACK_BARRIER_TTL)
            completion_barrier.create(len(self.children))

            children = []
            for child in self.children:
                if isinstance(child, group):
                    raise NotImplementedError

                elif isinstance(child, pipeline):
                    pipeline_children = child.messages[:]
                    pipeline_children[-1] = pipeline_children[-1].copy(options={
                        "group_completion_uuid": completion_uuid,
                        "group_completion_callbacks": self.completion_callbacks,
                    })

                    children.append(pipeline(pipeline_children, broker=child.broker))

                else:
                    children.append(child.copy(options={
                        "group_completion_uuid": completion_uuid,
                        "group_completion_callbacks": self.completion_callbacks,
                    }))
        else:
            children = self.children

        for child in children:
            if isinstance(child, (group, pipeline)):
                child.run(delay=delay)
            else:
                delay = random.randint(0, dispatch_window) if dispatch_window else delay
                self.broker.enqueue(child, delay=delay)

        return self
