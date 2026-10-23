import sys
import unittest
from hooks.path_firewall import check_path_permission
from hooks.webgl_playwright_gate import generate_webgl_assertion_script

class TestGovernanceHooks(unittest.TestCase):
    def test_path_firewall_allowed(self):
        # 允许的项目路径
        self.assertTrue(check_path_permission(r"C:\Users\Lenovo\Projects\hongyuanpai\app.js"))
        self.assertTrue(check_path_permission(r"./src/components/ThreeCanvas.vue"))

    def test_path_firewall_blocked(self):
        # 拦截的敏感与目录穿越路径
        self.assertFalse(check_path_permission(r"C:\Users\Lenovo\Desktop\secret.txt"))
        self.assertFalse(check_path_permission(r"C:\Users\Lenovo\Documents\private.pdf"))
        self.assertFalse(check_path_permission(r"..\..\Windows\System32\cmd.exe"))

    def test_webgl_assertion_script_integrity(self):
        script = generate_webgl_assertion_script()
        self.assertIn("CANVAS_ELEMENT_NOT_FOUND", script)
        self.assertIn("ZERO_RENDERED_TRIANGLES", script)
        self.assertIn("BLACK_SCREEN_RENDER_ERROR", script)

if __name__ == "__main__":
    unittest.main()
