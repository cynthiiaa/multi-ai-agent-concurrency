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
    
    def increment_counter(thread_id, increments=1000):
        """Increment counter many times (simulates many small updates)"""
        print(f"🏃 Thread {thread_id} starting {increments} increments")
        
        for _ in range(increments):
            # ⚠️ RACE CONDITION: These three operations are NOT atomic
            current_value = counter["value"]  # 1. Read
            new_value = current_value + 1     # 2. Compute  
            counter["value"] = new_value      # 3. Write
            # If two threads interleave these steps, updates get lost!
    
    # Run multiple threads incrementing the same counter
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(increment_counter, i, 1000)
            for i in range(5)
        ]
        
        # Wait for all to complete
        for future in futures:
            future.result()
    
    expected_value = 5 * 1000  # 5 threads × 1000 increments each
    actual_value = counter["value"]
    
    print(f"\n📊 COUNTER RESULTS:")
    print(f"Expected value: {expected_value}")
    print(f"Actual value: {actual_value}")
    print(f"Lost increments: {expected_value - actual_value}")
    
    if actual_value < expected_value:
        print("❌ RACE CONDITION: Lost updates due to concurrent access!")
    else:
        print("✅ No race condition this time (but it might happen on next run)")


def unsafe_list_demo():
    """Demonstrates race conditions with list operations"""
    print("\n" + "="*60)
    print("🔄 Demonstrating race conditions with list updates")
    
    # Shared list that multiple threads will modify
    shared_list = []
    
    def add_items_to_list(thread_id, num_items=100):
        """Add items to shared list (simulates agent updates)"""
        print(f"🏃 Thread {thread_id} adding {num_items} items")
        
        for i in range(num_items):
            # ⚠️ RACE CONDITION: list.append() is NOT atomic!
            # Multiple threads can corrupt the list structure
            shared_list.append(f"thread_{thread_id}_item_{i}")
            
            # Add tiny delay to increase chance of race condition
            time.sleep(0.0001)
    
    # Run multiple threads modifying the same list
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(add_items_to_list, i, 100)
            for i in range(3)
        ]
        
        # Wait for all to complete
        for future in futures:
            future.result()
    
    expected_items = 3 * 100  # 3 threads × 100 items each
    actual_items = len(shared_list)
    
    print(f"\n📊 LIST RESULTS:")
    print(f"Expected items: {expected_items}")
    print(f"Actual items: {actual_items}")
    print(f"Lost items: {expected_items - actual_items}")
    
    if actual_items < expected_items:
        print("❌ RACE CONDITION: Lost list items due to concurrent access!")
        print("⚠️  In a multi-agent system, this would be lost messages/results!")
    else:
        print("✅ No race condition this time (but it might happen on next run)")


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
        
        # Simulate LLM API call
        time.sleep(0.5)
        
        # ⚠️ RACE CONDITION ZONE ⚠️
        # Multiple agents updating shared state simultaneously
        
        # Update conversation history
        current_history = agent_state["conversation_history"]
        new_message = {
            "agent": f"agent_{agent_id}",
            "message": f"Result from agent {agent_id}",
            "timestamp": time.time()
        }
        current_history.append(new_message)  # NOT thread-safe!
        
        # Update agent status
        agent_state["agent_statuses"][f"agent_{agent_id}"] = "completed"
        
        # Update counter
        current_count = agent_state["total_processed"]
        agent_state["total_processed"] = current_count + 1  # NOT atomic!
        
        print(f"✅ Agent {agent_id} completed work")
    
    # Run multiple agents in parallel
    num_agents = 5
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
    
    if not race_detected:
        print("✅ No race conditions detected this time")
        print("⚠️  But they could happen on the next run!")
    
    return race_detected


def run_multiple_times():
    """Run the demo multiple times to show inconsistent results"""
    print("\n" + "="*60)
    print("🔄 Running multiple times to show inconsistency")
    print("="*60)
    
    race_condition_counts = 0
    total_runs = 5
    
    for run in range(total_runs):
        print(f"\n🏃 RUN {run + 1}/{total_runs}")
        print("-" * 30)
        
        if agent_state_race_demo():
            race_condition_counts += 1
    
    print(f"\n📈 SUMMARY AFTER {total_runs} RUNS:")
    print(f"Race conditions detected: {race_condition_counts}/{total_runs}")
    print(f"Success rate: {((total_runs - race_condition_counts) / total_runs) * 100:.1f}%")
    
    if race_condition_counts > 0:
        print("❌ This is why race conditions are dangerous!")
        print("❌ Your system might work most of the time, but fail randomly")
    else:
        print("✅ No race conditions detected in this batch")
        print("⚠️  But they could still happen with different timing!")


if __name__ == "__main__":
    print("⚠️  RACE CONDITION DEMONSTRATION")
    print("=" * 60)
    print("This script shows you exactly what goes wrong with concurrent access")
    print("to shared state. Watch for lost updates and inconsistent results!")
    print("=" * 60)
    
    # Run individual demos
    unsafe_counter_demo()
    unsafe_list_demo()
    
    # Run multiple times to show inconsistency
    run_multiple_times()
    
    print("\n" + "="*60)
    print("🎯 KEY TAKEAWAYS:")
    print("• Race conditions cause sporadic, hard-to-debug failures")
    print("• They only show up under concurrent load")
    print("• Simple operations like list.append() are NOT thread-safe")
    print("• In multi-agent systems, this means lost messages and corrupt state")
    print("• The solution: use proper concurrency controls (locks, queues, etc.)")
    print("=" * 60)