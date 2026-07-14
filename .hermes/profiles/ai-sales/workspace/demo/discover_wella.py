from pathlib import Path
from urllib import request, parse
from html import unescape
import json, re, time, csv, hashlib
from datetime import datetime, timezone

RUN = Path('/root/.hermes/profiles/ai-sales/workspace/prospect-runs/2026-07-12-wella-professionals-fr')
RUN.mkdir(parents=True, exist_ok=True)
USER_AGENT = 'Hermes ai-sales research for prospect sourcing (contact: local demo)'

cities = [
    ('Paris', 48.8566, 2.3522), ('Lyon', 45.7640, 4.8357),
    ('Bordeaux', 44.8378, -0.5792), ('Lille', 50.6292, 3.0573),
    ('Nantes', 47.2184, -1.5536), ('Toulouse', 43.6047, 1.4442),
    ('Nice', 43.7102, 7.2620), ('Montpellier', 43.6119, 3.8772),
    ('Strasbourg', 48.5734, 7.7521), ('Marseille', 43.2965, 5.3698),
]
kw_groups = {
    'coloration': ['coloration', 'couleur', 'coloriste', 'coloristes', 'colorimétrie', 'colorimetrie', 'gloss', 'patine'],
    'balayage_blond': ['balayage', 'blond', 'blonde', 'ombré', 'ombre', 'mèches', 'meches', 'babylight', 'babylights'],
    'soin': ['soin', 'soins', 'réparation', 'reparation', 'kératine', 'keratine', 'lissage', 'botox capillaire', 'traitement'],
    'premium': ['expert', 'expertise', 'studio', 'atelier', 'maison', 'premium', 'luxe', 'sur mesure', 'sur-mesure', 'diagnostic'],
    'formation': ['formation', 'academy', 'académie', 'academie', 'masterclass', 'formateur', 'formatrice'],
}
negative = ['tchip', 'low cost', 'low-cost', 'pas cher', 'discount']


def fetch_url(url, timeout=15, max_bytes=180000):
    if not url:
        return None, '', '', ''
    if url.startswith('//'):
        url = 'https:' + url
    if not re.match(r'https?://', url):
        url = 'https://' + url
    req = request.Request(url, headers={'User-Agent': USER_AGENT, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
    try:
        with request.urlopen(req, timeout=timeout) as r:
            final = r.geturl(); raw = r.read(max_bytes); ctype = r.headers.get('content-type', '')
        if b'\x00' in raw[:1000]:
            return final, '', ctype, 'binary'
        enc = 'utf-8'; m = re.search('charset=([^;]+)', ctype, re.I)
        if m:
            enc = m.group(1).strip()
        return final, raw.decode(enc, 'replace'), ctype, ''
    except Exception as e:
        return url, '', '', type(e).__name__ + ': ' + str(e)[:120]


def text_from_html(html):
    if not html:
        return '', '', ''
    title = ''; m = re.search(r'<title[^>]*>(.*?)</title>', html, re.I | re.S)
    if m:
        title = unescape(re.sub('<.*?>', ' ', m.group(1))).strip()
    desc = ''; m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', html, re.I | re.S)
    if m:
        desc = unescape(m.group(1)).strip()
    h = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', html, flags=re.I | re.S)
    text = unescape(re.sub(r'<[^>]+>', ' ', h)); text = re.sub(r'\s+', ' ', text).strip()
    return title, desc, text[:15000]


def domain_of(url):
    try:
        u = url if re.match(r'https?://', url) else 'https://' + url
        net = parse.urlparse(u).netloc.lower()
        return net[4:] if net.startswith('www.') else net
    except Exception:
        return ''


def overpass_city(city):
    name, lat, lon = city
    q = f'''[out:json][timeout:30];
(
  node(around:11000,{lat},{lon})["shop"="hairdresser"]["website"];
  way(around:11000,{lat},{lon})["shop"="hairdresser"]["website"];
  relation(around:11000,{lat},{lon})["shop"="hairdresser"]["website"];
  node(around:11000,{lat},{lon})["shop"="hairdresser"]["contact:website"];
  way(around:11000,{lat},{lon})["shop"="hairdresser"]["contact:website"];
  relation(around:11000,{lat},{lon})["shop"="hairdresser"]["contact:website"];
);
out tags center 60;'''
    data = parse.urlencode({'data': q}).encode()
    last = ''
    for u in ['https://overpass-api.de/api/interpreter', 'https://overpass.kumi.systems/api/interpreter']:
        try:
            req = request.Request(u, data=data, headers={'User-Agent': USER_AGENT})
            with request.urlopen(req, timeout=45) as r:
                js = json.loads(r.read())
            return js.get('elements', []), ''
        except Exception as e:
            last = type(e).__name__ + ': ' + str(e)[:120]; time.sleep(1)
    return [], last


def osm_url(el):
    return f"https://www.openstreetmap.org/{el.get('type')}/{el.get('id')}"


def compute_score(name, text, tags):
    low = (name + ' ' + text).lower()
    hits = {g: [k for k in kws if k in low] for g, kws in kw_groups.items()}
    hit_count = sum(len(v) for v in hits.values()); groups = sum(1 for v in hits.values() if v)
    neg = [k for k in negative if k in low]
    fit = 2.5
    if hits['coloration'] or hits['balayage_blond']: fit += 1.1
    if hits['premium']: fit += 0.6
    if hits['soin']: fit += 0.3
    if hits['formation']: fit += 0.4
    if tags.get('brand'): fit += 0.1
    if neg: fit -= 1.0
    fit = max(0, min(5, round(fit, 1)))
    intent = 1.5 + min(2.0, groups * 0.45) + min(1.0, hit_count * 0.08)
    if hits['balayage_blond']: intent += 0.4
    if hits['formation']: intent += 0.3
    if neg: intent -= 0.7
    intent = max(0, min(5, round(intent, 1)))
    timing = 2.5
    if 'instagram' in low or 'actualité' in low or 'actualites' in low or 'blog' in low: timing += 0.4
    if tags.get('opening_hours'): timing += 0.1
    timing = max(0, min(5, round(timing, 1)))
    total = round(fit * 0.45 + intent * 0.35 + timing * 0.20, 2)
    next_action = 'lead_enrichment' if total >= 4.0 else ('research_more' if total >= 2.0 else 'discard')
    if neg and total < 3.2: next_action = 'discard'
    return hits, {'fit': fit, 'intent': intent, 'timing': timing, 'total': total, 'reason': ''}, next_action, neg


def main():
    seen_domains = set(); seen_names = set(); candidates = []; errors = []
    for city in cities:
        elements, err = overpass_city(city)
        if err: errors.append(f"{city[0]} Overpass: {err}")
        for el in elements:
            tags = el.get('tags', {}); name = tags.get('name') or tags.get('brand') or ''; website = tags.get('website') or tags.get('contact:website') or ''
            if not name or not website: continue
            d = domain_of(website); key = (name.lower().strip(), d)
            if not d or d in seen_domains or key in seen_names: continue
            seen_domains.add(d); seen_names.add(key)
            final, html, ctype, ferr = fetch_url(website)
            title, desc, text = text_from_html(html)
            hits, score, next_action, neg = compute_score(name, title + ' ' + desc + ' ' + text, tags)
            if not any(hits.values()) and score['total'] < 3.0: continue
            segment = 'Segment E — Salon généraliste premium avec opportunité soin/styling'
            joined = (name + ' ' + title + ' ' + text[:1000]).lower()
            if hits['coloration'] or hits['balayage_blond']: segment = 'Segment A — Salon premium orienté coloration'
            if 'studio' in joined or 'coloriste' in joined: segment = 'Segment B — Studio coloriste / expert blond et balayage'
            if tags.get('brand') or 'groupe' in joined: segment = 'Segment C — Groupe ou réseau de salons'
            signal_parts = []
            if hits['coloration']: signal_parts.append('services/mentions coloration: ' + ', '.join(hits['coloration'][:4]))
            if hits['balayage_blond']: signal_parts.append('services/mentions balayage/blond: ' + ', '.join(hits['balayage_blond'][:4]))
            if hits['soin']: signal_parts.append('services/mentions soin/lissage: ' + ', '.join(hits['soin'][:4]))
            if hits['premium']: signal_parts.append('positionnement expert/premium: ' + ', '.join(hits['premium'][:4]))
            if hits['formation']: signal_parts.append('signal formation/academy: ' + ', '.join(hits['formation'][:4]))
            signal = '; '.join(signal_parts) if signal_parts else 'Salon coiffure avec site web public, à rechercher davantage.'
            score['reason'] = f"Fit {score['fit']}/5 car {segment.lower()} avec signal public; intent {score['intent']}/5 basé sur {signal[:180]}; timing {score['timing']}/5 car source publique accessible mais récence à confirmer."
            pain = 'Besoin probable de résultats couleur/soin constants, de différenciation salon et de supports techniques/formation Wella.'
            if hits['formation']: pain = 'Besoin probable de contenus, formation et support technique autour des prestations couleur/soin.'
            if segment.startswith('Segment C'): pain = 'Besoin probable de standardiser les produits, la formation et la qualité entre plusieurs salons ou une marque de réseau.'
            addr = ', '.join([v for k, v in tags.items() if k in ('addr:housenumber', 'addr:street', 'addr:postcode', 'addr:city')]) or city[0]
            cid = 'cand_' + hashlib.sha1((name + d).encode()).hexdigest()[:10]
            candidates.append({
                'candidate_id': cid,
                'company': {'name': name, 'domain': d, 'website': final or website, 'city': tags.get('addr:city') or city[0], 'address': addr, 'segment': segment, 'source_urls': [osm_url(el), final or website]},
                'person': {'first_name': '', 'last_name': '', 'title': 'Propriétaire / directeur artistique / responsable salon (à identifier)', 'linkedin_url': '', 'source_urls': []},
                'signal': {'type': 'website_service_signal', 'summary': signal, 'source_url': final or website, 'observed_date': '2026-07-12'},
                'pain_hypothesis': pain,
                'score': score,
                'email': {'address': '', 'status': 'not_found', 'hunter_score': None, 'hunter_sources': [], 'note': 'Pas de personne nommée fiable à ce stade ; ne pas deviner.'},
                'proof': {'tools_used': ['OpenStreetMap Overpass', 'website_fetch'], 'checked_at': datetime.now(timezone.utc).isoformat(), 'notes': ([f'Website fetch issue: {ferr}'] if ferr else []) + ([f'Negative signal: {neg}'] if neg else [])},
                'next_action': next_action,
                'raw': {'osm_tags': tags, 'page_title': title, 'meta_description': desc, 'keyword_hits': hits}
            })
            if len(candidates) >= 60: break
        if len(candidates) >= 60: break
        time.sleep(1)

    candidates_sorted = sorted(candidates, key=lambda x: x['score']['total'], reverse=True)
    discovery = [c for c in candidates_sorted if c['next_action'] != 'discard'][:20]
    if len(discovery) < 20:
        existing = {c['candidate_id'] for c in discovery}
        for c in candidates_sorted:
            if c['candidate_id'] not in existing:
                discovery.append(c); existing.add(c['candidate_id'])
            if len(discovery) >= 20: break

    (RUN / 'candidates.json').write_text(json.dumps(candidates_sorted[:40], indent=2, ensure_ascii=False), encoding='utf-8')
    (RUN / 'discovery.json').write_text(json.dumps(discovery, indent=2, ensure_ascii=False), encoding='utf-8')
    fields = ['candidate_id', 'company_name', 'city', 'domain', 'website', 'segment', 'signal_summary', 'signal_source', 'pain_hypothesis', 'fit', 'intent', 'timing', 'total', 'email_status', 'next_action']
    with (RUN / 'discovery.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for c in discovery:
            w.writerow({'candidate_id': c['candidate_id'], 'company_name': c['company']['name'], 'city': c['company']['city'], 'domain': c['company']['domain'], 'website': c['company']['website'], 'segment': c['company']['segment'], 'signal_summary': c['signal']['summary'], 'signal_source': c['signal']['source_url'], 'pain_hypothesis': c['pain_hypothesis'], 'fit': c['score']['fit'], 'intent': c['score']['intent'], 'timing': c['score']['timing'], 'total': c['score']['total'], 'email_status': c['email']['status'], 'next_action': c['next_action']})

    src_lines = ['# Sources — Wella Professionals France prospect run', '', '## Méthode', '', '- Découverte via OpenStreetMap Overpass : `shop=hairdresser` avec site web public dans les villes ICP.', '- Vérification des sites publics quand accessibles.', '- Extraction de signaux via mots-clés publics : coloration, balayage, blond, soin, lissage, studio, expert, formation.', '- Aucun décideur ni email inventé.', '', '## Sources par lead sélectionné']
    for i, c in enumerate(discovery, 1):
        src_lines += ['', f"### {i}. {c['company']['name']} — {c['company']['city']}", '', f"- OSM: {c['company']['source_urls'][0]}", f"- Site/source signal: {c['signal']['source_url']}", f"- Signal: {c['signal']['summary']}", f"- Score: {c['score']['total']} — {c['score']['reason']}"]
    if errors: src_lines += ['', '## Erreurs / limites de collecte', ''] + [f'- {e}' for e in errors]
    (RUN / 'sources.md').write_text('\n'.join(src_lines) + '\n', encoding='utf-8')

    notes = f"""# Notes — Wella Professionals France prospect run

Checked at: {datetime.now(timezone.utc).isoformat()}

## Collecte

- Candidats retenus dans `candidates.json`: {min(40, len(candidates_sorted))}
- Leads sélectionnés dans `discovery.json`: {len(discovery)}
- Source primaire de découverte: OpenStreetMap Overpass + sites publics.

## Limites

- La majorité des sites ne donne pas de décideur nominatif fiable ; Hunter.io n'a donc pas été utilisé pour éviter de deviner des emails.
- Le champ `observed_date` indique la date de vérification du run, pas forcément la date de publication du signal.
- Les signaux sont des preuves de positionnement/service, pas toujours des trigger events datés.

## Prochaine action

- Inspecter manuellement les 20 leads prioritaires.
- Identifier des décideurs nommés pour les meilleurs leads.
- Utiliser Hunter.io seulement quand un nom + domaine fiable sont disponibles.
- Synchroniser ces leads dans le CRM local.
"""
    (RUN / 'notes.md').write_text(notes, encoding='utf-8')
    print(json.dumps({'candidates_found': len(candidates), 'candidates_saved': min(40, len(candidates_sorted)), 'discovery_count': len(discovery), 'top5': [{'name': c['company']['name'], 'city': c['company']['city'], 'score': c['score']['total']} for c in discovery[:5]], 'errors': errors[:5]}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
