from pathlib import Path
import json,csv,sys,hashlib,zipfile,shutil,copy
import numpy as np
import model as m
from scheduler import matching
sys.stdout.reconfigure(encoding='utf-8');root=Path(__file__).resolve().parent
Base=m.Controller
class Recorder(Base):
    instances=[]
    def __init__(self,*args):
        super().__init__(*args);self.records={};Recorder.instances.append(self)
    def decision(self,t,current,query):
        r=super().decision(t,current,query)
        self.records[t]=dict(current=current,lo=self.cache.lo.copy(),hi=self.cache.hi.copy(),pointer=self.pointer,last=self.last_query.copy())
        return r
def oracle(initial_hi,start,target,available,truth,noise,budget):
    covered=(initial_hi+m.L*(target-start)<0).any(axis=1)
    jobs=np.flatnonzero(~covered);times=np.array([s for s in available if start<=s<=target],int)
    slots=np.repeat(times,budget).tolist()
    if not len(jobs):return True,{}
    good=(truth[times]+noise[times]+m.ETA+m.L*(target-times)[:,None,None]<0).any(axis=2)
    expanded=np.repeat(good,budget,axis=0)
    edges=[np.flatnonzero(expanded[:,a]).tolist() for a in jobs]
    result=matching(edges,slots)
    if result['feasible']:
        assigned={int(jobs[a]):s for a,s in result['assignment'].items()}
        for s in set(assigned.values()):assert list(assigned.values()).count(s)<=budget and s in available
        for a,s in assigned.items():assert (truth[s,a]+noise[s,a]+m.ETA+m.L*(target-s)<0).any()
        return True,assigned
    return False,{}
def tests():
    truth=np.full((3,m.N,2),-.3);noise=np.zeros_like(truth)
    assert oracle(np.full((m.N,2),-.1),0,1,[],truth,noise,1)[0]
    assert not oracle(np.ones((m.N,2)),0,1,[],truth,noise,24)[0]
    assert oracle(np.ones((m.N,2)),0,1,[1],truth,noise,24)[0]
    assert not oracle(np.full((m.N,2),-.08),0,2,[],truth,noise,24)[0]
    rng=np.random.default_rng(42)
    for _ in range(100):
        tr=rng.uniform(-.5,.5,(6,m.N,2));nz=rng.uniform(-m.ETA,m.ETA,tr.shape);times=np.array([0,2,5]);target=5
        fast=(tr[times]+nz[times]+m.ETA+m.L*(target-times)[:,None,None]<0).any(axis=2)
        slow=np.array([[(tr[s,a]+nz[s,a]+m.ETA+m.L*(target-s)<0).any() for a in range(m.N)] for s in times])
        np.testing.assert_array_equal(fast,slow)
def package():
    (root/'requirements.txt').write_text('numpy==2.3.5\n')
    (root/'MANIFEST.json').write_text(json.dumps({str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest() for f in root.rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.name!='MANIFEST.json'},indent=2))
    dest=root.parent/'GP_DFPR_Matched_Schedules_v12.zip'
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
        for f in root.rglob('*'):
            if f.is_file() and '__pycache__' not in f.parts:z.write(f,str(Path(root.name)/f.relative_to(root)))
    with zipfile.ZipFile(dest) as z:assert z.testzip() is None
def main():
    old=root.parent/'GP_DFPR_Scheduling_v11.zip'
    with zipfile.ZipFile(old) as z:
        assert z.testzip() is None
        assert z.read('GP_DFPR_Scheduling_v11/REPORT_RU.md')==(root.parent/'GP_DFPR_Scheduling_v11/REPORT_RU.md').read_bytes()
    (root/'V11_CHECKPOINT.json').write_text(json.dumps(dict(archive=old.name,sha256=hashlib.sha256(old.read_bytes()).hexdigest(),report_verified=True),indent=2))
    tests();m.Controller=Recorder;(root/'traces').mkdir(exist_ok=True)
    rows=[];targets=[];contexts=[];reference_runs=replay_checks=upper_checks=0
    for duration in [12,36]:
        for run in range(6000,6012):
            src=root.parent/'GP_DFPR_Periodic_v9/traces'/f'global-d{duration}_{run}.npz';shutil.copyfile(src,root/'traces'/src.name)
            with np.load(src) as d:truth=d['truth'];noise=d['noise']
            empty=~(truth[:m.T]>=0).all(axis=2).any(axis=1);starts=np.flatnonzero(empty&~np.r_[False,empty[:-1]])
            for budget in [4,8]:
                for mult in [1,2]:
                    for origin in ['Pure-sweep','Uncovered-first']:
                        Recorder.instances.clear();m.simulate(truth,noise,origin,budget,mult,run);rec=Recorder.instances[-1].records;reference_runs+=1
                        for start in starts:
                            start=int(start);end=start
                            while end<m.T and empty[end]:end+=1
                            previous=[s for s in rec if s<start]
                            if previous:
                                s=max(previous);state=rec[s];lo=np.maximum(-1,state['lo']-m.L*(start-s));hi=np.minimum(1,state['hi']+m.L*(start-s));pointer=state['pointer'];last=state['last'].copy()
                            else:lo=np.full((m.N,2),-1.);hi=np.full((m.N,2),1.);pointer=0;last=np.full(m.N,-1,int)
                            available=[t for t in rec if start<=t<end];key=dict(duration=duration,run=run,budget=budget,delay_multiplier=mult,origin=origin,episode_start=start)
                            contexts.append(dict(**key,end=end,lo=lo.tolist(),hi=hi.tolist(),pointer=pointer,last=last.tolist(),available=available,current={t:rec[t]['current'] for t in available}))
                            flags={p:[] for p in ['Pure-sweep','Uncovered-first','Oracle']};counts={p:0 for p in ['Pure-sweep','Uncovered-first']};controllers={}
                            for policy in counts:
                                c=Base(policy,budget,mult,run);c.cache.lo=lo.copy();c.cache.hi=hi.copy();c.cache.time=start;c.pointer=pointer;c.last_query=last.copy();controllers[policy]=c
                            for t in range(start,end):
                                exact,_=oracle(hi,start,t,available,truth,noise,budget);flags['Oracle'].append(exact)
                                values={}
                                for policy,c in controllers.items():
                                    if t in rec:
                                        result=c.decision(t,rec[t]['current'],lambda a,exact:truth[t,a]+noise[t,a]);counts[policy]+=result['queries']
                                        if policy==origin:
                                            np.testing.assert_allclose(c.cache.hi,rec[t]['hi'],rtol=0,atol=1e-12);replay_checks+=1
                                    propagated=np.minimum(1,c.cache.hi+m.L*(t-c.cache.time));detected=bool((propagated<0).any(axis=1).all());assert not detected or exact;upper_checks+=1;flags[policy].append(detected);values[policy]=detected
                                targets.append(dict(**key,t=t,oracle=exact,pure_sweep=values['Pure-sweep'],uncovered_first=values['Uncovered-first']))
                            for policy,observed in flags.items():
                                ix=np.flatnonzero(observed);rows.append(dict(**key,policy=policy,steps=end-start,detected=sum(observed),missed=int(not len(ix)),restricted_wait=int(ix[0]) if len(ix) else end-start,queries=counts.get(policy,'not_applicable')))
        print('duration',duration,'complete',flush=True)
    m.write_csv(root/'episodes.csv',rows);m.write_csv(root/'targets.csv',targets);(root/'contexts.json').write_text(json.dumps(contexts))
    summary=[];lines=['# Сравнение при одинаковом кэше и паузах: v12','','Для каждого эпизода начальный кэш, разрешённые моменты измерений, бюджет и путь текущего действия одинаковы. Изменяется только сбор информации. Новые действия не исполняются, поэтому сравнение не оценивает GPR новых политик.','','Oracle знает будущие исходы и для каждого целевого момента строит отдельное допустимое расписание. Его доля достижимых моментов — условная верхняя граница в этом фиксированном контексте, не обещание единого реализуемого расписания.','','| Импульс | Задержка | B | Источник кэша/пауз | Pure-sweep recall | Uncovered recall | Oracle |','|---|---:|---:|---|---:|---:|---:|']
    for duration in [12,36]:
        for mult in [1,2]:
            for budget in [4,8]:
                for origin in ['Pure-sweep','Uncovered-first']:
                    vals=[]
                    for policy in ['Pure-sweep','Uncovered-first','Oracle']:
                        rr=[r for r in rows if (r['duration'],r['delay_multiplier'],r['budget'],r['origin'],r['policy'])==(duration,mult,budget,origin,policy)];n=sum(r['steps'] for r in rr);hit=sum(r['detected'] for r in rr);vals.append(hit/n)
                        summary.append(dict(duration=duration,delay_multiplier=mult,budget=budget,origin=origin,policy=policy,steps=n,detected=hit,recall=hit/n,episodes=len(rr),missed_episodes=sum(r['missed'] for r in rr),restricted_wait=np.mean([r['restricted_wait'] for r in rr])))
                    lines.append(f'| {duration} | {mult} | {budget} | {origin} | '+' | '.join(f'{v:.4f}' for v in vals)+' |')
    m.write_csv(root/'summary.csv',summary)
    paired=[];rng=np.random.default_rng(2026092080)
    for duration in [12,36]:
        for mult in [1,2]:
            for budget in [4,8]:
                for origin in ['Pure-sweep','Uncovered-first']:
                    deltas=[]
                    for run in range(6000,6012):
                        rr=[r for r in rows if (r['duration'],r['delay_multiplier'],r['budget'],r['origin'],r['run'])==(duration,mult,budget,origin,run)]
                        def recall(p):
                            pp=[r for r in rr if r['policy']==p];return sum(r['detected'] for r in pp)/sum(r['steps'] for r in pp)
                        deltas.append(recall('Uncovered-first')-recall('Pure-sweep'))
                    x=np.array(deltas);ci=np.quantile(x[rng.integers(0,12,(10000,12))].mean(axis=1),[.025,.975]);paired.append(dict(duration=duration,delay_multiplier=mult,budget=budget,origin=origin,mean=float(x.mean()),ci_low=float(ci[0]),ci_high=float(ci[1]),n=12))
    m.write_csv(root/'paired.csv',paired)
    checks=dict(reference_runs=reference_runs,episode_contexts=len(contexts),target_problems=len(targets),reference_cache_replay_checks=replay_checks,online_implies_oracle_checks=upper_checks,unit_tests=4,status='PASS');(root/'checks.json').write_text(json.dumps(checks,indent=2));lines+=['',f'Проверки: {checks}.','','Парные интервалы в paired.csv рассчитаны по 12 исходным прогонам, поточечные 95%, без поправки на множественные проверки. Это повторный анализ известных данных. Эпизоды и два источника условий не являются независимыми повторениями. Отдельные расписания oracle могут быть несовместимы между целевыми моментами; это верхняя граница, а не достигнутый результат контроллера.'];(root/'REPORT_RU.md').write_text('\n'.join(lines),encoding='utf-8');package();print('\n'.join(lines),flush=True)
if __name__=='__main__':main()
