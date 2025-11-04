#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tograph_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # If running server, set default host and port
    # Default to localhost for security, use 0.0.0.0 explicitly if needed
    if len(sys.argv) >= 2 and sys.argv[1] == 'runserver':
        if len(sys.argv) == 2:
            sys.argv.append('127.0.0.1:8000')
    
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
