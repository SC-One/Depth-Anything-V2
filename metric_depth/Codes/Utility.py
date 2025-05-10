import os
import tempfile

def is_valid_filename(filename):
    try:
        # Try creating a temporary file with the name
        test_path = os.path.join(tempfile.gettempdir(), filename)
        with open(test_path, 'w') as f:
            f.write('test')
        os.unlink(test_path)
        return True
    except (OSError, IOError):
        return False
    
def save_strings_to_file(strings, file_path):
    try:
        with open(file_path, 'w') as file:
            for string in strings:
                file.write(string + '\n')  # Write each string followed by a newline
        print(f"Successfully saved {len(strings)} strings to {file_path}")
        return True
    except IOError as e:
        print(f"Error writing to file {file_path}: {e}")
        return False