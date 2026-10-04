"""Non-destructive backend checks for Kallami 1.5; uses a temporary SQLite database."""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys

# Ejecuta este archivo con el directorio servidor del proyecto como cwd.
sys.path.insert(0, str(Path.cwd()))
from fastapi.testclient import TestClient
from app import main

results = []
def record(case, expected, observed, interpretation):
    passed = expected == observed
    results.append((case, passed, expected, observed, interpretation))

def data_for(response):
    body=response.json()
    return body['profile']['profile_id'], {'Authorization': 'Bearer '+body['access_token']}

def progress(response):
    data=response.json()
    return {k:data[k] for k in ('player_id','level','clues','clue_ids','checkpoint_id','completed','health','position_x','position_y','mission_state','puzzle_step')}

with TemporaryDirectory(prefix='kallami_security_review_') as temp:
    main.DATABASE_PATH=Path(temp)/'isolated.sqlite3'
    main.initialize_database()
    client=TestClient(main.app)
    record('Servicio responde',200,client.get('/api/estado').status_code,'control')
    a=client.post('/api/perfiles',json={'display_name':'Perfil Auditor A','pin':'2468'})
    aid, ah=data_for(a)
    initial=client.get(f'/api/progreso/{aid}',headers=ah)
    p=progress(initial)
    record('Perfil crea progreso inicial predeterminado',True,(a.status_code==201 and p['level']==1 and p['health']==5 and p['checkpoint_id']=='inicio' and p['clues']==0),'control')
    cprofile=client.post('/api/perfiles',json={'display_name':'Prueba Progreso Inicial','pin':'8642'})
    cid,ch=data_for(cprofile)
    forged=progress(client.get(f'/api/progreso/{cid}',headers=ch))
    forged.update(level=3,clues=3,clue_ids=['pista_comunidad','pista_mineros','pista_cerro'],checkpoint_id='camara_final',completed=True,mission_state=3,puzzle_step=3)
    record('Regresión Alpha: perfil nuevo no puede declararse completado',409,client.post('/api/progreso',json=forged,headers=ch).status_code,'control corregido: creación fija estado inicial y transición bloquea salto')
    b=client.post('/api/perfiles',json={'display_name':'Perfil Auditor B','pin':'1357'})
    bid,bh=data_for(b)
    record('PIN incorrecto no inicia sesión',401,client.post('/api/perfiles/login',json={'profile_id':aid,'pin':'0000'}).status_code,'control')
    record('PIN con formato inválido es rechazado',422,client.post('/api/perfiles',json={'display_name':'PIN inválido','pin':'12ab'}).status_code,'control')
    record('Nombre de perfil con cadena SQL es rechazado',422,client.post('/api/perfiles',json={'display_name':"' OR 1=1--",'pin':'1234'}).status_code,'control')
    record('Nombre duplicado no crea otro perfil',409,client.post('/api/perfiles',json={'display_name':'Perfil Auditor A','pin':'2468'}).status_code,'control')
    record('GET de progreso sin token es rechazado',401,client.get(f'/api/progreso/{aid}').status_code,'control')
    record('POST de progreso sin token es rechazado',401,client.post('/api/progreso',json=p).status_code,'control')
    record('Token A no lee progreso B',403,client.get(f'/api/progreso/{bid}',headers=ah).status_code,'control')
    pb=progress(client.get(f'/api/progreso/{bid}',headers=bh))
    record('Token A no modifica progreso B',403,client.post('/api/progreso',json=pb,headers=ah).status_code,'control')
    # First accept a legitimate damage-like lower health and changed location.
    p.update(health=1,position_x=2372.0,position_y=28.0)
    r=client.post('/api/progreso',json=p,headers=ah)
    record('Estado con salud reducida se guarda',200,r.status_code,'precondition')
    p=progress(r)
    # Then attempt health restoration and teleport in a single client-submitted update.
    p.update(health=5,position_x=28.0,position_y=1472.0)
    r=client.post('/api/progreso',json=p,headers=ah)
    record('Aumento de salud y salto a coordenadas opuestas debería bloquearse',409,r.status_code,'finding: accepted; returned health=%s position=(%s,%s)'%(r.json().get('health'),r.json().get('position_x'),r.json().get('position_y')))
    p=progress(r)
    p.update(level=2,checkpoint_id='ascenso_inicio',mission_state=1)
    r=client.post('/api/progreso',json=p,headers=ah)
    record('Paso de nivel 1 a 2 antes de recoger memorias del ascenso',200,r.status_code,'transición permitida según el recorrido documentado')
    p=progress(r)
    p.update(level=3,checkpoint_id='camara_inicio')
    r=client.post('/api/progreso',json=p,headers=ah)
    record('Segundo cambio de nivel sin memorias debe bloquearse',409,r.status_code,'finding: reached level=%s with clues=%s'%(r.json().get('level'),r.json().get('clues')))
    listing=client.get('/api/perfiles')
    ids=[row['profile_id'] for row in listing.json()]
    results.append(('Directorio de perfiles expone identificadores sin token', None, 200, listing.status_code, 'OBSERVACION informativa: lista nombres e IDs para el selector; servicio limitado a loopback'))
    record('Eliminación con PIN incorrecto es rechazada',401,client.post(f'/api/perfiles/{aid}/eliminar',json={'pin':'9999'}).status_code,'control')
    deleted=client.post(f'/api/perfiles/{bid}/eliminar',json={'pin':'1357'})
    remaining=client.get('/api/perfiles').json()
    record('Eliminación con PIN correcto borra el perfil y no el otro',True,(deleted.status_code==200 and all(row['profile_id']!=bid for row in remaining) and any(row['profile_id']==aid for row in remaining)),'control')

for case, passed, expected, observed, interpretation in results:
    status='OBSERVATION' if passed is None else ('PASS' if passed else 'FINDING')
    print(f'{status} | {case} | expected={expected} | observed={observed} | {interpretation}')
print(f'RESUMEN | controles PASS={sum(1 for x in results if x[1] is True)} | findings={sum(1 for x in results if x[1] is False)} | observations={sum(1 for x in results if x[1] is None)} | cases={len(results)}')
