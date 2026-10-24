"""兼容性验收：使用临时设置目录，不读写真实用户设置，也不发送输入。"""
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import admin_util
import user_settings
from flow.core import Graph
from version import APP_NAME, __version__


class BrandingCompatibility(unittest.TestCase):
    def test_legacy_preferences_are_preserved_on_first_save(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {"APPDATA": tmp}):
            legacy = Path(tmp) / "AOE4AutoVillager" / "settings.json"
            legacy.parent.mkdir()
            original = {"last_flow": "flows/combined.flow.json", "overlay_bg": .35}
            legacy.write_text(json.dumps(original), encoding="utf-8")
            self.assertEqual(user_settings.load_settings(), original)
            updated = user_settings.update_settings(overlay_bg=.5)
            self.assertEqual(updated["last_flow"], original["last_flow"])
            self.assertEqual(json.loads(legacy.read_text("utf-8")), original)
            self.assertEqual(Path(user_settings.settings_path()).parent.name, "AoE4Flow")
            user_settings.save_settings({})
            self.assertEqual(user_settings.load_settings(), {})

    def test_old_and_new_no_elevation_launchers(self):
        for key in ("AOE4_NO_ELEVATE", "AOE4_FLOW_NO_ELEVATE"):
            with self.subTest(key=key), patch.dict(os.environ, {key: "1"}, clear=True), \
                    patch.object(admin_util, "is_admin", return_value=False), \
                    patch.object(admin_util, "relaunch_as_admin") as relaunch:
                self.assertFalse(admin_util.ensure_admin_or_warn(prompt=lambda message: None))
                relaunch.assert_not_called()

    def test_legacy_flow_format_still_loads(self):
        import flow.nodes  # noqa: F401
        graph = Graph.load("flows/combined.flow.json")
        self.assertGreater(len(graph.nodes), 30)

    def test_toolbar_readable_default_and_saved_transparency(self):
        from flow.editor.webhost import Api
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {"APPDATA": tmp}):
            self.assertTrue(Api()._overlay_opaque)
            legacy = Path(tmp) / "AOE4AutoVillager" / "settings.json"
            legacy.parent.mkdir()
            legacy.write_text('{"overlay_opaque": false}', encoding="utf-8")
            self.assertFalse(Api()._overlay_opaque)
            user_settings.save_settings({"overlay_opaque": False})
            self.assertFalse(Api()._overlay_opaque)

    def test_public_identity(self):
        self.assertEqual(__version__, "3.3.0")
        self.assertEqual(APP_NAME, "AoE4 Flow · 帝国时代 4 自动化助手")


if __name__ == "__main__":
    unittest.main(verbosity=2)
