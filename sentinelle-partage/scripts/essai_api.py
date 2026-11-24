#!/usr/bin/env python3
"""Mesure le temps de réponse du service sur N appels à /noter.

Usage : python scripts/essai_api.py [N] [adresse]      (défaut : 1000 appels, http://127.0.0.1:8000)
Le service doit tourner : uvicorn sentinelle.api:app --port 8000
"""
import json
import statistics
import sys
import time
import urllib.request

n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
base = sys.argv[2] if len(sys.argv) > 2 else "http://127.0.0.1:8000"


def appeler(chemin, corps=None):
    donnees = None if corps is None else json.dumps(corps).encode()
    requete = urllib.request.Request(base + chemin, data=donnees, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(requete, timeout=10) as reponse:
        return json.load(reponse)


print("Service :", appeler("/sante"))
temps, decisions = [], {}
for i in range(n):
    t0 = time.perf_counter()
    v = appeler("/noter", {"expediteur": f"ESSAI{i % 50}", "destinataire": f"DEST{i % 200}", "montant": 10000 + 500 * i})
    temps.append((time.perf_counter() - t0) * 1000)
    decisions[v["decision"]] = decisions.get(v["decision"], 0) + 1
temps.sort()
print(f"{n} appels : médiane {statistics.median(temps):.1f} ms, 95e centile {temps[int(0.95 * n) - 1]:.1f} ms, "
      f"maximum {temps[-1]:.1f} ms")
print("Décisions :", decisions)
