import unittest

from src.configuration.infrastruture.loadjsonconfiguration import LoadJsonConfiguration


class LoadJsonConfigurationTest(unittest.TestCase):


    def test_load_conf_dict_simples_types(self):
        readconfig = LoadJsonConfiguration()
        original_conf = """{"int" : 1, "bool": true, "str" : "test" }"""
        result_conf = readconfig.load_from_str(original_conf)
        self.assertEqual(result_conf["int"],1)
        self.assertEqual(result_conf["bool"], True)
        self.assertEqual(result_conf["str"], "test")

    def test_load_conf_dict_with_environment(self):
        readconfig = LoadJsonConfiguration()
        original_conf = """{"environmentpathexample": "${ENV.PATH}"}"""
        result_conf = readconfig.load_from_str(original_conf)
        self.assertTrue(result_conf["environmentpathexample"] != "${ENV.PATH}")

    def test_load_conf_dict_with_simple_object(self):
        readconfig = LoadJsonConfiguration()
        original_conf = """{"test": "test", "object_ref" : "${test}"}"""
        result_conf = readconfig.load_from_str(original_conf)
        self.assertEqual(result_conf["test"], "test")
        self.assertEqual(result_conf["object_ref"],  result_conf["test"])

    def test_load_conf_dict_with_object_insede_object(self):
        readconfig = LoadJsonConfiguration()
        original_conf = """{"object": {"test":"test"}, "object_ref" : "${object.test}"}"""
        result_conf = readconfig.load_from_str(original_conf)
        self.assertEqual(result_conf["object"]["test"], "test")
        self.assertEqual(result_conf["object_ref"],  result_conf["object"]["test"])

    def test_load_conf_dict_with_reference_insede_object(self):
        readconfig = LoadJsonConfiguration()
        original_conf = """{
                            "object": {
                                "environmentpathexample":"${ENV.PATH}"
                            }, 
                            "object_ref" : {
                                "int" : 1,
                                 "object_environment_ref": "${object.environmentpathexample}"
                            }
                            }"""
        result_conf = readconfig.load_from_str(original_conf)
        self.assertTrue(result_conf["object"]["environmentpathexample"] != "${ENV.PATH}")
        self.assertEqual(result_conf["object"]["environmentpathexample"],  result_conf["object_ref"]["object_environment_ref"])


    def test_load_conf_dict_with_array(self):
        readconfig = LoadJsonConfiguration()
        original_conf = """{
                            "object": {
                                "environmentpathexample":"${ENV.PATH}"
                            }, 
                            "object_ref" : {
                                "int" : 1,
                                 "object_environment_ref": "${object.environmentpathexample}"
                            },
                            "array": [
                                {"test": 0},
                                {"test":"${ENV.PATH}"},
                                {"test": "${object_ref.int}"},
                                {"test": "${object_ref.object_environment_ref}"}
                            ]
                            }"""
        result_conf = readconfig.load_from_str(original_conf)
        self.assertTrue(result_conf["object"]["environmentpathexample"] != "${ENV.PATH}")
        self.assertEqual(result_conf["object"]["environmentpathexample"],  result_conf["object_ref"]["object_environment_ref"])
        self.assertEqual(result_conf["array"][0]["test"], 0)
        self.assertEqual(result_conf["array"][1]["test"],  result_conf["object_ref"]["object_environment_ref"])
        self.assertEqual(result_conf["array"][2]["test"], 1)
        self.assertEqual(result_conf["array"][3]["test"], result_conf["object_ref"]["object_environment_ref"])