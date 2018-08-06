import json
import unittest

from assertpy import assert_that

from audiopyle.commons.models.metric import MetricDefinition, MetricValue
from audiopyle.commons.models.result import DataStats


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


class MetricValueModelTest(unittest.TestCase):
    def setUp(self):
        self.data_stats = DataStats(minimum=0.03276, maximum=0.44241, median=0.22399, mean=0.21448,
                                    standard_deviation=0.12923, variance=0.01670)
        self.metric_definition = MetricDefinition(name="my_metric",
                                                  plugin_key="vamp-example-plugins:amplitudefollower:amplitude",
                                                  function="none", kwargs={"param1": 2.0})
        self.metric_value = MetricValue("0f961f20-b036-5740-b526-013523dd88c7", self.metric_definition,
                                        self.data_stats)

    def test_should_turn_into_serializable_form_and_back(self):
        serializable_form = self.metric_value.to_serializable()
        assert_that(serializable_form).is_not_none()
        assert_that(serializable_form["task_id"]).is_equal_to("0f961f20-b036-5740-b526-013523dd88c7")
        assert_that(serializable_form["stats"]["minimum"]).is_equal_to(0.03276)
        assert_that(serializable_form["definition"]["name"]).is_equal_to("my_metric")

        deserialized_form = MetricValue.from_serializable(serializable_form)
        assert_that(deserialized_form).is_equal_to(self.metric_value)

    def test_should_serialize_to_json_and_back_without_errors(self):
        json_form = json.dumps(self.metric_value.to_serializable())
        assert_that(json_form).is_not_empty()

        back_to_object = MetricValue.from_serializable(json.loads(json_form))
        assert_that(back_to_object).is_equal_to(self.metric_value)
