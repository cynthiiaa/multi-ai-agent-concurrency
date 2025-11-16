# Race Conditions in Multi-Agent Systems

This directory demonstrates how race conditions manifest when multiple agents try to update shared state simultaneously. You'll see the problem in action, understand why it happens, and learn how to identify it in your own systems.

## The Problem

When you run agents in parallel, they often need to share state - conversation history, results, metadata. But if multiple agents write to the same data structure simultaneously, you get race conditions. Data gets corrupted, updates get lost, and your system becomes unreliable.

## What's In This Directory

### 🔴 `broken_sequential.py`

Shows the "simple" sequential approach that works but is slow. Each agent waits for the previous one to finish before starting. Safe but inefficient.

**Run it**: `python broken_sequential.py`

- Watch the timing - each agent blocks the next one
- Notice it works perfectly but takes forever

### 🔴 `broken_parallel.py`

Shows naive parallel execution with race conditions. Multiple agents update shared state simultaneously, leading to data corruption and lost updates.

**Run it**: `python broken_parallel.py`

- Run it multiple times - results will be inconsistent
- Watch how conversation history gets corrupted
- See how agent states get lost

### 🟢 `simple_fix.py`

Shows a basic fix using thread-safe data structures. Not the best solution, but demonstrates the concept.

**Run it**: `python simple_fix.py`

- Consistent results every time
- Fast execution without race conditions

### 📊 `race_condition_demo.py`

Deliberately triggers race conditions to show you exactly what goes wrong. Great for understanding the problem.

**Run it**: `python race_condition_demo.py`

- Shows before/after state corruption
- Demonstrates lost updates
- Helps you recognize the symptoms

## Key Concepts

### What Are Race Conditions?

Imagine two people editing the same document simultaneously. Person A reads the document, makes changes, saves. Person B reads the original document (before A's changes), makes different changes, saves. Person B's save overwrites A's work. That's a race condition.

In multi-agent systems:

- Agent A reads conversation history: `["message1", "message2"]`
- Agent B reads the same history: `["message1", "message2"]`
- Agent A appends its result: `["message1", "message2", "A's result"]`
- Agent B appends its result: `["message1", "message2", "B's result"]`
- Only B's result survives. A's work is lost.

### Why They're Sneaky

- Work fine in testing (you run one request at a time)
- Only fail under load (multiple concurrent users)
- Failures are sporadic and hard to reproduce
- Look like "weird bugs" rather than systematic issues

### Common Symptoms

- Intermittent data corruption
- Missing entries in conversation history
- Inconsistent results for identical inputs
- Errors that only happen in production

## Running the Examples

Start with the broken examples to see the problem:

```bash
python broken_sequential.py    # Slow but safe
python broken_parallel.py      # Fast but broken
```

Then see the fix:

```bash
python simple_fix.py           # Fast AND safe
```

Try the race condition demo:

```bash
python race_condition_demo.py  # Shows exactly what goes wrong
```

## Next Steps

Once you understand the race condition problem, move to:

- [`../02-async-await/`](../02-async-await/) - Learn proper async execution
- [`../03-thread-safety/`](../03-thread-safety/) - Master safe state management

## Tips

1. **Test under load**: Race conditions only show up with concurrent requests
2. **Use thread-safe data structures**: Python's `queue.Queue`, not `list`
3. **Never assume operations are atomic**: Even `list.append()` can cause corruption
4. **Look for shared mutable state**: That's where race conditions breed

Remember: If multiple agents can write to the same data simultaneously, you probably have a race condition waiting to happen.
