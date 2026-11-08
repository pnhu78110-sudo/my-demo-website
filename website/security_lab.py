"""Intentionally vulnerable examples for local security practice."""

import sqlite3

from django.conf import settings
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render


def require_lab():
    if not settings.DEBUG:
        raise Http404


def reflected_xss(request):
    require_lab()

    # SECURITY LAB: user input is deliberately rendered without HTML escaping.
    return render(
        request,
        "website/security_lab_xss.html",
        {"message": request.GET.get("message", "")},
    )


def sql_injection(request):
    require_lab()
    # SECURITY LAB: a disposable database contains only fictional records.
    connection = sqlite3.connect(":memory:")
    try:
        connection.execute("CREATE TABLE accounts (username TEXT, role TEXT)")
        connection.executemany(
            "INSERT INTO accounts VALUES (?, ?)",
            [("alice", "reader"), ("admin", "administrator")],
        )
        username = request.GET.get("username", "alice")
        # INTENTIONAL SQL INJECTION: fix by binding username as a parameter.
        query = "SELECT username, role FROM accounts WHERE username = '%s'" % username
        try:
            rows = connection.execute(query).fetchall()
        except sqlite3.Error:
            return JsonResponse({"error": "Invalid lab query"}, status=400)
        return JsonResponse({"accounts": rows})
    finally:
        connection.close()


def insecure_invoice(request, invoice_id):
    require_lab()
    invoices = {
        1: {"owner": "alice", "amount": 100},
        2: {"owner": "bob", "amount": 900},
    }
    if invoice_id not in invoices:
        raise Http404
    # INTENTIONAL IDOR: Alice can access Bob's fictional invoice by changing ID.
    # Fix by checking authenticated ownership before returning a record.
    return JsonResponse({"demo_user": "alice", "invoice": invoices[invoice_id]})


def open_redirect(request):
    require_lab()
    # INTENTIONAL OPEN REDIRECT: fix by validating the destination host/scheme.
    return HttpResponseRedirect(request.GET.get("next", "/security-lab/xss/"))


def exposed_config(request):
    require_lab()
    # INTENTIONAL INFORMATION DISCLOSURE: fictional credentials only.
    # Fix by removing public configuration endpoints and keeping secrets private.
    return JsonResponse({
        "database_user": "lab_admin",
        "database_password": "DEMO_ONLY_not_a_real_password",
        "api_key": "DEMO_ONLY_not_a_real_api_key",
    })
