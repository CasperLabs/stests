import dataclasses



@dataclasses.dataclass
class ProcessInfo():
    """Encapsulates information pertaining to the running process.
    
    """
    # OS user running system.
    os_user: str

    # Process ID.
    pid: str
