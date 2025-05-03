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