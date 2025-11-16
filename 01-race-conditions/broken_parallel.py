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
        
        # Read current state
        current_history = shared_state["conversation_history"]
        current_states = shared_state["agent_states"]
        
        # Simulate some processing time where race conditions can occur
        time.sleep(0.1)
        
        # Update state - this can get corrupted!
        current_history.append({
            "agent": self.name,
            "prompt": prompt,
            "response": response,
            "timestamp": time.time()
        })
        current_states[self.name] = "completed"
        
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
        "metadata": {"start_time": time.time()}
    }
    
    # Create agents
    agents = [
        Agent("Researcher"),
        Agent("Analyzer"), 
        Agent("Writer")
    ]
    
    prompts = [
        "Research the latest trends in multi-agent AI systems",
        "Analyze the key challenges in implementing these systems", 
        "Write a summary of the main findings and recommendations"
    ]
    
    total_start = time.time()
    
    # Run agents in parallel using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=3) as executor:
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
    
    # Show the conversation history
    print(f"\n📝 Conversation History:")
    for i, entry in enumerate(shared_state['conversation_history']):
        print(f"  {i+1}. {entry['agent']}: {entry['response'][:60]}...")
    
    # ⚠️ These assertions might fail due to race conditions! ⚠️
    expected_entries = 3
    expected_agents = 3
    
    print(f"\n🔍 CHECKING FOR RACE CONDITIONS:")
    print(f"Expected {expected_entries} conversation entries, got {len(shared_state['conversation_history'])}")
    print(f"Expected {expected_agents} completed agents, got {len(shared_state['agent_states'])}")
    
    if len(shared_state['conversation_history']) != expected_entries:
        print("❌ RACE CONDITION DETECTED: Lost conversation entries!")
    
    if len(shared_state['agent_states']) != expected_agents:
        print("❌ RACE CONDITION DETECTED: Lost agent states!")
    
    if (len(shared_state['conversation_history']) == expected_entries and 
        len(shared_state['agent_states']) == expected_agents):
        print("✅ No race conditions this time (but they might happen on next run!)")
    
    print(f"\n⚠️  Run this script multiple times - results will be inconsistent!")
    print(f"⚠️  That's the race condition problem in action!")


if __name__ == "__main__":
    print("=" * 60)
    run_parallel_agents()
    print("=" * 60)
    print("\n🔄 Try running this script again - you might get different results!")
    print("That inconsistency is exactly what race conditions cause.")