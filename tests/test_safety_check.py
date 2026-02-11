"""
Tests for safety_check module.
"""
import pytest
from unittest.mock import patch, MagicMock
from ahs_agentic.utils.safety_check import safety_check, _prompt_user_confirmation


class TestSafetyCheck:
    """Test suite for safety check decorator."""
    
    @pytest.mark.asyncio
    @patch('ahs_agentic.utils.safety_check._prompt_user_confirmation')
    async def test_async_function_user_accepts(self, mock_prompt):
        """Test async function when user accepts."""
        mock_prompt.return_value = True
        
        @safety_check(action_description="Test dangerous operation")
        async def dangerous_async_operation():
            return "operation_completed"
        
        result = await dangerous_async_operation()
        
        assert result == "operation_completed"
        mock_prompt.assert_called_once_with("Test dangerous operation")
    
    @pytest.mark.asyncio
    @patch('ahs_agentic.utils.safety_check._prompt_user_confirmation')
    async def test_async_function_user_declines(self, mock_prompt):
        """Test async function when user declines."""
        mock_prompt.return_value = False
        
        @safety_check(action_description="Test dangerous operation")
        async def dangerous_async_operation():
            return "operation_completed"
        
        result = await dangerous_async_operation()
        
        assert result is None
        mock_prompt.assert_called_once_with("Test dangerous operation")
    
    @patch('ahs_agentic.utils.safety_check._prompt_user_confirmation')
    def test_sync_function_user_accepts(self, mock_prompt):
        """Test sync function when user accepts."""
        mock_prompt.return_value = True
        
        @safety_check(action_description="Test dangerous operation")
        def dangerous_sync_operation():
            return "operation_completed"
        
        result = dangerous_sync_operation()
        
        assert result == "operation_completed"
        mock_prompt.assert_called_once_with("Test dangerous operation")
    
    @patch('ahs_agentic.utils.safety_check._prompt_user_confirmation')
    def test_sync_function_user_declines(self, mock_prompt):
        """Test sync function when user declines."""
        mock_prompt.return_value = False
        
        @safety_check(action_description="Test dangerous operation")
        def dangerous_sync_operation():
            return "operation_completed"
        
        result = dangerous_sync_operation()
        
        assert result is None
        mock_prompt.assert_called_once_with("Test dangerous operation")
    
    @pytest.mark.asyncio
    @patch('ahs_agentic.utils.safety_check._prompt_user_confirmation')
    async def test_default_description_async(self, mock_prompt):
        """Test default description uses function name (async)."""
        mock_prompt.return_value = True
        
        @safety_check()
        async def my_test_function():
            return "completed"
        
        result = await my_test_function()
        
        assert result == "completed"
        mock_prompt.assert_called_once_with("Execute my_test_function")
    
    @patch('ahs_agentic.utils.safety_check._prompt_user_confirmation')
    def test_default_description_sync(self, mock_prompt):
        """Test default description uses function name (sync)."""
        mock_prompt.return_value = True
        
        @safety_check()
        def my_test_function():
            return "completed"
        
        result = my_test_function()
        
        assert result == "completed"
        mock_prompt.assert_called_once_with("Execute my_test_function")
    
    @pytest.mark.asyncio
    async def test_no_confirmation_required_async(self, capsys):
        """Test async function without confirmation requirement."""
        @safety_check(action_description="Test operation", require_confirmation=False)
        async def operation_without_confirmation():
            return "completed"
        
        result = await operation_without_confirmation()
        
        assert result == "completed"
        captured = capsys.readouterr()
        assert "⚠️  Warning: About to Test operation" in captured.out
        assert "✅ Executing: Test operation" in captured.out
    
    def test_no_confirmation_required_sync(self, capsys):
        """Test sync function without confirmation requirement."""
        @safety_check(action_description="Test operation", require_confirmation=False)
        def operation_without_confirmation():
            return "completed"
        
        result = operation_without_confirmation()
        
        assert result == "completed"
        captured = capsys.readouterr()
        assert "⚠️  Warning: About to Test operation" in captured.out
        assert "✅ Executing: Test operation" in captured.out
    
    @pytest.mark.asyncio
    @patch('ahs_agentic.utils.safety_check._prompt_user_confirmation')
    async def test_function_with_arguments(self, mock_prompt):
        """Test decorated function with arguments."""
        mock_prompt.return_value = True
        
        @safety_check(action_description="Process data")
        async def process_data(data, multiplier=2):
            return data * multiplier
        
        result = await process_data(5, multiplier=3)
        
        assert result == 15
    
    @patch('ahs_agentic.utils.safety_check._prompt_user_confirmation')
    def test_function_preserves_name(self, mock_prompt):
        """Test that decorator preserves function name."""
        mock_prompt.return_value = True
        
        @safety_check(action_description="Test")
        def my_original_function():
            pass
        
        assert my_original_function.__name__ == "my_original_function"


class TestPromptUserConfirmation:
    """Test the user confirmation prompt function."""
    
    @patch('builtins.input', return_value='Y')
    def test_user_confirms_with_Y(self, mock_input):
        """Test user confirmation with 'Y'."""
        result = _prompt_user_confirmation("Test action")
        assert result is True
    
    @patch('builtins.input', return_value='YES')
    def test_user_confirms_with_YES(self, mock_input):
        """Test user confirmation with 'YES'."""
        result = _prompt_user_confirmation("Test action")
        assert result is True
    
    @patch('builtins.input', return_value='y')
    def test_user_confirms_with_lowercase_y(self, mock_input):
        """Test user confirmation with lowercase 'y'."""
        result = _prompt_user_confirmation("Test action")
        assert result is True
    
    @patch('builtins.input', return_value='N')
    def test_user_declines_with_N(self, mock_input):
        """Test user decline with 'N'."""
        result = _prompt_user_confirmation("Test action")
        assert result is False
    
    @patch('builtins.input', return_value='NO')
    def test_user_declines_with_NO(self, mock_input):
        """Test user decline with 'NO'."""
        result = _prompt_user_confirmation("Test action")
        assert result is False
    
    @patch('builtins.input', side_effect=['invalid', 'maybe', 'Y'])
    def test_invalid_input_retries(self, mock_input):
        """Test that invalid input causes retry until valid input."""
        result = _prompt_user_confirmation("Test action")
        assert result is True
        assert mock_input.call_count == 3
    
    @patch('builtins.input', return_value='  yes  ')
    def test_strips_whitespace(self, mock_input):
        """Test that input is stripped of whitespace."""
        result = _prompt_user_confirmation("Test action")
        assert result is True
