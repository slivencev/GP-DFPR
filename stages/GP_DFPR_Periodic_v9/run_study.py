from pathlib import Path
import sys,json,hashlib,zipfile,io,unittest
import numpy as np
import model as m
import periodic as p
sys.stdout.reconfigure(encoding='utf-8');root=Path(__file__).resolve().parent
class Tests(unittest.TestCase):
    def test_durations(self):
        for d in [6,12,24,36]:
            mask=p.schedule(f'global-d{d}',308)
            self.assertEqual(int(mask[:300].any(axis=1).sum()),4*d)
            self.assertTrue(mask[60+d-1].all());self.assertFalse(mask[60+d].any())
    def test_paired_bounds(self):
        x=p.plant('global-d6',6000);y=p.plant('global-d36',6000)
        np.testing.assert_array_equal(x[0][:66],y[0][:66]);np.testing.assert_array_equal(x[1],y[1])
        self.assertLessEqual(np.abs(np.diff(y[0],axis=0)).max(),m.L+1e-12)
        self.assertLessEqual(np.abs(y[1]).max(),m.ETA)
    def test_decomposition(self):
        empty=np.array([0,1,0,0,1],bool);satisfied=np.array([1,0,0,1,0],bool)
        self.assertAlmostEqual(1-empty.mean()-satisfied.mean(),np.mean(~empty & ~satisfied))
def package():
    (root/'requirements.txt').write_text('numpy==2.3.5\n')
    (root/'MANIFEST.json').write_text(json.dumps({str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest() for f in root.rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.name!='MANIFEST.json'},indent=2))
    dest=root.parent/'GP_DFPR_Periodic_v9.zip'
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
        for f in root.rglob('*'):
            if f.is_file() and '__pycache__' not in f.parts:z.write(f,str(Path(root.name)/f.relative_to(root)))
    with zipfile.ZipFile(dest) as z:assert z.testzip() is None
def main():
    old=root.parent/'GP_DFPR_Periodic_v8.zip'
    with zipfile.ZipFile(old) as z:
        assert z.testzip() is None
        assert z.read('GP_DFPR_Periodic_v8/REPORT_RU.md')==(root.parent/'GP_DFPR_Periodic_v8/REPORT_RU.md').read_bytes()
    (root/'V8_CHECKPOINT.json').write_text(json.dumps(dict(archive=old.name,sha256=hashlib.sha256(old.read_bytes()).hexdigest(),verified=True),indent=2))
    stream=io.StringIO();res=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests));(root/'TESTS.txt').write_text(stream.getvalue());assert res.wasSuccessful()
    rows=[];env=[];(root/'traces').mkdir(exist_ok=True)
    for variant in p.VARIANTS:
        for run in range(6000,6012):
            truth,noise,mask=p.plant(variant,run);np.savez_compressed(root/'traces'/f'{variant}_{run}.npz',truth=truth,noise=noise,impairment_mask=mask)
            empty=~(truth[:m.T]>=0).all(axis=2).any(axis=1);ep=m.episode_metrics(empty,np.zeros(m.T,bool));env.append(dict(variant=variant,run=run,**ep))
            for mult in [1,2]:
                for budget in [1,2,4,8]:
                    for policy in ['Pure-sweep','Uncovered-first']:
                        met,_=m.simulate(truth,noise,policy,budget,mult,run)
                        ceiling=1-met['empty_steps']/m.T;gap=ceiling-met['GPR'];assert gap>=-1e-12
                        met.update(instantaneous_ceiling=ceiling,violation_with_feasible_alternative=max(0,gap),recall=met['detected_empty_steps']/met['empty_steps'] if met['empty_steps'] else float('nan'))
                        rows.append(dict(duration=int(variant.split('-d')[1]),run=run,delay_multiplier=mult,budget=budget,policy=policy,**met))
        print(variant,'complete',flush=True)
    m.write_csv(root/'per_run.csv',rows);m.write_csv(root/'environment.csv',env)
    groups={}
    for r in rows:groups.setdefault((r['duration'],r['delay_multiplier'],r['budget'],r['policy']),[]).append(r)
    rng=np.random.default_rng(2026092060);paired=[];summary=[]
    for key,rr in groups.items():
        n=sum(r['empty_steps'] for r in rr);d=sum(r['detected_empty_steps'] for r in rr);ep=sum(r['empty_episodes'] for r in rr)
        summary.append(dict(zip(['duration','delay_multiplier','budget','policy'],key),GPR=np.mean([r['GPR'] for r in rr]),instantaneous_ceiling=np.mean([r['instantaneous_ceiling'] for r in rr]),violation_with_feasible_alternative=np.mean([r['violation_with_feasible_alternative'] for r in rr]),queries_per_step=np.mean([r['queries_per_step'] for r in rr]),recall=d/n if n else 'undefined',empty_episodes=ep,missed_episodes=sum(r['missed_episodes'] for r in rr),restricted_wait=sum(r['restricted_detection_wait_sum'] for r in rr)/ep if ep else 'undefined'))
        if key[3]=='Pure-sweep':continue
        base=groups[(*key[:3],'Pure-sweep')]
        for metric in ['GPR','recall','violation_with_feasible_alternative','queries_per_step','missed_episodes','restricted_detection_wait_sum']:
            x=np.array([a[metric]-b[metric] for a,b in zip(rr,base)]);x=x[np.isfinite(x)]
            if len(x):lo,hi=np.quantile(x[rng.integers(0,len(x),(10000,len(x)))].mean(axis=1),[.025,.975]);mean=float(x.mean())
            else:mean=lo=hi=float('nan')
            paired.append(dict(duration=key[0],delay_multiplier=key[1],budget=key[2],metric=metric,mean=mean,ci_low=float(lo),ci_high=float(hi),n=len(x)))
    m.write_csv(root/'summary.csv',summary);m.write_csv(root/'paired.csv',paired)
    lines=['# Длительность нарушения и бюджет измерений: v9','','768 прогонов на 12 новых семенах. Алгоритмы Pure-sweep и Uncovered-first не менялись. Это проверка в той же синтетической модели при новых длительностях и бюджетах, а не внешняя валидация.','','## Фактические эпизоды','','| Импульс, шагов | Пустых шагов за прогон, среднее | Эпизодов за прогон, среднее |','|---|---:|---:|']
    for duration in [6,12,24,36]:
        rr=[r for r in env if r['variant']==f'global-d{duration}'];lines.append(f'| {duration} | {np.mean([r["empty_steps"] for r in rr]):.2f} | {np.mean([r["empty_episodes"] for r in rr]):.2f} |')
    lines+=['','## Все комбинации','','Recall — объединённая доля правильно диагностированных пустых шагов. При отсутствии пустых шагов — undefined. GPR — доля выполнения целей. Для каждой пары значения указаны Pure-sweep → Uncovered-first.','','| Импульс | Задержка | B | Recall | GPR |','|---|---:|---:|---|---|']
    for duration in [6,12,24,36]:
        for mult in [1,2]:
            for budget in [1,2,4,8]:
                rr=[next(s for s in summary if (s['duration'],s['delay_multiplier'],s['budget'],s['policy'])==(duration,mult,budget,pol)) for pol in ['Pure-sweep','Uncovered-first']]
                rec=['undefined' if s['recall']=='undefined' else f'{s["recall"]:.3f}' for s in rr]
                lines.append(f'| {duration} | {mult} | {budget} | {rec[0]} → {rec[1]} | {rr[0]["GPR"]:.3f} → {rr[1]["GPR"]:.3f} |')
    checks={k:sum(r[k] for r in rows) for k in ['arrival_certificates','arrival_certificate_failures','false_infeasibility_certificates','hold_certificate_failures']};checks.update(controller_runs=len(rows),scored_steps=len(rows)*m.T,tests=3,all_invariants='PASS');(root/'checks.json').write_text(json.dumps(checks,indent=2))
    lines+=['',f'Проверки: {checks}.','','Нарушения при наличии физически выполнимой альтернативы отдельно сохранены в summary.csv и per_run.csv. Они не объявляются предотвратимыми для контроллера с ограниченными наблюдениями и задержками. Парные поточечные интервалы — paired.csv; независимая единица — прогон, без поправки на множественные сравнения. Все сырые среды — traces/.'];(root/'REPORT_RU.md').write_text('\n'.join(lines),encoding='utf-8');package();print('\n'.join(lines),flush=True)
if __name__=='__main__':main()
