"""Écran de démonstration de Sentinelle : `streamlit run demo/app.py`.

Le modèle n'est pas entraîné ici : l'écran charge modeles/sentinelle_v1.ubj par le même moteur
que le service (sentinelle/moteur.py) et calcule chaque score en direct.
"""
import hashlib
import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sentinelle import config                      # noqa: E402
from sentinelle.config import JOUR                 # noqa: E402
from sentinelle.magasin import Magasin             # noqa: E402
from sentinelle.moteur import ModeleAbsent, Moteur  # noqa: E402
from sentinelle.rejeu import magasin_depuis, rejouer  # noqa: E402

st.set_page_config(page_title="Sentinelle", page_icon="🛡️", layout="wide")

# ----------------------------------------------------------------------------- textes
CAS = {
    "arnaque": ("1. L'arnaque du « transfert par erreur »",
                "Un inconnu appelle : il aurait envoyé de l'argent par erreur et demande à être remboursé. "
                "Un faux SMS de dépôt arrive. La victime s'apprête à « rembourser » elle-même."),
    "collecteur": ("2. Le compte collecteur",
                   "Ce compte reçoit l'argent de plusieurs victimes en quelques heures, puis le fait sortir. "
                   "Une nouvelle victime s'apprête à lui envoyer de l'argent."),
    "tontine": ("3. La tontine (cas légitime)",
                "Chaque semaine, les mêmes membres cotisent auprès du même collecteur. Beaucoup d'entrées en "
                "peu de temps, comme une mule, mais ce n'en est pas une."),
    "commerce": ("4. Le petit commerce (cas légitime)",
                 "Une boutique encaisse de nombreux clients nouveaux, par petits montants. Un client paie."),
    "limite": ("5. La limite : une mule toute neuve",
               "Premier transfert d'une victime vers un compte qui n'a encore rien fait. Sentinelle lit le "
               "passé du compte ; ici, il n'y en a pas."),
}
SCENARIOS = {
    "fond": "Trafic normal PaySim", "fond_mule": "Passé normal d'une future mule",
    "L_commerce": "Petit commerce (légitime)", "L_etudiant": "Étudiant (légitime)",
    "L_nouveau": "Compte neuf ordinaire (légitime)", "L_tontine": "Tontine (légitime)",
    "S1_erreur": "Arnaque : transfert par erreur", "S2_faux_agent": "Arnaque : faux agent",
    "S3_collecteur": "Arnaque : compte collecteur", "S4_chaine": "Arnaque : chaîne de mules",
}
DECISIONS = {"laisser_passer": "Laisser passer", "alerter": "Alerter", "bloquer": "Bloquer"}
PRENOMS = ["Awa", "Kossi", "Mariam", "Yao", "Afi", "Sènan", "Fifamè", "Rachidi", "Bignon", "Codjo", "Dossou",
           "Edwige", "Fatou", "Gildas", "Hermine", "Ibrahim", "Jocelyne", "Koffi", "Latifa", "Modeste",
           "Nadège", "Olivier", "Pélagie", "Rodrigue", "Salimata", "Thierry", "Ulrich", "Victoire"]


def nom(compte):
    """Nom inventé et stable pour un identifiant de compte simulé."""
    compte = str(compte)
    if compte.startswith("A") and compte[1:].isdigit():
        return f"Agent de retrait •••{compte[-4:]}"
    h = int(hashlib.md5(compte.encode()).hexdigest(), 16)
    return f"{PRENOMS[h % len(PRENOMS)]} {'ABCDGHKLMNOSTZ'[(h // 97) % 14]}. •••{compte[-4:]}"


def argent(v):
    return f"{v:,.0f}".replace(",", " ") + " F"


def heure(t):
    t = int(t)
    return f"jour {t // JOUR + 1}, {t % JOUR // 3600:02d} h {t % 3600 // 60:02d}"


def pourcent(v, decimales=1):
    return "non mesuré" if v is None else f"{100 * v:.{decimales}f} %".replace(".", ",")


# ----------------------------------------------------------------------------- chargement
@st.cache_resource(show_spinner="Chargement du modèle...")
def charger():
    moteur = Moteur()
    d = config.MODELES
    historique = pd.read_csv(d / "demo_historique.csv")
    flux = pd.read_csv(d / "demo_flux.csv")
    cas = json.loads((d / "demo_cas.json").read_text(encoding="utf-8"))
    return moteur, historique, flux, cas


try:
    moteur, HISTORIQUE, FLUX, CAS_DONNEES = charger()
except (ModeleAbsent, FileNotFoundError) as erreur:
    st.error(f"Le modèle n'est pas encore intégré.\n\n{erreur}")
    st.code("python -m sentinelle.integrer     # si modeles/sentinelle_v1.ubj a été téléchargé\n"
            "python -m sentinelle.entrainer    # sinon, pour l'entraîner sur cette machine")
    st.stop()

etat = st.session_state


def afficher_verdict(v):
    texte = f"**{DECISIONS[v['decision']]}** · score {v['score']:.2f}\n\n{v['message']}"
    if v["raisons"]:
        texte += "\n\n" + "\n".join(f"- {r[0].upper()}{r[1:]}" for r in v["raisons"])
    {"bloquer": st.error, "alerter": st.warning, "laisser_passer": st.success}[v["decision"]](texte)


def tableau_signaux(v):
    return pd.DataFrame({"signal": list(v["signaux"]), "valeur": [round(x, 3) for x in v["signaux"].values()]})


# ----------------------------------------------------------------------------- en-tête
st.title("🛡️ Sentinelle")
st.caption("Avant que l'expéditeur confirme un transfert instantané, Sentinelle note le compte destinataire "
           "et dit pourquoi. Une fois confirmé, le transfert est irrévocable.")
with st.sidebar:
    st.subheader("Le modèle chargé")
    st.write(f"**Origine :** {moteur.meta.get('origine', 'inconnue')}")
    st.write(f"**Signaux lus :** {len(moteur.signaux)}")
    st.write(f"**Seuil d'alerte :** {moteur.seuil_alerte:.3f}")
    st.write(f"**Seuil de blocage :** {moteur.seuil_blocage:.3f}")
    st.divider()
    st.caption("Données simulées : PaySim comme trafic de fond, plus nos scénarios d'arnaque injectés. "
               "Aucune connexion à la vraie plateforme PI-SPI. Les montants suivent PaySim, dont la monnaie "
               "est masquée ; « F » est une commodité d'affichage. Les noms sont inventés.")

onglet_cas, onglet_flux, onglet_bac, onglet_mesures = st.tabs(
    ["L'arnaque en direct", "Une journée rejouée", "Bac à sable", "Mesures et limites"])

# ----------------------------------------------------------------------------- 1. les cas
with onglet_cas:
    if not CAS_DONNEES:
        st.info("Aucun cas n'a été préparé pour ce modèle.")
    else:
        par_id = {c["id"]: c for c in CAS_DONNEES}
        ident = st.radio("Situation", list(par_id), format_func=lambda i: CAS[i][0])
        cas = par_id[ident]
        st.write(CAS[ident][1])
        if f"magasin_{ident}" not in etat:
            etat[f"magasin_{ident}"] = Magasin().charger(cas["historique"])
        magasin = etat[f"magasin_{ident}"]
        cle_issue = f"issue_{ident}"

        def fixer(valeur, cle=cle_issue):
            etat[cle] = valeur

        gauche, droite = st.columns(2)
        with gauche:
            st.subheader("Le téléphone de l'expéditeur")
            actif = st.toggle("Sentinelle activée", value=True, key=f"actif_{ident}")
            montant = st.number_input("Montant à envoyer", min_value=100.0, value=float(round(cas["montant"])),
                                      step=1000.0, format="%.0f", key=f"montant_{ident}")
            st.markdown(f"**De :** {nom(cas['src'])}  \n**Vers :** {nom(cas['dst'])}  \n**Quand :** {heure(cas['t'])}")
            st.caption("PI-SPI affiche déjà le nom et le pays du destinataire. Cela ne dit rien du "
                       "comportement du compte.")
            verdict = moteur.noter(magasin, cas["src"], cas["dst"], montant, cas["t"])
            if actif:
                afficher_verdict(verdict)
            else:
                st.info("Sans Sentinelle : rien ne s'affiche entre le nom du destinataire et la confirmation.")
            bloque = actif and verdict["decision"] == "bloquer"
            b1, b2, b3 = st.columns(3)
            b1.button("Confirmer", key=f"confirmer_{ident}", type="primary", disabled=bloque,
                      on_click=fixer, args=("confirme",))
            b2.button("Annuler", key=f"annuler_{ident}", on_click=fixer, args=("annule",))
            b3.button("Recommencer", key=f"recommencer_{ident}", on_click=fixer, args=(None,))
            if bloque:
                st.caption("Le transfert est bloqué : l'expéditeur ne peut pas confirmer.")

        with droite:
            st.subheader("Ce que Sentinelle lit sur le compte destinataire")
            r = magasin.resume(cas["dst"], cas["t"])
            if not r["connu"] or r["anciennete_jours"] is None:
                st.write("Aucune activité connue avant ce transfert.")
            else:
                m1, m2, m3 = st.columns(3)
                m1.metric("Actif depuis", f"{r['anciennete_jours']:.0f} j")
                m2.metric("Transferts reçus", r["transferts_recus"])
                m3.metric("Sorties rapides", r["sorties_rapides"], help="Fonds ressortis moins de 30 minutes après une entrée")
                st.write(f"Reçu au total : {argent(r['somme_recue'])}. Ressorti : {argent(r['somme_sortie'])}.")
            st.metric("Score de risque", f"{verdict['score']:.2f}",
                      help=f"Alerte à partir de {moteur.seuil_alerte:.2f}, blocage à partir de {moteur.seuil_blocage:.2f}")
            st.caption(f"Calculé en {verdict['latence_ms']:.1f} ms sur cet ordinateur, sans GPU.")
            with st.expander("Les signaux donnés au modèle"):
                st.dataframe(tableau_signaux(verdict), hide_index=True)

        issue = etat.get(cle_issue)
        if issue:
            st.divider()
            st.subheader("La suite")
            fraude = bool(cas["fraude"])
            if issue == "confirme" and fraude:
                echelle = montant / cas["montant"]
                for t, type_, somme, src, dst in cas["suite"]:
                    minutes = max(1, round((t - cas["t"]) / 60))
                    action = "retrait en espèces chez un agent" if type_ == "CASH_OUT" else f"transfert vers {nom(dst)}"
                    st.write(f"**+ {minutes} min** · {nom(src)} : {action}, {argent(somme * echelle)}")
                if not cas["suite"]:
                    st.write("Le compte garde l'argent pour l'instant : il attend d'autres victimes avant de retirer.")
                st.error(f"Argent perdu : {argent(montant)}. Un transfert confirmé ne peut plus être annulé.")
            elif issue == "confirme":
                st.success("Transfert arrivé. C'était un transfert normal.")
            elif fraude:
                st.success(f"{argent(montant)} sauvés : le transfert n'est jamais parti.")
            else:
                st.warning("Un transfert normal a été annulé : c'est une fausse alerte, le coût à surveiller.")
            st.caption("Dans les données simulées, ce transfert est "
                       + ("une arnaque." if fraude else "légitime.")
                       + f" Scénario : {SCENARIOS.get(cas['scen'], cas['scen'])}.")

# ----------------------------------------------------------------------------- 2. le flux
with onglet_flux:
    st.write("Tous les transferts du premier jour de test, dans l'ordre où ils arrivent. Le modèle ne les a "
             "jamais vus. Chaque transfert est noté avant d'être enregistré, comme le ferait le service.")
    if "flux_magasin" not in etat:
        with st.spinner("Chargement de l'historique des comptes..."):
            etat.update(flux_magasin=magasin_depuis(HISTORIQUE), flux_position=0, flux_verdicts=[])

    def avancer(nb):
        verdicts, etat["flux_position"] = rejouer(moteur, etat["flux_magasin"], FLUX, etat["flux_position"], nb)
        etat["flux_verdicts"] += verdicts

    def recommencer():
        for cle in ("flux_magasin", "flux_position", "flux_verdicts"):
            etat.pop(cle, None)

    c1, c2, c3 = st.columns(3)
    fini = etat["flux_position"] >= len(FLUX)
    c1.button("Jouer 100 transferts", type="primary", disabled=fini, on_click=avancer, args=(100,))
    c2.button("Jouer toute la journée", disabled=fini, on_click=avancer, args=(None,))
    c3.button("Revenir au début", on_click=recommencer)
    st.progress(min(1.0, etat["flux_position"] / max(1, len(FLUX))),
                text=f"{len(etat['flux_verdicts'])} transferts notés")

    if etat["flux_verdicts"]:
        v = pd.DataFrame(etat["flux_verdicts"])
        v["signale"] = v["decision"] != "laisser_passer"
        victimes, sains = v[v["victime"]], v[v["fraude"] == 0]
        perdu_sans, perdu_avec = victimes["montant"].sum(), victimes.loc[~victimes["signale"], "montant"].sum()
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Alertes et blocages", int(v["signale"].sum()))
        k2.metric("Transferts de victimes signalés", f"{int(victimes['signale'].sum())} sur {len(victimes)}")
        k3.metric("Fausses alertes", f"{int(sains['signale'].sum())} sur {len(sains)}")
        k4.metric("Dont blocages", int((v["decision"] == "bloquer").sum()))
        a1, a2 = st.columns(2)
        a1.metric("Sans Sentinelle, envoyé à des fraudeurs", argent(perdu_sans))
        a2.metric("Avec Sentinelle", argent(perdu_avec),
                  delta=f"-{argent(perdu_sans - perdu_avec)}" if perdu_sans > perdu_avec else None, delta_color="inverse")
        st.caption("Hypothèse : chaque expéditeur alerté renonce à son transfert. Seul le premier maillon est "
                   "compté, c'est-à-dire l'argent envoyé par une victime. Les transferts entre comptes "
                   "complices ne sont pas recomptés.")
        st.subheader("Dernières alertes")
        alertes = v[v["signale"]].tail(15).iloc[::-1]
        if alertes.empty:
            st.write("Aucune alerte pour l'instant.")
        else:
            st.dataframe(pd.DataFrame({
                "Quand": alertes["t"].map(heure), "Destinataire": alertes["destinataire"].map(nom),
                "Montant": alertes["montant"].map(argent), "Score": alertes["score"].round(2),
                "Décision": alertes["decision"].map(DECISIONS),
                "Raison": alertes["raisons"].map(lambda r: " ; ".join(r)),
                "Vérité (simulée)": alertes["scen"].map(lambda s: SCENARIOS.get(s, s)),
            }), hide_index=True)

# ----------------------------------------------------------------------------- 3. le bac à sable
with onglet_bac:
    st.write("Un monde vide pour tester le modèle à la main. Tous les comptes y sont neufs : inventez des "
             "identifiants, enregistrez des transferts et des retraits, et regardez comment le score évolue.")
    if "bac" not in etat:
        etat.update(bac=Magasin(), bac_t=config.JOUR_TEST * JOUR, bac_journal=[])
    bac = etat["bac"]

    def vider():
        for cle in ("bac", "bac_t", "bac_journal"):
            etat.pop(cle, None)

    def agir(type_, src, dst, somme, minutes):
        etat["bac_t"] += int(minutes * 60)
        etat["bac"].ajouter(etat["bac_t"], type_, somme, src, dst)
        quoi = "transfert vers " + dst if type_ == "TRANSFER" else "retrait en espèces"
        etat["bac_journal"].append(f"{heure(etat['bac_t'])} · {src} : {quoi}, {argent(somme)}")

    f1, f2, f3, f4 = st.columns(4)
    src = f1.text_input("Expéditeur", "VICTIME-1").strip() or "VICTIME-1"
    dst = f2.text_input("Destinataire", "COMPTE-X").strip() or "COMPTE-X"
    somme = f3.number_input("Montant", min_value=100.0, value=180000.0, step=1000.0, format="%.0f")
    minutes = f4.number_input("Minutes écoulées avant l'action", min_value=1, value=5, step=1)
    essai = moteur.noter(bac, src, dst, somme, etat["bac_t"] + int(minutes * 60))
    afficher_verdict(essai)
    g1, g2, g3 = st.columns(3)
    g1.button("Enregistrer ce transfert", type="primary", on_click=agir, args=("TRANSFER", src, dst, somme, minutes))
    g2.button("Le destinataire retire cette somme", on_click=agir, args=("CASH_OUT", dst, "AGENT-1", somme, minutes))
    g3.button("Vider le bac à sable", on_click=vider)
    st.caption("Essai possible : trois expéditeurs différents envoient au même compte neuf, qui retire à "
               "chaque fois en quelques minutes. Puis notez un quatrième transfert vers ce compte.")
    with st.expander("Les signaux donnés au modèle"):
        st.dataframe(tableau_signaux(essai), hide_index=True)
    if etat["bac_journal"]:
        st.write("**Opérations enregistrées**")
        for ligne in etat["bac_journal"][-12:]:
            st.write("· " + ligne)

# ----------------------------------------------------------------------------- 4. les mesures
with onglet_mesures:
    m = moteur.meta.get("mesures")
    if not m:
        st.info("Mesures absentes : lancer `python -m sentinelle.integrer`.")
    else:
        d = m["decoupage"]
        st.write(f"Mesures sur les jours 24 à 30, jamais vus par le modèle : {d['test']['transferts']:,} transferts, "
                 f"dont {d['test']['fraudes']:,} frauduleux. Seuils réglés sur les jours 20 à 23.".replace(",", " "))
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Fraudes signalées", pourcent(m["fraudes_signalees"]))
        k2.metric("Fausses alertes", pourcent(m["fausses_alertes"], 2))
        k3.metric("Alertes justes", pourcent(m["alertes_justes"]), help="Part des alertes qui sont de vraies fraudes")
        k4.metric("Précision moyenne", f"{m['precision_moyenne']:.3f}".replace(".", ","),
                  help=f"Un tirage au hasard donnerait {m['hasard']:.3f}")
        cache, vierge = m["scenario_cache"], m["premier_transfert_mule_vierge"]
        st.write(f"**Scénario jamais vu à l'entraînement** ({SCENARIOS.get(cache['nom'], cache['nom'])}) : "
                 f"{pourcent(cache['part_alertee'])} de ses transferts sont signalés.")
        st.write(f"**Limite** : premier transfert d'une victime vers une mule qui n'a encore rien reçu : "
                 f"{vierge['alertes']} signalés sur {vierge['total']}. Sans passé à lire, Sentinelle ne voit rien.")
        st.dataframe(pd.DataFrame([{
            "Cas": SCENARIOS.get(s["scen"], s["scen"]), "Transferts": s["transferts"], "Dont fraudes": s["fraudes"],
            "Signalés": pourcent(s["part_alertee"]), "Bloqués": pourcent(s["part_bloquee"]),
        } for s in m["par_scenario"]]), hide_index=True)
        st.subheader("À dire avec ces chiffres")
        st.write("- Les données sont simulées et les scénarios d'arnaque sont les nôtres : délais, montants et "
                 "nombre de mules sont des hypothèses.\n"
                 "- Le scénario caché est la preuve que le modèle ne récite pas seulement ce qu'il a appris.\n"
                 "- Le modèle s'entraîne sur GPU ; le service de score, lui, tourne sans GPU.")
    temps = moteur.meta.get("temps_s") or {}
    if temps:
        st.subheader("Temps mesurés (secondes)")
        st.dataframe(pd.DataFrame({"étape": list(temps), "secondes": list(temps.values())}), hide_index=True)

    def controler():
        from sentinelle.verifier import verifier
        etat["controle"] = verifier(journal=lambda *_: None)

    st.subheader("Le modèle intégré est-il celui qui a été évalué ?")
    st.button("Rejouer le flux et comparer les scores", on_click=controler)
    if "controle" in etat:
        c = etat["controle"]
        st.write(f"{c['transferts']} transferts rejoués par le service. Écart maximal de score avec "
                 f"l'évaluation : {c['ecart_max']:.4f}. Décisions différentes : {c['decisions_differentes']}.")
