import json

from django.http import Http404
from django.test import RequestFactory, SimpleTestCase, override_settings

from .security_lab import (
    reflected_xss, sql_injection, insecure_invoice, open_redirect, exposed_config,
)


class SecurityLabTests(SimpleTestCase):
    @override_settings(DEBUG=True)
    def test_lab_reflects_unescaped_html(self):
        payload = '<img src=x onerror="alert(1)">'
        response = reflected_xss(RequestFactory().get("/", {"message": payload}))
        self.assertContains(response, '<div id="result">' + payload + "</div>")
        self.assertContains(response, "&lt;img src=x onerror=&quot;alert(1)&quot;&gt;")

    @override_settings(DEBUG=False)
    def test_lab_is_unavailable_outside_debug(self):
        for view, args in [
            (reflected_xss, ()), (sql_injection, ()),
            (insecure_invoice, (2,)), (open_redirect, ()), (exposed_config, ()),
        ]:
            with self.subTest(view=view.__name__), self.assertRaises(Http404):
                view(RequestFactory().get("/"), *args)

    @override_settings(DEBUG=True)
    def test_sql_injection_returns_other_accounts(self):
        normal = sql_injection(RequestFactory().get("/", {"username": "alice"}))
        self.assertEqual(len(json.loads(normal.content)["accounts"]), 1)
        injected = sql_injection(RequestFactory().get("/", {"username": "' OR '1'='1"}))
        self.assertEqual(len(json.loads(injected.content)["accounts"]), 2)

    @override_settings(DEBUG=True)
    def test_invoice_id_exposes_another_demo_users_invoice(self):
        response = insecure_invoice(RequestFactory().get("/"), 2)
        self.assertEqual(json.loads(response.content)["invoice"]["owner"], "bob")

    @override_settings(DEBUG=True)
    def test_redirect_accepts_external_destination(self):
        response = open_redirect(RequestFactory().get("/", {"next": "https://example.com/"}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "https://example.com/")

    @override_settings(DEBUG=True)
    def test_config_exposes_fake_credentials(self):
        response = exposed_config(RequestFactory().get("/"))
        self.assertEqual(json.loads(response.content)["database_password"], "DEMO_ONLY_not_a_real_password")
