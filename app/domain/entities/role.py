class Role:
    """Domain entity for a User"""

    def __init__(
        self,
        id: int,
        name: str,
        isActive: bool = True
    ):
        self.id = id
        self.name = name
        self.isActive = isActive
