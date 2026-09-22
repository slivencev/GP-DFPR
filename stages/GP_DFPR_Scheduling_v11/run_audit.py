from pathlib import Path
import sys,json,csv,hashlib,zipfile,shutil,itertools
import numpy as np
from scheduler import matching,known_lifetimes
sys.stdout.reconfigure(encoding='utf-8');root=Path(__file__).resolve().parent
def write_csv(path,rows):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def tests():
    for mask in range(512):
        edges=[[s for s in range(3) if mask&(1<<(a*3+s))] for a in range(3)]
        brute=any(all(perm[a] in edges[a] for a in range(3)) for perm in itertools.permutations(range(3)))
        result=matching(edges,list(range(3)));assert result['feasible']==brute
        if not brute:
            jobs=result['deficient_jobs'];neighbors=set(s for a in jobs for s in edges[a]);assert len(neighbors)==result['neighbor_slots']<len(jobs)
    rng=np.random.default_rng(2026092070)
    for _ in range(500):
        n=int(rng.integers(0,8));target=5;release=rng.integers(0,8,n).tolist();life=rng.integers(1,8,n).tolist();caps={t:int(rng.integers(0,3)) for t in range(6)}
        slots=[t for t,b in caps.items() for _ in range(b)];edges=[[j for j,s in enumerate(slots) if max(release[a],target-life[a]+1)<=s<=target] for a in range(n)]
        greedy=known_lifetimes(release,life,target,caps);exact=matching(edges,slots);assert greedy['feasible']==exact['feasible']
        if greedy['feasible']:
            for a,s in greedy['assignment'].items():assert s>=release[a] and s<=target and target-s<life[a]
    assert not known_lifetimes([0],[1],1,{0:1})['feasible']
    assert known_lifetimes([],[],1,{})['feasible']
    return dict(exhaustive_graphs=512,random_nested_window_cases=500,strict_expiry_and_empty_tests=2,status='PASS')
def package():
    (root/'requirements.txt').write_text('numpy==2.3.5\n')
    (root/'MANIFEST.json').write_text(json.dumps({str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest() for f in root.rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.name!='MANIFEST.json'},indent=2))
    dest=root.parent/'GP_DFPR_Scheduling_v11.zip'
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
        for f in root.rglob('*'):
            if f.is_file() and '__pycache__' not in f.parts:z.write(f,str(Path(root.name)/f.relative_to(root)))
    with zipfile.ZipFile(dest) as z:assert z.testzip() is None
def main():
    old=root.parent/'GP_DFPR_Certificate_Audit_v10.zip'
    with zipfile.ZipFile(old) as z:
        assert z.testzip() is None
        assert z.read('GP_DFPR_Certificate_Audit_v10/REPORT_RU.md')==(root.parent/'GP_DFPR_Certificate_Audit_v10/REPORT_RU.md').read_bytes()
    (root/'V10_CHECKPOINT.json').write_text(json.dumps(dict(archive=old.name,sha256=hashlib.sha256(old.read_bytes()).hexdigest(),report_verified=True),indent=2))
    checks=tests();(root/'TESTS.json').write_text(json.dumps(checks,indent=2));(root/'traces').mkdir(exist_ok=True)
    rows=[];examples={};targets=0
    for duration in [12,36]:
        for run in range(6000,6012):
            src=root.parent/'GP_DFPR_Periodic_v9/traces'/f'global-d{duration}_{run}.npz';shutil.copyfile(src,root/'traces'/src.name)
            with np.load(src) as d:truth=d['truth'];noise=d['noise']
            empty=~(truth[:300]>=0).all(axis=2).any(axis=1);starts=np.flatnonzero(empty&~np.r_[False,empty[:-1]])
            for budget in [1,4,8]:
                attainable=missed=0;waitsum=0;count=0
                for start in starts:
                    end=int(start)
                    while end<300 and empty[end]:end+=1
                    first=None
                    for target in range(int(start),end):
                        times=list(range(int(start),target+1));slots=[s for s in times for _ in range(budget)]
                        good=(truth[times]+noise[times]+.01+.04*(target-np.array(times))[:,None,None]<0).any(axis=2)
                        edges=[[j for j,s in enumerate(slots) if good[s-start,a]] for a in range(24)]
                        r=matching(edges,slots);count+=1;targets+=1
                        if r['feasible']:
                            attainable+=1
                            if first is None:first=target-start
                            for s in set(r['assignment'].values()):assert list(r['assignment'].values()).count(s)<=budget
                            for a,s in r['assignment'].items():assert good[s-start,a]
                        key=f'{duration}_{budget}_{r["feasible"]}'
                        if key not in examples:examples[key]=dict(duration=duration,budget=budget,run=run,episode_start=int(start),target=target,**r)
                    missed+=first is None;waitsum+=end-start if first is None else first
                rows.append(dict(duration=duration,run=run,budget=budget,empty_targets=count,attainable_targets=attainable,episodes=len(starts),episodes_without_attainable_target=missed,restricted_earliest_wait_sum=waitsum))
        print('duration',duration,'complete',flush=True)
    write_csv(root/'per_run.csv',rows);(root/'examples.json').write_text(json.dumps(examples,indent=2));summary=[]
    lines=['# Точное планирование общего сертификата: v11','','Получены необходимое и достаточное условие для известных сроков действия свидетельств и точный алгоритм для произвольных допустимых моментов измерения. Это ограниченная задача планирования, не новая онлайн-политика.','','На сохранённых данных v9 выполнен ретроспективный анализ: доступны все будущие исходы измерений, измерения начинаются с начала реально невыполнимого эпизода, пауз исполнения нет. Доэпизодная история исключена. Поэтому это не безусловная верхняя граница качества прежних контроллеров. Достижимость каждого момента проверяется отдельным расписанием; совместная достижимость всех моментов не утверждается.','','| Импульс | B | Доля отдельно достижимых моментов | Эпизодов без достижимого момента | Среднее ограниченное ожидание |','|---|---:|---:|---:|---:|']
    for duration in [12,36]:
        for budget in [1,4,8]:
            rr=[r for r in rows if r['duration']==duration and r['budget']==budget];sums={k:sum(r[k] for r in rr) for k in ['empty_targets','attainable_targets','episodes','episodes_without_attainable_target','restricted_earliest_wait_sum']};summary.append(dict(duration=duration,budget=budget,**sums));lines.append(f'| {duration} | {budget} | {sums["attainable_targets"]/sums["empty_targets"]:.4f} | {sums["episodes_without_attainable_target"]}/{sums["episodes"]} | {sums["restricted_earliest_wait_sum"]/sums["episodes"]:.2f} |')
    write_csv(root/'summary.csv',summary);checks.update(target_matching_problems=targets,all_witness_checks='PASS');(root/'checks.json').write_text(json.dumps(checks,indent=2));lines+=['',f'Проверки: {checks}.','','Расписания-свидетели и примеры дефицита слотов — examples.json. Невозможность паросочетания означает дефицит в заданной модели свидетельств, а не физическую невыполнимость сети. Все расчёты используют только синтетические данные. Теоретическая конструкция основана на стандартных идеях планирования и паросочетаний; новизна относительно литературы не заявляется.'];(root/'REPORT_RU.md').write_text('\n'.join(lines),encoding='utf-8');package();print('\n'.join(lines),flush=True)
if __name__=='__main__':main()
