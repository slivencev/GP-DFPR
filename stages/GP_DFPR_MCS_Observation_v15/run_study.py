from pathlib import Path
import json,csv,hashlib,zipfile,sys
import numpy as np
import observation as o
sys.stdout.reconfigure(encoding='utf-8');root=Path(__file__).resolve().parent
def save(name,rows):
    with (root/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def package():
    (root/'requirements.txt').write_text('numpy==2.3.5\n')
    (root/'MANIFEST.json').write_text(json.dumps({str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='MANIFEST.json'},indent=2))
    dest=root.parent/'GP_DFPR_MCS_Observation_v15.zip'
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
        for p in root.rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts:z.write(p,str(Path(root.name)/p.relative_to(root)))
    with zipfile.ZipFile(dest) as z:assert z.testzip() is None
def main():
    old=root.parent/'GP_DFPR_Observation_Model_v14.zip'
    with zipfile.ZipFile(old) as z:
        assert z.testzip() is None
        assert z.read('GP_DFPR_Observation_Model_v14/OBSERVATION_MODEL_RU.md')==(root.parent/'GP_DFPR_Observation_Model_v14/OBSERVATION_MODEL_RU.md').read_bytes()
    (root/'V14_CHECKPOINT.json').write_text(json.dumps(dict(archive=old.name,sha256=hashlib.sha256(old.read_bytes()).hexdigest(),verified=True),indent=2))
    for curve in o.CURVES.values():
        assert np.all(np.diff(curve['sinr_db'])>0) and np.all(np.diff(curve['code_bler'])<=0)
    b0,b1,g0,g1,_=o.predict(np.array([6.]),np.array([0]),np.array([2]),1,'Interval')
    np.testing.assert_allclose(b0,o.bler(np.array([6.+.2+.08*3])))
    np.testing.assert_allclose(b1,o.bler(np.array([6.-.2-.08*3])))
    assert np.all(g0<=g1)
    rows=[];(root/'traces').mkdir(exist_ok=True);times=np.arange(2,o.T);audited=0
    for run in range(7000,7030):
        gamma,noise=o.plant(run);np.savez_compressed(root/'traces'/f'{run}.npz',gamma_db=gamma,noise_db=noise)
        for period in [1,4,8]:
            sampled=((times-o.LATENCY)//period)*period;z=gamma[sampled]+noise[sampled]
            for horizon in [1,3]:
                predictions={method:o.predict(z,sampled,times,horizon,method) for method in ['Point','Interval','Interval-plus-model']}
                for shift in [0.,.35,.70]:
                    truth=o.bler(gamma[times+horizon]-shift);eff=o.EFF*(1-truth);feasible=(truth<=.1)&(eff>=.5)
                    for method,(lo,hi,glo,ghi,support) in predictions.items():
                        contain=(lo<=truth+1e-12)&(truth<=hi+1e-12)&(glo<=eff+1e-12)&(eff<=ghi+1e-12)
                        safe=(hi<=.1)&(glo>=.5);bad=(lo>.1)|(ghi<.5)
                        false_safe=safe&~feasible;false_bad=bad&feasible
                        guaranteed=(method=='Interval' and shift==0) or (method=='Interval-plus-model' and shift<=.4)
                        if guaranteed:
                            assert contain.all() and not false_safe.any() and not false_bad.any();audited+=int(contain.size)
                        rows.append(dict(run=run,measurement_period=period,horizon=horizon,shift_db=shift,predictor=method,candidate_decisions=int(truth.size),observations_consumed=len(np.unique(sampled)),contained=int(contain.sum()),predicted_feasible=int(safe.sum()),false_feasible=int(false_safe.sum()),predicted_infeasible=int(bad.sum()),false_infeasible=int(false_bad.sum()),unknown=int((~(safe|bad)).sum()),within_table_domain=int(support.sum()),mean_bler_width=float((hi-lo).mean())))
    save('per_case.csv',rows);summary=[]
    lines=['# Измерение общего канала и оценка нескольких MCS: v15','','Проверен тракт «одна шумная оценка SINR → интервалы для MCS 4/10/15». Истина альтернатив доступна только оценщику. Это эксперимент с компонентной аппроксимацией, не запуск ns-3 или проверка реальной RAN.','','Источник кривых — [5G-LENA, NrEesmT1](https://cttc-lena.gitlab.io/nr/html/structns3_1_1_nr_eesm_t1.html), ранее извлечённые BG1/CBS3840. Предиктор и оценщик используют одни таблицы; внесённый сдвиг SINR — специально заданная ошибка модели. Независимость физической модели здесь не проверяется.','','| Сдвиг, дБ | Предиктор | Покрытие интервалами | Допущено | Ошибочных допусков / допущенных | UNKNOWN | Внутри диапазона таблиц |','|---|---|---:|---:|---:|---:|---:|']
    for shift in [0.,.35,.70]:
        for method in ['Point','Interval','Interval-plus-model']:
            rr=[r for r in rows if r['shift_db']==shift and r['predictor']==method];keys=['candidate_decisions','contained','predicted_feasible','false_feasible','predicted_infeasible','false_infeasible','unknown','within_table_domain'];s={k:sum(r[k] for r in rr) for k in keys};n=s['candidate_decisions'];ad=s['predicted_feasible'];summary.append(dict(shift_db=shift,predictor=method,**s))
            lines.append(f'| {shift:.2f} | {method} | {s["contained"]/n:.4f} | {ad/n:.4f} | {s["false_feasible"]}/{ad} | {s["unknown"]/n:.4f} | {s["within_table_domain"]/n:.4f} |')
    save('summary.csv',summary);checks=dict(source_curve_monotonicity='PASS',age_and_latency_checks='PASS',conditional_containment_checks=audited,hard_assumption_failures=0,synthetic_trajectories=30,predictor_case_rows=len(rows),all_candidate_evaluations=sum(r['candidate_decisions'] for r in rows));(root/'checks.json').write_text(json.dumps(checks,indent=2))
    lines+=['',f'Проверки: {checks}.','','Допуски в таблице основаны на BLER<=0.1 и success-weighted nominal efficiency>=0.5; это не измеренная пропускная способность. Количество наблюдений считается по одному общему отчёту для трёх MCS. Коррелированные настройки/альтернативы не являются независимыми экспериментами.','','Расширение кривых плато 1/0 за пределами узлов — явное допущение суррогата. Колонка области таблиц показывает, насколько часто весь предиктивный диапазон находится внутри опубликованных узлов. Даже внутри этих узлов погрешность переноса на реальную сеть не установлена. Синтетическая проверка интервальной арифметики не заменяет её калибровку.'];(root/'REPORT_RU.md').write_text('\n'.join(lines),encoding='utf-8');package();print('\n'.join(lines))
if __name__=='__main__':main()
