import unittest
from serum import mock, Component, inject, Environment
from serum.exceptions import NoEnvironment


class SomeComponent(Component):
    def method(self):
        return 'some value'


class Depenedent:
    some_component = inject(SomeComponent)


class MockTests(unittest.TestCase):
    def test_mock_always_replaces_component(self):
        with Environment():
            some_component_mock = mock(SomeComponent)
            some_component_mock.method.return_value = 'some other value'
            d = Depenedent()
            self.assertIs(d.some_component, some_component_mock)
            self.assertEqual(d.some_component.method(), 'some other value')

    def test_mocks_are_reset_after_context_exit(self):
        with Environment():
            some_component_mock = mock(SomeComponent)
            d = Depenedent()
            self.assertIs(some_component_mock, d.some_component)

        with Environment():
            d = Depenedent()
            self.assertIsNot(some_component_mock, d.some_component)
            self.assertIsInstance(d.some_component, SomeComponent)

    def test_cant_register_mocks_outside_environment(self):
        with self.assertRaises(NoEnvironment):
            mock(SomeComponent)
