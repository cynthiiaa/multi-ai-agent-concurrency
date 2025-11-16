"""
Race Condition Demonstration

This script deliberately triggers race conditions to show you exactly 
what goes wrong. Great for understanding the problem before learning the solution.
"""
import time
import threading
from concurrent.futures import ThreadPoolExecutor


def unsafe_counter_demo():
    """Demonstrates race conditions with a simple counter"""
    print("🔄 Demonstrating race conditions with a counter")

    # Shared state that multiple threads will modify
    counter = {"value": 0}

    def increment_counter(thread_id, increments=5000):
        """Increment counter many times (simulates many small updates)"""
        print(f"🏃 Thread {thread_id} starting {increments} increments")

        for _ in range(increments):
            # ⚠️ RACE CONDITION: These three operations are NOT atomic
            current_value = counter["value"]  # 1. Read
            # Add tiny delay to make race condition MORE likely
            time.sleep(0.000001)  # 1 microsecond
            new_value = current_value + 1     # 2. Compute
            counter["value"] = new_value      # 3. Write
            # If two threads interleave these steps, updates get lost!

    # Run multiple threads incrementing the same counter
    # More threads = more contention = more likely to see race conditions
    num_threads = 10
    increments_per_thread = 5000

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(increment_counter, i, increments_per_thread)
            for i in range(num_threads)
        ]

        # Wait for all to complete
        for future in futures:
            future.result()

    expected_value = num_threads * increments_per_thread
    actual_value = counter["value"]

    print(f"\n📊 COUNTER RESULTS:")
    print(f"Expected value: {expected_value:,}")
    print(f"Actual value: {actual_value:,}")
    print(f"Lost increments: {expected_value - actual_value:,}")
    print(f"Loss percentage: {((expected_value - actual_value) / expected_value * 100):.2f}%")

    if actual_value < expected_value:
        print("❌ RACE CONDITION: Lost updates due to concurrent access!")
        return True
    else:
        print("✅ No race condition this time (but it might happen on next run)")
        return False


def unsafe_list_demo():
    """Demonstrates race conditions with list operations"""
    print("\n" + "="*60)
    print("🔄 Demonstrating race conditions with list updates")

    # Shared list that multiple threads will modify
    shared_list = []

    def add_items_to_list(thread_id, num_items=1000):
        """Add items to shared list (simulates agent updates)"""
        print(f"🏃 Thread {thread_id} adding {num_items} items")

        for i in range(num_items):
            # ⚠️ RACE CONDITION: Even list.append() has race conditions!
            # It's implemented as multiple operations internally

            # Read the list length
            current_len = len(shared_list)

            # Tiny delay to force thread interleaving
            if i % 100 == 0:  # Only delay occasionally to keep it fast
                time.sleep(0.0001)

            # Append based on what we think the position should be
            item = {
                "thread": thread_id,
                "item": i,
                "expected_position": current_len  # This can be wrong!
            }
            shared_list.append(item)

    # Run multiple threads modifying the same list
    num_threads = 8
    items_per_thread = 1000

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(add_items_to_list, i, items_per_thread)
            for i in range(num_threads)
        ]

        # Wait for all to complete
        for future in futures:
            future.result()

    expected_items = num_threads * items_per_thread
    actual_items = len(shared_list)

    print(f"\n📊 LIST RESULTS:")
    print(f"Expected items: {expected_items:,}")
    print(f"Actual items: {actual_items:,}")
    print(f"Lost items: {expected_items - actual_items:,}")

    # Check for position mismatches
    position_errors = 0
    for i, item in enumerate(shared_list):
        if item['expected_position'] != i:
            position_errors += 1

    if position_errors > 0:
        print(f"Position mismatches: {position_errors:,} ({(position_errors/actual_items*100):.1f}%)")

    if actual_items < expected_items or position_errors > 0:
        print("❌ RACE CONDITION: Lost list items or position errors!")
        print("⚠️  In a multi-agent system, this would be lost messages/results!")
        return True
    else:
        print("✅ No race condition this time (but it might happen on next run)")
        return False


def agent_state_race_demo():
    """Demonstrates race conditions in agent state management"""
    print("\n" + "="*60)
    print("🔄 Demonstrating race conditions in agent state")

    # Simulated agent shared state
    agent_state = {
        "conversation_history": [],
        "agent_statuses": {},
        "total_processed": 0
    }

    def simulate_agent_work(agent_id):
        """Simulate an agent doing work and updating shared state"""
        print(f"🤖 Agent {agent_id} starting work")

        # Simulate LLM API call (shorter than before for faster demo)
        time.sleep(0.1)

        # ⚠️ RACE CONDITION ZONE ⚠️
        # Multiple agents updating shared state simultaneously

        # Update conversation history with explicit read-modify-write
        current_history_len = len(agent_state["conversation_history"])

        # Delay to make race more likely
        time.sleep(0.01)

        new_message = {
            "agent": f"agent_{agent_id}",
            "message": f"Result from agent {agent_id}",
            "timestamp": time.time(),
            "expected_position": current_history_len
        }
        agent_state["conversation_history"].append(new_message)  # NOT thread-safe!

        # Update agent status
        agent_state["agent_statuses"][f"agent_{agent_id}"] = "completed"

        # Update counter in non-atomic way
        current_count = agent_state["total_processed"]
        time.sleep(0.001)  # Increase chance of race
        agent_state["total_processed"] = current_count + 1  # NOT atomic!

        print(f"✅ Agent {agent_id} completed work")

    # Run multiple agents in parallel
    num_agents = 10  # More agents = more contention
    with ThreadPoolExecutor(max_workers=num_agents) as executor:
        futures = [
            executor.submit(simulate_agent_work, i)
            for i in range(num_agents)
        ]

        # Wait for all agents to complete
        for future in futures:
            future.result()

    # Check results
    expected_messages = num_agents
    expected_statuses = num_agents
    expected_processed = num_agents

    actual_messages = len(agent_state["conversation_history"])
    actual_statuses = len(agent_state["agent_statuses"])
    actual_processed = agent_state["total_processed"]

    print(f"\n📊 AGENT STATE RESULTS:")
    print(f"Expected conversation messages: {expected_messages}")
    print(f"Actual conversation messages: {actual_messages}")
    print(f"Expected agent statuses: {expected_statuses}")
    print(f"Actual agent statuses: {actual_statuses}")
    print(f"Expected processed count: {expected_processed}")
    print(f"Actual processed count: {actual_processed}")

    # Check for position mismatches
    position_errors = 0
    for i, msg in enumerate(agent_state["conversation_history"]):
        if msg.get("expected_position") != i:
            position_errors += 1

    if position_errors > 0:
        print(f"Position mismatches in history: {position_errors}")

    # Check for race conditions
    race_detected = False

    if actual_messages < expected_messages:
        print("❌ RACE CONDITION: Lost conversation messages!")
        race_detected = True

    if actual_statuses < expected_statuses:
        print("❌ RACE CONDITION: Lost agent status updates!")
        race_detected = True

    if actual_processed < expected_processed:
        print("❌ RACE CONDITION: Lost counter updates!")
        race_detected = True

    if position_errors > 0:
        print("❌ RACE CONDITION: Position tracking corrupted!")
        race_detected = True

    if not race_detected:
        print("✅ No race conditions detected this time")
        print("⚠️  But they could happen on the next run!")

    return race_detected


def run_multiple_times():
    """Run the demo multiple times to show inconsistent results"""
    print("\n" + "="*60)
    print("🔄 Running agent state demo multiple times to show inconsistency")
    print("="*60)

    race_condition_counts = 0
    total_runs = 3  # Reduced for faster execution

    for run in range(total_runs):
        print(f"\n🏃 RUN {run + 1}/{total_runs}")
        print("-" * 30)

        if agent_state_race_demo():
            race_condition_counts += 1

        if run < total_runs - 1:
            time.sleep(0.5)  # Small pause between runs

    print(f"\n{'='*60}")
    print(f"📈 SUMMARY AFTER {total_runs} RUNS")
    print("="*60)
    print(f"Race conditions detected: {race_condition_counts}/{total_runs}")

    if race_condition_counts == total_runs:
        print(f"❌ ALL runs had race conditions!")
    elif race_condition_counts > 0:
        print(f"❌ {race_condition_counts} out of {total_runs} runs had race conditions!")
    else:
        print("⚠️  No race conditions detected in this batch")

    if race_condition_counts > 0:
        print("\n🔑 This is why race conditions are dangerous!")
        print("   Your system might work most of the time, but fail randomly")
        print("   Under production load with many concurrent users, failures are almost guaranteed!")
    else:
        print("\n⚠️  Even if you didn't see race conditions this time,")
        print("   they could still happen with different timing or under heavier load!")


if __name__ == "__main__":
    print("⚠️  RACE CONDITION DEMONSTRATION")
    print("=" * 60)
    print("This script shows you exactly what goes wrong with concurrent access")
    print("to shared state. Watch for lost updates and inconsistent results!")
    print("=" * 60)

    print("\n💡 We'll run three different demos:")
    print("   1. Counter race conditions (simple but clear)")
    print("   2. List operation race conditions (shows data loss)")
    print("   3. Agent state race conditions (realistic multi-agent scenario)\n")

    # Run individual demos
    print("\n" + "="*60)
    print("DEMO 1: COUNTER RACE CONDITIONS")
    print("="*60)
    unsafe_counter_demo()

    print("\n" + "="*60)
    print("DEMO 2: LIST OPERATION RACE CONDITIONS")
    print("="*60)
    unsafe_list_demo()

    # Run multiple times to show inconsistency
    print("\n" + "="*60)
    print("DEMO 3: AGENT STATE RACE CONDITIONS (MULTIPLE RUNS)")
    print("="*60)
    run_multiple_times()

    print("\n" + "="*60)
    print("🎯 KEY TAKEAWAYS")
    print("="*60)
    print("✓ Race conditions cause sporadic, hard-to-debug failures")
    print("✓ They only show up under concurrent load (multiple threads/processes)")
    print("✓ Even simple operations like list.append() can have race conditions")
    print("✓ In multi-agent systems, this means:")
    print("  - Lost messages in conversation history")
    print("  - Corrupted agent state")
    print("  - Incorrect counters and metrics")
    print("  - Unpredictable behavior that's hard to reproduce")
    print("\n💡 The solution: Use proper concurrency controls!")
    print("   - Locks (threading.Lock)")
    print("   - Thread-safe data structures (queue.Queue)")
    print("   - Atomic operations")
    print("   - Message passing patterns")
    print("="*60)
    print("\n👉 Check out simple_fix.py to see how to fix these issues!")