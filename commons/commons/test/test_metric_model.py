import json
import unittest

from assertpy import assert_that

from commons.models.metric import MetricDefinition


class MetricDefinitionModelTest(unittest.TestCase):
    def setUp(self):
        self.none_metric_definition_creation_dict = {'name': 'my_metric',
                                                     'plugin_key': 'vamp-example-plugins:amplitudefollower:amplitude',
                                                     'function': 'none', 'kwargs': {}}
        self.none_metric_definition = MetricDefinition(**self.none_metric_definition_creation_dict)

    def test_should_turn_into_serializable_form_and_back(self):
        serializable_form = self.none_metric_definition.to_serializable()
        assert_that(serializable_form).is_not_none()
        assert_that(serializable_form["name"]).is_equal_to("my_metric")
        assert_that(serializable_form["kwargs"]).is_equal_to({})

        deserialized_form = MetricDefinition.from_serializable(serializable_form)
        assert_that(deserialized_form).is_equal_to(self.none_metric_definition)

    def test_should_serialize_to_json_and_back_without_errors(self):
        json_form = json.dumps(self.none_metric_definition.to_serializable())
        assert_that(json_form).is_not_empty()

        from_json_form = MetricDefinition.from_serializable(json.loads(json_form))
        assert_that(from_json_form).is_equal_to(self.none_metric_definition)
