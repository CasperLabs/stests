import inspect

from stests.core.utils import env



class LibraryException(Exception):
    """Default library exception class.

    """

    def __init__(self, msg):
        """Constructor.

        :param msg: Exception message.

        """
        self.message = msg() if inspect.isfunction(msg) else str(msg)


    def __str__(self):
        """Returns a string representation.

        """
        return u"CLABS STESTS EXCEPTION : {0}".format(repr(self.message))


class InvalidEnvironmentVariable(LibraryException):
    """Raised when a library environment variable has been misconfigured.
    
    """
    def __init__(self, name, val, expected=None):
        """Constructor.

        :param name: Environment variable name.
        :param val: Environment variable val.
        :param expected: Expected value.

        """ 
        err = f"Invalid env-var: {env.get_var_name(name)} :: f{val}"
        if expected:
            if isinstance(expected, dict):
                expected = " | ".join(list(expected.keys()))
            err = f"{err}.  Expected {expected}"
        super(InvalidEnvironmentVariable, self).__init__(err)


class IgnoreableAssertionError(AssertionError):
    """Raised when an assertion may raise an error that can be igonored.
    
    """
    pass
