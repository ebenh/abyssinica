from abyssinica.calendar.date import Date

# Date is defined in a submodule but belongs to this package as far as
# callers are concerned, so report that path in repr. Version 2.0.0 shipped
# this class in a flat calendar.py, where its repr read the same way.
Date.__module__ = __name__

__all__ = ['Date']
