ms_wrapper
==========

Wrapper(s) for a popular coalescent simulator Hudson's ms.
These implement additional models that can be simulated without
modifying ms.

Wrappers
--------

Following models are implemented.

- ms_ps.py: Partial-selfing with and without recombination
  (Nordborg & Donnelly (1997), Nordborg(2000))

Requirement
-----------

Either python2 or python3 with scipy in addition to ms.  ms should be found either in
search path or under ./msdir/.
