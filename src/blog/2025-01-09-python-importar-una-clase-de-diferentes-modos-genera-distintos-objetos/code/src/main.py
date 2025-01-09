import pathlib
import sys

from subfolder.exceptions import CustomError as FromSubfolderCustomError

# Modify sys.path to make a different import.
sys.path.append(str(pathlib.Path(__file__).parent.absolute().joinpath("subfolder")))

from exceptions import CustomError as FromFileCustomError


# The class imported in a different way does not capture the exception.
# The following code prints `Captured by FromFileCustomError`.
try:
    raise FromFileCustomError()
except FromSubfolderCustomError:
    print("Captured by FromSubfolderCustomError")
except FromFileCustomError:
    print("Captured by FromFileCustomError")

# No instances relation between classes imported in a different way.
assert not isinstance(FromFileCustomError(), FromSubfolderCustomError)
assert not isinstance(FromSubfolderCustomError(), FromFileCustomError)

# Different imports generate different objects.
assert FromFileCustomError is not FromSubfolderCustomError

# Show the difference between classes.
print(FromSubfolderCustomError)  # <class 'subfolder.exceptions.CustomError'>
print(FromFileCustomError)  # <class 'exceptions.CustomError'>

# The previous data means that different modules were loaded.
print(sys.modules["subfolder.exceptions"])  # <module 'subfolder.exceptions' from '/tmp/src/subfolder/exceptions.py'>
print(sys.modules["exceptions"])  # <module 'exceptions' from '/tmp/src/subfolder/exceptions.py'>

# Classes are different objects.
assert FromFileCustomError is not FromSubfolderCustomError
