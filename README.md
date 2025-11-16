# Multi-Agent Concurrency Companion Repository

This repository contains practical examples and runnable code that complement the blog post on concurrency in multi-agent AI systems. If you're an MLE or data scientist looking to improve your software engineering skills, this repo will help you understand the low-level primitives that make multi-agent systems scale.

## Why This Matters

Multi-agent AI is exploding in popularity, but most tutorials focus on the high-level architecture. They show you the patterns but skip the crucial implementation details. This repo fills that gap by teaching you the concurrency fundamentals that make these systems work in production.

## What You'll Learn

- How race conditions manifest in LLM systems (and how to prevent them)
- Async/await patterns for massive performance gains
- Thread-safe state management techniques
- Rate limiting and backpressure handling
- Testing strategies for concurrent agent systems

## Repository Structure

### 📁 [`01-race-conditions/`](./01-race-conditions/)

**The Problem**: See exactly how parallel agents can corrupt shared state

Examples include:

- Broken parallel execution that loses data
- Race condition demonstrations
- Sequential vs parallel timing comparisons

### 📁 [`02-async-await/`](./02-async-await/)

**The Solution**: Learn async/await for I/O-bound speedups

Examples include:

- Synchronous vs asynchronous agent execution
- Proper async client usage patterns
- Performance benchmarking code

### 📁 [`03-thread-safety/`](./03-thread-safety/)

**The Implementation**: Build thread-safe agent state management

Examples include:

- Immutable state patterns
- Lock-based shared state
- Thread-safe data structures

### 📁 [`04-testing/`](./04-testing/)

**The Verification**: Test concurrent systems properly

Examples include:

- Concurrency-specific test patterns
- Load testing with pytest
- Race condition detection

### 📁 [`05-production/`](./05-production/)

**The Complete System**: Put it all together

Examples include:

- Full production-ready architecture
- Rate limiting with semaphores
- Error handling and timeouts
- Clean interfaces and dependency injection

## Quick Start

1. **Clone and setup**:

```bash
git clone <repository-url>
cd concurrency-blog
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Set up your API keys**:

```bash
export OPENAI_API_KEY="your-key-here"
# or create a .env file with your keys
```

3. **Start with the basics**:

```bash
cd 01-race-conditions
python broken_agents.py  # See the problem
python fixed_agents.py   # See the solution
```

4. **Progress through each directory** in order, running the examples and reading the accompanying documentation.

## Prerequisites

- Python 3.8+
- Basic familiarity with Python async/await
- An OpenAI API key (for examples)
- Understanding of multi-agent concepts (covered in the blog post)

## Learning Path

1. **Start with `01-race-conditions/`** - Understand the problem
2. **Move to `02-async-await/`** - Learn the speed solution
3. **Continue to `03-thread-safety/`** - Master safe state management
4. **Practice with `04-testing/`** - Learn to verify correctness
5. **Finish with `05-production/`** - See the complete picture

Each directory builds on the previous one, so follow the order for best results.

## Running the Examples

Most directories have both "broken" and "fixed" versions of code:

- `broken_*.py` - Shows the problem
- `fixed_*.py` - Shows the solution
- `benchmark_*.py` - Measures performance

Run them side by side to see the difference:

```bash
python broken_example.py
python fixed_example.py
```

## Common Issues

**API Rate Limits**: Examples use real LLM APIs. Start with small examples and adjust rate limits in the code if you hit quota limits.

**Environment Setup**: Use a virtual environment. Some examples require specific async-compatible libraries.

**Python Version**: Examples assume Python 3.8+. Some async features won't work on older versions.

## Additional Resources

- [Original Blog Post](link-to-blog) - Deep dive into the concepts
- [Anthropic's Multi-Agent Research](https://www.anthropic.com/research/building-effective-agents) - The research that inspired this work
- [AsyncIO Documentation](https://docs.python.org/3/library/asyncio.html) - Python's async programming guide

## Questions?

If you're stuck on a concept, check the corresponding section in the blog post first. The code here is meant to be hands-on practice for the theory explained there.

Happy coding 🚀!
