"""
Sequential Agent Execution - Safe but Slow

This shows the traditional approach: run agents one after another.
It works perfectly but wastes time waiting between agents.
"""
import time
import random


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
        
        # Update shared state
        shared_state["conversation_history"].append({
            "agent": self.name,
            "prompt": prompt,
            "response": response,
            "timestamp": time.time()
        })
        shared_state["agent_states"][self.name] = "completed"
        
        duration = time.time() - start_time
        print(f"✅ {self.name} finished in {duration:.1f}s")
        return response


def run_sequential_agents():
    """Run agents one at a time - safe but slow"""
    print("🔄 Running agents sequentially (safe but slow)")
    
    # Shared state that agents will update
    shared_state = {
        "conversation_history": [],
        "agent_states": {},
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
    results = []
    
    # Run each agent sequentially - this is SLOW
    for agent, prompt in zip(agents, prompts):
        result = agent.process(prompt, shared_state)
        results.append(result)
    
    total_time = time.time() - total_start
    
    print(f"\n📊 RESULTS:")
    print(f"⏰ Total time: {total_time:.1f} seconds")
    print(f"💬 Conversation entries: {len(shared_state['conversation_history'])}")
    print(f"✅ Agents completed: {len(shared_state['agent_states'])}")
    
    # Show the conversation history
    print(f"\n📝 Conversation History:")
    for i, entry in enumerate(shared_state['conversation_history']):
        print(f"  {i+1}. {entry['agent']}: {entry['response'][:60]}...")
    
    # This should always be consistent
    assert len(shared_state['conversation_history']) == 3
    assert len(shared_state['agent_states']) == 3
    print(f"\n✅ All data is consistent (but took {total_time:.1f}s)")


if __name__ == "__main__":
    run_sequential_agents()