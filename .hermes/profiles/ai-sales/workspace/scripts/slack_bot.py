#!/usr/bin/env python3
"""Compatibility wrapper: notify pending review items to Slack once."""
from review_manager import main
if __name__ == '__main__':
    import sys
    sys.argv = [sys.argv[0], 'notify']
    raise SystemExit(main())
