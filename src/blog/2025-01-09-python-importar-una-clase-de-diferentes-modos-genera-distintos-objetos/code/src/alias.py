from subfolder.exceptions import CustomError as FromSubfolderCustomError
from subfolder.exceptions import CustomError as BFromSubfolderCustomError

assert FromSubfolderCustomError is BFromSubfolderCustomError
assert isinstance(FromSubfolderCustomError(), BFromSubfolderCustomError)
