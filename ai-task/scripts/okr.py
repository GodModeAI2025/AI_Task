"""OKR records, evidence validation and transparent progress calculations."""
import datetime as dt
import html
import math

KINDS = ('objective', 'key-result', 'measurement', 'review')
FIELDS = {
 'objective': {'owner', 'startDate', 'endDate', 'goalType', 'status'},
 'key-result': {'objectiveId', 'direction', 'baseline', 'target', 'unit', 'method', 'critical', 'taskIds', 'projectIds', 'freshnessDays'},
 'measurement': {'keyResultId', 'date', 'value', 'sourceId', 'locator', 'confidence', 'supersedes'},
 'review': {'objectiveId', 'date', 'reviewType', 'obstacles', 'learnings', 'nextTaskIds', 'outcome'},
}


def require(ok, message):
 if not ok:
  raise ValueError(message)


def number(value):
 require(type(value) in (int, float) and math.isfinite(value) and abs(value) <= 1e15, 'Invalid finite OKR number')


def validate(records, date, text):
 def relation(kind, ident):
  require(isinstance(ident, str) and ident in records[kind] and not records[kind][ident].get('trashedAt'), 'Invalid OKR reference: ' + str(ident))
 def links(kind, values):
  require(isinstance(values, list) and all(isinstance(x, str) for x in values) and len(set(values)) == len(values), 'Invalid OKR links')
  for ident in values:
   relation(kind, ident)
 for r in records['objective'].values():
  text(r.get('owner'), 'objective owner');date(r.get('startDate'));date(r.get('endDate'))
  require(r['startDate'] <= r['endDate'], 'Objective dates reversed')
  require(r.get('goalType') in ('committed', 'aspirational'), 'Invalid goal type')
  require(r.get('status') in ('draft', 'active', 'closed'), 'Invalid objective status')
 for r in records['key-result'].values():
  relation('objective', r.get('objectiveId'))
  require(r.get('direction') in ('increase', 'decrease', 'binary'), 'Invalid KR direction')
  number(r.get('baseline'));number(r.get('target'))
  if r['direction'] == 'binary':
   require(r['baseline'] == 0 and r['target'] == 1, 'Binary KR requires baseline 0 and target 1')
  else:
   require((r['target'] > r['baseline']) if r['direction'] == 'increase' else (r['target'] < r['baseline']), 'KR target must match direction and differ from baseline')
  text(r.get('unit'), 'unit');text(r.get('method'), 'measurement method')
  require(type(r.get('critical')) is bool, 'Critical must be boolean')
  require(type(r.get('freshnessDays')) is int and 1 <= r['freshnessDays'] <= 366, 'Invalid freshness threshold')
  links('task', r.get('taskIds'));links('project', r.get('projectIds'))
 consumed = set()
 active_slots = set()
 for r in records['measurement'].values():
  require(not r.get('trashedAt'), 'Measurements cannot be trashed; create a correction')
  relation('key-result', r.get('keyResultId'));relation('source', r.get('sourceId'))
  date(r.get('date'));number(r.get('value'));text(r.get('locator'), 'measurement locator')
  objective = records['objective'][records['key-result'][r['keyResultId']]['objectiveId']]
  require(objective['startDate'] <= r['date'] <= objective['endDate'], 'Measurement outside objective cycle')
  if records['key-result'][r['keyResultId']]['direction'] == 'binary':
   require(r['value'] in (0, 1), 'Binary measurement must be 0 or 1')
  if r.get('confidence') is not None:
   number(r['confidence']);require(0 <= r['confidence'] <= 1, 'Confidence must be 0–1')
  old = r.get('supersedes')
  if old:
   relation('measurement', old)
   previous = records['measurement'][old]
   require(old != r['id'] and previous['keyResultId'] == r['keyResultId'] and previous['date'] == r['date'], 'Correction must replace same KR/date')
   require(old not in consumed, 'Measurement has multiple corrections')
   consumed.add(old)
 for r in records['measurement'].values():
  visited = set();node = r
  while node.get('supersedes'):
   require(node['id'] not in visited, 'Measurement correction cycle')
   visited.add(node['id']);node = records['measurement'][node['supersedes']]
  if r['id'] not in consumed:
   slot = (r['keyResultId'], r['date'])
   require(slot not in active_slots, 'Multiple measurements for same KR/date require supersedes')
   active_slots.add(slot)
 for r in records['review'].values():
  relation('objective', r.get('objectiveId'));date(r.get('date'))
  require(r.get('reviewType') in ('check-in', 'closeout'), 'Invalid review type')
  require(r.get('outcome') in ('pending', 'achieved', 'partially-achieved', 'not-achieved'), 'Invalid review outcome')
  require(r['reviewType'] == 'closeout' or r['outcome'] == 'pending', 'Only closeout reviews may judge outcome')
  text(r.get('obstacles', ''), 'obstacles', empty=True);text(r.get('learnings', ''), 'learnings', empty=True)
  links('task', r.get('nextTaskIds'))


def defaults(kind):
 if kind == 'objective':return {'status': 'draft', 'goalType': 'committed'}
 if kind == 'key-result':return {'critical': False, 'taskIds': [], 'projectIds': [], 'freshnessDays': 14}
 if kind == 'measurement':return {'confidence': None, 'supersedes': None}
 if kind == 'review':return {'reviewType': 'check-in', 'outcome': 'pending', 'obstacles': '', 'learnings': '', 'nextTaskIds': []}
 return {}


def report(state, today):
 dt.date.fromisoformat(today)
 records = state['records']
 eligible = [m for m in records.get('measurement', {}).values() if m['date'] <= today and m['createdAt'] <= today]
 replaced = {m['supersedes'] for m in eligible if m.get('supersedes')}
 eligible = [m for m in eligible if m['id'] not in replaced]
 result = []
 for obj in records.get('objective', {}).values():
  if obj.get('trashedAt'):continue
  results = []
  for kr in records.get('key-result', {}).values():
   if kr['objectiveId'] != obj['id'] or kr.get('trashedAt'):continue
   measurements = sorted([m for m in eligible if m['keyResultId'] == kr['id']], key=lambda m: m['date'])
   m = measurements[-1] if measurements else None
   raw = (m['value'] - kr['baseline']) / (kr['target'] - kr['baseline']) if m else None
   score = max(0, min(1, raw)) if raw is not None else None
   age = (dt.date.fromisoformat(today) - dt.date.fromisoformat(m['date'])).days if m else None
   results.append({'id': kr['id'], 'title': kr['title'], 'direction': kr['direction'], 'baseline': kr['baseline'],
                   'target': kr['target'], 'unit': kr['unit'], 'method': kr['method'], 'critical': kr['critical'],
                   'value': m['value'] if m else None, 'rawProgress': raw, 'progress': score,
                   'measurement': m, 'confidence': m['confidence'] if m else None, 'ageDays': age,
                   'stale': age > kr['freshnessDays'] if m else None, 'taskIds': kr['taskIds'], 'projectIds': kr['projectIds']})
  known = [r['progress'] for r in results if r['progress'] is not None]
  partial = sum(known) / len(known) if known else None
  complete = bool(results) and len(known) == len(results)
  reviews = sorted([r for r in records.get('review', {}).values() if r['objectiveId'] == obj['id'] and r['date'] <= today and r['createdAt'] <= today and not r.get('trashedAt')], key=lambda r: (r['date'], r['id']))
  result.append({'objective': obj, 'keyResults': results, 'progress': partial if complete else None,
                 'partialMean': partial, 'measuredCount': len(known), 'totalCount': len(results),
                 'criticalUnmet': [r['id'] for r in results if r['critical'] and (r['progress'] is None or r['progress'] < 1)],
                 'reviews': reviews, 'asOf': today})
 return result


def render(state, today):
 esc = lambda x: html.escape(str(x), quote=True)
 pct = lambda x: 'unbekannt' if x is None else f'{x * 100:.1f} %'
 out = '<section id="okr"><h2>Ziele &amp; Wirkung · OKR</h2><p>Gemessene Wirkung, unabhängig von erledigten Aufgaben. Zuversicht und Aktualität stehen separat.</p>'
 for item in report(state, today):
  obj = item['objective']
  out += '<article class="card" id="' + esc(obj['id']) + '"><h3>' + esc(obj['title']) + '</h3><p>' + esc(obj['owner']) + ' · ' + esc(obj['startDate']) + ' bis ' + esc(obj['endDate']) + ' · ' + ('Verbindlich' if obj['goalType'] == 'committed' else 'Ambitioniert') + '</p><p><strong>Fortschritt: ' + pct(item['progress']) + '</strong> · Messabdeckung ' + str(item['measuredCount']) + '/' + str(item['totalCount']) + '</p>'
  if item['progress'] is None and item['partialMean'] is not None:
   out += '<p>Teilmittel nur der gemessenen Ergebnisse: ' + pct(item['partialMean']) + ' (unvollständig)</p>'
  if item['criticalUnmet']:out += '<p>Kritische Ergebnisse offen: ' + esc(', '.join(item['criticalUnmet'])) + '</p>'
  for kr in item['keyResults']:
   out += '<div class="card" id="' + esc(kr['id']) + '"><h4>' + esc(kr['title']) + (' · kritisch' if kr['critical'] else '') + '</h4><p>Ausgang ' + esc(kr['baseline']) + ' → Ziel ' + esc(kr['target']) + ' ' + esc(kr['unit']) + ' · Ist ' + esc(kr['value'] if kr['value'] is not None else 'unbekannt') + '</p><p>Fortschritt ' + pct(kr['progress']) + ' · Rohfortschritt ' + pct(kr['rawProgress']) + ' · Zuversicht ' + pct(kr['confidence']) + '</p><p>Messmethode: ' + esc(kr['method']) + '</p>'
   if kr['measurement']:
    m = kr['measurement'];source = state['records']['source'][m['sourceId']]
    out += '<p>Messung ' + esc(m['date']) + ' · ' + str(kr['ageDays']) + ' Tage alt' + (' · veraltet' if kr['stale'] else '') + '<br>Beleg: ' + esc(source['title']) + ' · ' + esc(source['reference']) + ' · ' + esc(m['locator']) + '</p>'
   links = []
   for kind, ids in [('task', kr['taskIds']), ('project', kr['projectIds'])]:
    for ident in ids:
     links.append('<a href="#record-' + esc(ident) + '">' + esc(state['records'][kind][ident]['title']) + '</a>')
   out += '<p>Unterstützt durch: ' + (', '.join(links) or 'noch keine Verknüpfung') + '</p>'
   history = sorted([m for m in state['records']['measurement'].values() if m['keyResultId'] == kr['id'] and m['date'] <= today and m['createdAt'] <= today], key=lambda m: (m['date'], m['createdAt'], m['id']))
   if history:
    out += '<details><summary>Messverlauf und Belege</summary>'
    for point in history:
     source = state['records']['source'][point['sourceId']]
     replaced = any(m.get('supersedes') == point['id'] for m in history)
     out += '<p>' + esc(point['date']) + ': ' + esc(point['value']) + ' ' + esc(kr['unit']) + (' · ersetzt' if replaced else '') + ' · ' + esc(source['title']) + ' · ' + esc(point['locator']) + '</p>'
    out += '</details>'
   out += '</div>'
  for review in item['reviews']:
   out += '<details><summary>Review ' + esc(review['date']) + ' · ' + esc(review['reviewType']) + '</summary><p>Hindernisse: ' + esc(review['obstacles']) + '</p><p>Erkenntnisse: ' + esc(review['learnings']) + '</p><p>Nächste Aufgaben: ' + esc(', '.join(review['nextTaskIds'])) + '</p><p>Bewertung: ' + esc(review['outcome']) + '</p></details>'
  out += '</article>'
 linked = set()
 for item in report(state, today):
  for kr in item['keyResults']:
   linked.update(kr['taskIds'] + kr['projectIds'])
  for review in item['reviews']:
   linked.update(review['nextTaskIds'])
 if linked:
  out += '<h3>Unterstützende Aufgaben und Projekte</h3>'
  for ident in sorted(linked):
   record = state['records']['task'].get(ident) or state['records']['project'][ident]
   out += '<details id="record-' + esc(ident) + '"><summary>' + esc(record['title']) + '</summary><p>Status: ' + esc(record.get('status')) + '</p><p>' + esc(record.get('notes', '')) + '</p><small>' + esc(ident) + '</small></details>'
 return out + '<p>Der Durchschnitt bewertet das Ziel nicht automatisch als erreicht. Die Abschlussbewertung wird im Review festgehalten.</p></section>'
