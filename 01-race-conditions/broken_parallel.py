"""
Parallel Agent Execution - Fast but Broken

This shows naive parallel execution with race conditions.
Multiple agents update shared state simultaneously, causing data corruption.
Run this multiple times - you'll get different results each time!
"""
import time
import random
from concurrent.futures import ThreadPoolExecutor


class MockLLMClient:
    """Simulates an LLM API call with realistic timing"""
    
    def chat_completion(self, messages):
        # Simulate API latency (2-4 seconds)
        time.sleep(random.uniform(2, 4))
        return f"Response to: {messages[-1]['content'][:50]}..."


class Agent:
    def __init__(self, name):
        self.name = name
        self.client = MockLLMClient()
    
    def process(self, prompt, shared_state):
        print(f"🤖 {self.name} starting work on: '{prompt[:30]}...'")
        start_time = time.time()

        # Make LLM API call (this takes time!)
        response = self.client.chat_completion([
            {"role": "user", "content": prompt}
        ])

        # ⚠️ RACE CONDITION HERE! ⚠️
        # Multiple threads are modifying shared_state simultaneously
        # Python lists are NOT thread-safe!

        # Step 1: Read current state
        current_history = shared_state["conversation_history"]
        current_count = len(current_history)

        # Step 2: Simulate processing the data (another thread might modify state here!)
        time.sleep(random.uniform(0.01, 0.05))  # Tiny delay to force interleaving

        # Step 3: Create new entry based on OLD count
        new_entry = {
            "agent": self.name,
            "prompt": prompt,
            "response": response,
            "timestamp": time.time(),
            "position": current_count  # This will be wrong if another thread appended!
        }

        # Step 4: Write to state - this can overwrite other threads' work!
        current_history.append(new_entry)
        shared_state["agent_states"][self.name] = "completed"

        # Also update a counter in a non-atomic way
        shared_state["total_responses"] = shared_state.get("total_responses", 0) + 1

        duration = time.time() - start_time
        print(f"✅ {self.name} finished in {duration:.1f}s")
        return response


def run_parallel_agents():
    """Run agents in parallel - fast but has race conditions"""
    print("🔄 Running agents in parallel (fast but broken)")

    # Shared state that agents will update
    # ⚠️ This is where race conditions happen! ⚠️
    shared_state = {
        "conversation_history": [],  # NOT thread-safe!
        "agent_states": {},          # NOT thread-safe!
        "total_responses": 0,        # NOT thread-safe!
        "metadata": {"start_time": time.time()}
    }

    # Create MORE agents to increase chance of race conditions
    agents = [
        Agent("Researcher"),
        Agent("Analyzer"),
        Agent("Writer"),
        Agent("Critic"),
        Agent("Summarizer"),
        Agent("Validator")
    ]

    prompts = [
        "Research the latest trends in multi-agent AI systems",
        "Analyze the key challenges in implementing these systems",
        "Write a summary of the main findings and recommendations",
        "Critique the proposed approaches for potential issues",
        "Summarize the key insights from the research",
        "Validate the conclusions against best practices"
    ]

    total_start = time.time()

    # Run agents in parallel using ThreadPoolExecutor
    # More agents = more likelihood of race conditions!
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = [
            executor.submit(agent.process, prompt, shared_state)
            for agent, prompt in zip(agents, prompts)
        ]

        # Wait for all to complete
        results = [future.result() for future in futures]

    total_time = time.time() - total_start

    print(f"\n📊 RESULTS:")
    print(f"⏰ Total time: {total_time:.1f} seconds")
    print(f"💬 Conversation entries: {len(shared_state['conversation_history'])}")
    print(f"✅ Agents completed: {len(shared_state['agent_states'])}")
    print(f"🔢 Total responses counter: {shared_state['total_responses']}")

    # Show the conversation history
    print(f"\n📝 Conversation History:")
    for i, entry in enumerate(shared_state['conversation_history']):
        recorded_position = entry.get('position', '?')
        print(f"  {i+1}. {entry['agent']} (thought it was position {recorded_position}): {entry['response'][:50]}...")

    # ⚠️ These checks will likely fail due to race conditions! ⚠️
    expected_entries = 6
    expected_agents = 6
    expected_count = 6

    print(f"\n🔍 CHECKING FOR RACE CONDITIONS:")
    print(f"Expected {expected_entries} conversation entries, got {len(shared_state['conversation_history'])}")
    print(f"Expected {expected_agents} completed agents, got {len(shared_state['agent_states'])}")
    print(f"Expected total_responses = {expected_count}, got {shared_state['total_responses']}")

    race_detected = False

    if len(shared_state['conversation_history']) != expected_entries:
        print("❌ RACE CONDITION DETECTED: Lost conversation entries!")
        race_detected = True

    if len(shared_state['agent_states']) != expected_agents:
        print("❌ RACE CONDITION DETECTED: Lost agent states!")
        race_detected = True

    if shared_state['total_responses'] != expected_count:
        print("❌ RACE CONDITION DETECTED: Counter is wrong!")
        race_detected = True

    # Check for position mismatches (shows read-modify-write race)
    for i, entry in enumerate(shared_state['conversation_history']):
        if entry.get('position') != i:
            print(f"❌ RACE CONDITION: Entry {i} thought it was position {entry.get('position')}!")
            race_detected = True

    if not race_detected:
        print("✅ No race conditions this time (but they might happen on next run!)")

    print(f"\n⚠️  Run this script multiple times - results will be inconsistent!")
    print(f"⚠️  That's the race condition problem in action!")

    return race_detected


if __name__ == "__main__":
    print("=" * 60)
    print("RACE CONDITION DEMONSTRATION")
    print("=" * 60)
    print("\n💡 This script runs 6 agents in parallel, all updating shared state.")
    print("   Watch for inconsistent results across multiple runs!\n")

    # Run multiple times to show inconsistency
    runs = 3
    race_count = 0

    for run_num in range(runs):
        print(f"\n{'='*60}")
        print(f"RUN #{run_num + 1}")
        print("=" * 60)

        if run_parallel_agents():
            race_count += 1

        if run_num < runs - 1:
            print("\n⏳ Waiting 1 second before next run...")
            time.sleep(1)

    # Summary
    print(f"\n\n{'='*60}")
    print("📈 SUMMARY")
    print("=" * 60)
    print(f"Total runs: {runs}")
    print(f"Race conditions detected: {race_count}/{runs}")

    if race_count > 0:
        print(f"\n❌ {race_count} out of {runs} runs had race conditions!")
        print("   This is why concurrent access to shared state is dangerous!")
    else:
        print("\n⚠️  No race conditions detected in these runs,")
        print("   but they could still happen! Try running the script again.")

    print("\n🔑 Key takeaway: Results are unpredictable without proper synchronization!")
    print("=" * 60)