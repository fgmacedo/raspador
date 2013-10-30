.. :changelog:

Release history
===============

0.2.2 (2013-10-30)
------------------

- More tests translated to ``en``.
- More useful log messages.

**API Changes:**

- ``BaseField._setup`` renamed to ``BaseField.setup``.
- ``FloatField`` has new parameters and defaults: ``thousand_separator`` and
  ``decimal_separator``.
- ``BRFloatField`` is now deprecated in favor of ``FloatField`` parameters.
