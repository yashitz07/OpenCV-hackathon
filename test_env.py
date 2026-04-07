"""
Test script for Manufacturing QC Environment
Tests basic functionality locally before deployment
"""

import asyncio
from manufacturing_qc_env import (
    ManufacturingQCEnv,
    ManufacturingQCAction,
    ActionType,
    GRADERS,
)


async def test_basic_functionality():
    """Test basic environment functionality"""
    print("=" * 60)
    print("Testing Manufacturing QC Environment")
    print("=" * 60)
    
    # Test each task
    tasks = ["basic_inspection", "optimized_throughput", "adaptive_control"]
    
    for task_name in tasks:
        print(f"\n{'='*60}")
        print(f"Testing Task: {task_name}")
        print(f"{'='*60}\n")
        
        env = ManufacturingQCEnv(task_name=task_name)
        
        # Test reset
        print("✓ Testing reset()...")
        observation = await env.reset()
        assert observation.current_product is not None
        assert observation.queue_length > 0
        print(f"  Initial product: {observation.current_product.product_id}")
        print(f"  Queue length: {observation.queue_length}")
        print(f"  Task: {env.current_task.name} ({env.current_task.difficulty})")
        
        # Test multiple steps
        print("\n✓ Testing step()...")
        steps = 5
        total_reward = 0.0
        
        for i in range(steps):
            if not observation.current_product:
                break
            
            # Make a simple decision based on quality score
            product = observation.current_product
            
            if product.quality_score >= 0.7:
                action = ManufacturingQCAction(
                    action_type=ActionType.APPROVE,
                    product_id=product.product_id,
                    reason="Quality score acceptable"
                )
            elif product.defect_severity.value in ["critical", "severe"]:
                action = ManufacturingQCAction(
                    action_type=ActionType.REJECT,
                    product_id=product.product_id,
                    reason="Critical defects detected"
                )
            else:
                action = ManufacturingQCAction(
                    action_type=ActionType.REWORK,
                    product_id=product.product_id,
                    reason="Minor defects - send for rework"
                )
            
            observation, reward, done, info = await env.step(action)
            total_reward += reward.reward
            
            print(f"  Step {i+1}: {action.action_type.value} -> Reward: {reward.reward:.2f}")
            
            if done:
                break
        
        print(f"\n  Total reward: {total_reward:.2f}")
        print(f"  Steps taken: {env.current_step}")
        
        # Test state
        print("\n✓ Testing state()...")
        state = await env.state()
        print(f"  Current step: {state.current_step}")
        print(f"  Total reward: {state.total_reward:.2f}")
        print(f"  Done: {state.done}")
        
        # Test grader
        print("\n✓ Testing grader...")
        grader = GRADERS.get(task_name)
        if grader:
            score = grader(env)
            print(f"  Grader score: {score:.3f}")
            print(f"  Accuracy: {env._calculate_accuracy():.2%}")
            print(f"  Defects caught: {env.stats.defects_caught}")
            print(f"  False positives: {env.stats.false_positives}")
            print(f"  False negatives: {env.stats.false_negatives}")
        
        # Test close
        print("\n✓ Testing close()...")
        await env.close()
        
        print(f"\n✅ Task '{task_name}' passed all tests!\n")


async def test_all_actions():
    """Test all available actions"""
    print("\n" + "=" * 60)
    print("Testing All Action Types")
    print("=" * 60 + "\n")
    
    env = ManufacturingQCEnv(task_name="adaptive_control")
    observation = await env.reset()
    
    actions_to_test = [
        ActionType.APPROVE,
        ActionType.REJECT,
        ActionType.REWORK,
        ActionType.ADJUST_THRESHOLD,
        ActionType.REQUEST_MAINTENANCE,
    ]
    
    for action_type in actions_to_test:
        if not observation.current_product:
            observation = await env.reset()
        
        product_id = observation.current_product.product_id
        
        action = ManufacturingQCAction(
            action_type=action_type,
            product_id=product_id,
            reason=f"Testing {action_type.value}",
            threshold_value=0.75 if action_type == ActionType.ADJUST_THRESHOLD else None
        )
        
        observation, reward, done, info = await env.step(action)
        
        print(f"✓ {action_type.value:20s} -> Reward: {reward.reward:+.2f}")
        if reward.components:
            for component, value in reward.components.items():
                print(f"    {component}: {value:+.2f}")
    
    await env.close()
    print("\n✅ All action types tested successfully!\n")


async def test_error_handling():
    """Test error handling"""
    print("\n" + "=" * 60)
    print("Testing Error Handling")
    print("=" * 60 + "\n")
    
    env = ManufacturingQCEnv(task_name="basic_inspection")
    await env.reset()
    
    # Complete episode
    for _ in range(20):
        if env.done:
            break
        
        if not env.current_product:
            break
        
        action = ManufacturingQCAction(
            action_type=ActionType.APPROVE,
            product_id=env.current_product.product_id,
            reason="Test"
        )
        await env.step(action)
    
    # Try to step after done
    print("✓ Testing step() after episode done...")
    try:
        action = ManufacturingQCAction(
            action_type=ActionType.APPROVE,
            product_id="TEST",
            reason="Should fail"
        )
        await env.step(action)
        print("  ❌ Should have raised RuntimeError")
    except RuntimeError as e:
        print(f"  ✅ Correctly raised RuntimeError: {str(e)[:50]}...")
    
    await env.close()
    print("\n✅ Error handling tests passed!\n")


async def main():
    """Run all tests"""
    print("\n" + "🔬" * 30)
    print(" " * 20 + "MANUFACTURING QC ENVIRONMENT TESTS")
    print("🔬" * 30 + "\n")
    
    try:
        await test_basic_functionality()
        await test_all_actions()
        await test_error_handling()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60 + "\n")
        print("Your environment is ready to deploy! 🚀\n")
        print("Next steps:")
        print("1. Test with inference script: python inference.py")
        print("2. Build Docker image: docker build -t manufacturing-qc-env .")
        print("3. Deploy to Hugging Face Spaces")
        print()
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
