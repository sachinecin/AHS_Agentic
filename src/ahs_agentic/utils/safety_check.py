"""
Safety check decorator for write operations and API calls.
"""
import functools
from typing import Callable, Optional

def safety_check(
    action_description: Optional[str] = None,
    require_confirmation: bool = True
):
    """
    Decorator that prompts user for confirmation before executing write/API operations.
    
    Usage:
        @safety_check(action_description="Delete all records from database")
        def dangerous_operation():
            # Your code here
            pass
        
        @safety_check()  # Uses function name as description
        async def api_call():
            # Your code here
            pass
    
    Args:
        action_description: Human-readable description of the action
        require_confirmation: If False, only logs warning without prompting
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            description = action_description or f"Execute {func.__name__}"
            
            if require_confirmation:
                if not _prompt_user_confirmation(description):
                    print("❌ Operation cancelled by user.")
                    return None
            else:
                print(f"⚠️  Warning: About to {description}")
            
            print(f"✅ Executing: {description}")
            return await func(*args, **kwargs)
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            description = action_description or f"Execute {func.__name__}"
            
            if require_confirmation:
                if not _prompt_user_confirmation(description):
                    print("❌ Operation cancelled by user.")
                    return None
            else:
                print(f"⚠️  Warning: About to {description}")
            
            print(f"✅ Executing: {description}")
            return func(*args, **kwargs)
        
        # Return appropriate wrapper
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator

def _prompt_user_confirmation(action: str) -> bool:
    """Prompt user for Y/N confirmation."""
    print("\n" + "="*60)
    print("🚨 SAFETY CHECK REQUIRED")
    print("="*60)
    print(f"Action: {action}")
    print("="*60)
    
    while True:
        response = input("Proceed? (Y/N): ").strip().upper()
        if response in ['Y', 'YES']:
            return True
        elif response in ['N', 'NO']:
            return False
        else:
            print("Invalid input. Please enter Y or N.")
