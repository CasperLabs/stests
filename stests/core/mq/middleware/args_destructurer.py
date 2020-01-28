import dramatiq



class ArgsDestructurerMiddleware(dramatiq.Middleware):
    """Middleware to destructure arguments when used in a workflow pipeline.
    
    """
    def before_process_message(self, broker, message):
        """Called before a message is processed.

        :param broker: Message broker to which message was dispatched.
        :param message: A message being processed.

        """
        # When an actor returns args to be passed to the next actor in a pipeline,
        # dramatiq serialises the args as an array.  We wish that they are serialised
        # as a tuple so that the next actor will not need to destructure.  
        if len(message.args) == 1 and isinstance(message.args[0], list):
            message.args = tuple(message.args[0])

