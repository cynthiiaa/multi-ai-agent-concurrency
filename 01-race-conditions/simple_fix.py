"""
Fixed Parallel Agent Execution - Fast AND Safe

This shows how to fix race conditions using thread-safe data structures.
Now we get the speed of parallel execution without the data corruption.
"""
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue


class MockLLMClient:
    """Simulates an LLM API call with realistic timing"""
    
    def chat_completion(self, messages):
        # Simulate API latency (2-4 seconds)
        time.sleep(random.uniform(2, 4))
        return f"Response to: {messages[-1]['content'][:50]}..."


class ThreadSafeState:
    """Thread-safe shared state for agents"""
    
    def __init__(self):
        self._lock = threading.Lock()
        self._conversation_history = []
        self._agent_states = {}
        self._metadata = {"start_time": time.time()}
    
    def add_conversation_entry(self, agent_name, prompt, response):
        """Thread-safe way to add conversation entry"""
        with self._lock:
            self._conversation_history.append({
                "agent": agent_name,
                "prompt": prompt,
                "response": response,
                "timestamp": time.time()
            })
    
    def set_agent_state(self, agent_name, state):
        """Thread-safe way to set agent state"""
        with self._lock:
            self._agent_states[agent_name] = state
    
    def get_conversation_history(self):
        """Thread-safe way to get conversation history"""
        with self._lock:
            return self._conversation_history.copy()
    
    def get_agent_states(self):
        """Thread-safe way to get agent states"""
        with self._lock:
            return self._agent_states.copy()
    
    def get_stats(self):
        """Thread-safe way to get current stats"""
        with self._lock:
            return {
                "conversation_entries": len(self._conversation_history),
                "completed_agents": len(self._agent_states)
            }


class Agent:
    def __init__(self, name):
        self.name = name
        self.client = MockLLMClient()
    
    def process(self, prompt, safe_state):
        print(f"🤖 {self.name} starting work on: '{prompt[:30]}...'")
        start_time = time.time()
        
        # Make LLM API call (this takes time!)
        response = self.client.chat_completion([
            {"role": "user", "content": prompt}
        ])
        
        # ✅ UPDATE STATE SAFELY ✅
        # Using thread-safe methods instead of direct manipulation
        safe_state.add_conversation_entry(self.name, prompt, response)
        safe_state.set_agent_state(self.name, "completed")
        
        duration = time.time() - start_time
        print(f"✅ {self.name} finished in {duration:.1f}s")
        return response


def run_safe_parallel_agents():
    """Run agents in parallel safely - fast AND correct"""
    print("🔄 Running agents in parallel (fast and safe)")
    
    # ✅ Thread-safe shared state ✅
    safe_state = ThreadSafeState()
    
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
            executor.submit(agent.process, prompt, safe_state)
            for agent, prompt in zip(agents, prompts)
        ]
        
        # Wait for all to complete
        results = [future.result() for future in futures]
    
    total_time = time.time() - total_start
    
    # Get final state safely
    conversation_history = safe_state.get_conversation_history()
    agent_states = safe_state.get_agent_states()
    stats = safe_state.get_stats()
    
    print(f"\n📊 RESULTS:")
    print(f"⏰ Total time: {total_time:.1f} seconds")
    print(f"💬 Conversation entries: {stats['conversation_entries']}")
    print(f"✅ Agents completed: {stats['completed_agents']}")
    
    # Show the conversation history
    print(f"\n📝 Conversation History:")
    for i, entry in enumerate(conversation_history):
        print(f"  {i+1}. {entry['agent']}: {entry['response'][:60]}...")
    
    # ✅ These should always pass now! ✅
    expected_entries = 3
    expected_agents = 3
    
    print(f"\n🔍 CHECKING FOR RACE CONDITIONS:")
    print(f"Expected {expected_entries} conversation entries, got {stats['conversation_entries']}")
    print(f"Expected {expected_agents} completed agents, got {stats['completed_agents']}")
    
    assert stats['conversation_entries'] == expected_entries, "Lost conversation entries!"
    assert stats['completed_agents'] == expected_agents, "Lost agent states!"
    
    print("✅ All data is consistent AND fast!")
    print(f"✅ Total time: {total_time:.1f}s (much faster than sequential)")
    
    return total_time


def compare_with_sequential():
    """Compare timing with sequential execution"""
    print("\n" + "="*60)
    print("🏁 PERFORMANCE COMPARISON")
    print("="*60)
    
    # Rough sequential timing estimate (3 agents × 3 seconds average each)
    estimated_sequential_time = 9  # seconds
    
    parallel_time = run_safe_parallel_agents()
    
    speedup = estimated_sequential_time / parallel_time
    
    print(f"\n📈 PERFORMANCE RESULTS:")
    print(f"Estimated sequential time: {estimated_sequential_time:.1f}s")
    print(f"Parallel time: {parallel_time:.1f}s")
    print(f"Speedup: {speedup:.1f}x faster")
    print(f"Time saved: {estimated_sequential_time - parallel_time:.1f}s")


if __name__ == "__main__":
    print("=" * 60)
    compare_with_sequential()
    print("=" * 60)
    print("\n🎉 This version is both fast AND safe!")
    print("🔄 Run it multiple times - results will always be consistent!")