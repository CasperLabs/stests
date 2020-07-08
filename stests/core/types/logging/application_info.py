import dataclasses



@dataclasses.dataclass
class ApplicationInfo():
    """Encapsulates information pertaining to the application.
    
    """
    # System emitting event, i.e. STESTS.
    system: str

    # Sub-system emitting event, e.g. CORE.
    sub_system: str

    # System version.
    version: str
