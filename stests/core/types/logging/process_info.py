import dataclasses



@dataclasses.dataclass
class ProcessInfo():
    """Encapsulates information pertaining to the running process.
    
    """
    # Machine upon which system is running.
    host: str

    # Network of which machine is a member.
    net: str

    # OS user running system.
    os_user: str

    # Process ID.
    pid: str
