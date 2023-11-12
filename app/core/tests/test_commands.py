"""
Test custom Django management commands.
"""
from unittest.mock import patch

# Import the generic OperationalError from Django
from django.db.utils import OperationalError
from django.test import SimpleTestCase
from django.core.management import call_command

@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        # Use the generic OperationalError from Django
        patched_check.side_effect = [OperationalError] * 5 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
