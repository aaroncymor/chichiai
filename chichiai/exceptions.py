class EnvironmentError(Exception):
    """
    Raised when a environment variable is not set.

    Args:
        Exception (Exception): EnvironmentError
    """
    pass


class UnsupportedModelError(Exception):
    """
    Raised when unsupported model is used.

    Args:
        model_name (str): The name of unsupported model
        Exception (Exception): UnsupportedModelError
    """

    def __init__(self, model_name):
        self.model = model_name
        super().__init__(
            f"Unsupported model: The model '{model_name}' doesn't exist "
            f"or is not supported yet."
        )
