import unittest

from iam_simulator import POLICIES, check_permission


class CheckPermissionTests(unittest.TestCase):
    def test_developer_can_read_logs(self):
        self.assertEqual(
            check_permission("developer", "read_logs", "logs", POLICIES),
            "ALLOW",
        )

    def test_developer_cannot_delete_database(self):
        self.assertEqual(
            check_permission(
                "developer", "delete_resource", "database", POLICIES
            ),
            "DENY",
        )

    def test_explicit_deny_overrides_admin_allow(self):
        self.assertEqual(
            check_permission("admin", "delete_resource", "database", POLICIES),
            "DENY",
        )

    def test_admin_can_create_compute_resource(self):
        self.assertEqual(
            check_permission("admin", "create_resource", "compute", POLICIES),
            "ALLOW",
        )

    def test_unlisted_user_is_denied(self):
        self.assertEqual(
            check_permission("unknown", "read_logs", "logs", POLICIES),
            "DENY",
        )

    def test_action_and_resource_wildcards(self):
        test_policies = {
            "operator": [
                {
                    "Effect": "Allow",
                    "Action": ["read_*", "list_*"],
                    "Resource": "project-*",
                }
            ]
        }
        self.assertEqual(
            check_permission(
                "operator", "read_logs", "project-alpha", test_policies
            ),
            "ALLOW",
        )
        self.assertEqual(
            check_permission(
                "operator", "delete_logs", "project-alpha", test_policies
            ),
            "DENY",
        )


if __name__ == "__main__":
    unittest.main()
