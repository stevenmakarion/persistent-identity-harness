# Registry-Enforced Subsystems

**78 scheduled subsystems. If it is not in the registry, it does not exist.**

## The rule

Every scheduled thing that runs on this estate is declared in one registry with:

- what it is for, in one sentence
- how it proves it ran, which is an **artifact**, never a process name or an exit code
- how fresh that artifact must be before it counts as broken
- whether it is currently expected to run at all

A reconciler walks the registry twice a day and compares declarations against the machine.
It reports three classes: declared and healthy, declared and silent, and **running but
undeclared**. The third class is the dangerous one, because undeclared work is work nobody
is watching.

## Why exit codes are not proof

An exit code tells you a process finished. It does not tell you the process did anything.

This estate has produced, at various times: a job that ran nightly and produced nothing for
weeks while exiting zero, a scheduled entry that would have failed instantly because it
lacked a working directory, and a subsystem reporting success while delivering under two
percent of its payload.

**A job ran only if its artifact is new.** That is the only definition that has survived
contact.

## Fail closed

Any subsystem that cannot verify its own preconditions refuses to start rather than
proceeding. A refused run is visible and recoverable. A run that proceeds on bad
preconditions is neither, and it is often wrong in a direction that looks like success.

## Detection must interrupt

This is the law that cost the most.

At one point this estate had a reconciler running twice daily, an alert service posting to
a phone, and a status board printing its own zeros. All three worked. And a 19-day-old
alarm sat unread next to a subsystem that had been dead for ten days.

Nothing was broken. A sixth watcher would have changed nothing.

**A finding that cannot interrupt is a finding that did not happen.** The fix was not more
detection. It was routing findings onto the channel that reaches the operator before the
first command of the day, rather than onto a surface that has to be visited.

## Preflight over postmortem

The question is not *did it work*, which silently assumes it ran. The question is **can it
fire**, asked before it matters.

A preflight that proves every path is capable of executing, run before the work begins,
catches the class of failure where two months of careful analysis is performed on results
that were never produced. That failure is not rare and it does not announce itself.

The preflight here is trusted for one reason: it was replayed against three real historical
bugs from this estate and caught all three.
