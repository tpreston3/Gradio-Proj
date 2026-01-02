import os

key = os.environ.get('GOOGLE_API_KEY')
key1 = os.environ.get('GEMINI_API_KEY')


print("Please set your Google API key in the environment variable 'GOOGLE_API_KEY'.", key)
print("Please set your Gemini API key in the environment variable 'GEMINI_API_KEY'.", key1)
import os

def show_environment_variables():
    """
    Prints all system environment variables and their values.
    Also, specifically prints the PATH environment variable in a formatted way.
    """
    print("--------------------------------------------------")
    print("          ALL ENVIRONMENT VARIABLES")
    print("--------------------------------------------------")

    # os.environ is a dictionary-like object containing all environment variables
    if not os.environ:
        print("No environment variables found.")
        return

    # Sort the variables by name for easier reading
    for var_name, var_value in sorted(os.environ.items()):
        print(f"{var_name} = {var_value}")

    print("\n--------------------------------------------------")
    print("          PATH Environment Variable Details")
    print("--------------------------------------------------")

    # Get the PATH environment variable
    path_variable = os.environ.get('PATH')

    if path_variable:
        print("The 'PATH' variable contains the following directories (searched for executables):\n")
        # In Windows, paths are separated by semicolons; in Linux/macOS, by colons.
        # os.pathsep handles this automatically.
        paths = path_variable.split(os.pathsep)
        for idx, p in enumerate(paths):
            print(f"{idx + 1}. {p}")
    else:
        print("The 'PATH' environment variable is not set or is empty.")

    print("\n--------------------------------------------------")
    print("Note: Environment variables are key-value pairs. They don't have a single 'path' themselves,")
    print("but the 'PATH' variable specifically contains a list of directory paths.")
    print("The script above lists all variables and then details the 'PATH' variable.")
    print("--------------------------------------------------")

if __name__ == "__main__":
    show_environment_variables()
