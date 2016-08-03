import json
from stock_tracer.common import transaction
from stock_tracer.scheduler import UpdateQuoteAction
from stock_tracer.operation import AddScheduledAction
from stock_tracer.test.base import DBUnitTest

class TestAddScheduledAction(DBUnitTest):
    """TestAddScheduledAction"""

    def test_add_scheduled_action_succeed(self):
        """test_add_scheduled_action_succeed"""
        add_scheduled_action_op = AddScheduledAction(action_type='update_quote', interval_in_second=10)
        result = add_scheduled_action_op.run()
        result_json = json.loads(result)
        assert result_json['type'] == 'update_quote'
        assert result_json['interval_in_second'] == '10'

        with transaction() as tx:
            action = tx.query(UpdateQuoteAction).first()
            assert action
