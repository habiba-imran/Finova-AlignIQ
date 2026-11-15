"""Original, complete fictional datasets. Loading never grants TEST_ONLY authority."""
from app.functional.models import FunctionalContext
from app.interactive.models import InteractiveSubmission, ReviewDetails
from app.parser.receipts import resolve
import hashlib

HEADERS = 'Tooth\tRotation (deg)\tAngulation (deg)\tInclination (deg)\tVertical (mm)\tRelative Ext / Int (mm)\tTranslation B / L (mm)\tTranslation M / D (mm)'
FIELDS = ('rotation','angulation','inclination','vertical','relative_vertical','buccolingual','mesiodistal')


def scenario(scenario_id):
    if scenario_id not in {'macro-distribution','micro-catalog','nano-phases'}:
        raise KeyError('SCENARIO_NOT_FOUND')
    module = scenario_id.split('-')[0]
    tokens = ([str(q)+str(n) for q in (1,2) for n in range(1,9)] if module == 'macro' else
        [str(n) for n in range(11,19)] if module == 'micro' else ['11','21','16','26','31','41','36','46'])
    # These zeros are authored scenario cells, never a repair of user source data.
    rows = {t:['0.00']*7 for t in tokens}
    if module == 'macro':
        rows.update({'11':['2.00 D','1.00 D','1.00 B','1.00 I','0.20 I','1.60 L','1.00 D'],
            '12':['0.50 D','0.00','1.00 B','1.00 I','0.50 I','0.40 B','1.50 D'],
            '16':['1.00 D','0.50 D','0.00','0.00','0.00','0.20 B','2.00 D'],
            '17':['1.20 D','0.20 D','0.00','0.00','0.00','0.20 B','2.00 D'],
            '21':['1.00 D','0.50 D','0.50 B','1.00 I','0.20 I','1.60 L','1.00 D']})
    elif module == 'micro':
        rows.update({'11':['2.00 D','1.00 D','0.00','0.00','0.00','0.00','0.00'],
            '12':['2.00 D','0.00','0.00','0.00','0.00','0.00','0.00'],
            '13':['0.00','1.00 D','0.00','0.00','0.00','0.00','0.00'],
            '14':['0.00','0.00','1.00 B','0.00','0.00','0.00','0.00'],
            '15':['0.00','0.00','0.00','1.00 I','0.20 I','0.00','0.00'],
            '17':['—','0.00','0.00','0.00','0.00','0.00','0.00'],
            '18':['0.00','0.00','0.00','0.00','0.00','0.00','1.00 D']})
    else:
        rows.update({'11':['2.00 D','0.00','0.00','0.00','0.00','1.00 L','0.00'],
            '21':['0.00','0.00','0.00','0.60 I','0.00','0.00','0.00'],
            '31':['0.00','0.00','0.00','0.00','0.00','0.00','1.20 D'],
            '41':['0.00','1.00 M','0.00','0.00','0.00','0.00','0.00']})
    raw = '# SYNTHETIC FUNCTIONAL SCENARIO — '+scenario_id+'\n'+HEADERS+'\n'+'\n'.join(t+'\t'+'\t'.join(rows[t]) for t in tokens)
    digest = hashlib.sha256(raw.encode()).hexdigest()
    request = InteractiveSubmission(raw_text=raw,raw_sha256=digest,synthetic_data_confirmed=True,module=module)
    parsed = resolve(request)
    tooth_refs = {t.token:t.id for t in parsed.teeth}
    cells = {(next(t.token for t in parsed.teeth if t.id == m.tooth_ref),m.recognized_label):m for m in parsed.measurements}
    context = dict(scenario_id=scenario_id,source_sha256=digest,module=module,notation='FDI')
    details = ReviewDetails()
    if module == 'macro':
        context['objectives'] = ['REDISTRIBUTE_TRANSLATIONS','VERTICAL_REVIEW','ANGULAR_CONTROL']
        targets = [('16','mesiodistal','1.00'),('17','mesiodistal','1.00'),('11','buccolingual','1.20'),('21','buccolingual','1.20'),('12','vertical','0.80'),('11','rotation','1.50')]
        context['targets'] = [dict(measurement_ref=cells[t,f].id,amount=amount,unit=cells[t,f].unit,source_direction=cells[t,f].raw_direction) for t,f,amount in targets]
    elif module == 'micro':
        options = []
        for concept,dims,orientation in [('RECTANGULAR',('2.000','2.000','0.800'),'UNSPECIFIED'),
            ('VERTICAL_RECTANGULAR',('2.000','3.000','1.000'),'VERTICAL'),
            ('HORIZONTAL_RECTANGULAR',('3.000','2.000','1.000'),'HORIZONTAL'),
            ('OVAL',('2.000','2.500','0.800'),'UNSPECIFIED')]:
            options.append(dict(concept=concept,geometry=dict(zip(('width_mm','height_mm','depth_mm'),dims)),orientation=orientation,
                surface='BUCCAL',placement=dict(frame='FICTIONAL_TOOTH_LOCAL_MM',x_mm='0.000',y_mm='0.000',z_mm='0.000')))
        options += [dict(concept='OPTIMIZED_STYLE'),dict(concept='NO_ATTACHMENT')]
        context['attachment_options'] = options
    else:
        context.update(objectives=['STAGE_REVIEW'],stage_value_basis='INCREMENTS_MATCH_SOURCE_LABELS',
            phases=[dict(phase_id='P1',label='Initial supplied allocations',stage_ids=['S1']),dict(phase_id='P2',label='Translation follow-through',stage_ids=['S2']),dict(phase_id='P3',label='Angular finishing',stage_ids=['S3'])])
        allocations = [('S1','11','buccolingual','0.40'),('S2','11','buccolingual','0.60'),('S3','11','rotation','2.00'),
            ('S1','21','vertical','0.20'),('S2','21','vertical','0.40'),('S1','31','mesiodistal','0.50'),('S2','31','mesiodistal','0.70'),
            ('S3','41','angulation','1.00'),('S1','16','rotation','0.00'),('S2','26','rotation','0.00'),('S1','36','rotation','0.00'),('S3','46','rotation','0.00')]
        details = ReviewDetails(stages=[dict(stage_id=f'S{i}',order=i) for i in range(1,4)],allocations=[dict(stage_id=s,tooth_ref=tooth_refs[t],measurement_ref=cells[t,f].id,amount=amount,unit=cells[t,f].unit) for s,t,f,amount in allocations])
        context['support_constraints'] = [dict(phase_id=p,support_tooth_refs=[tooth_refs[t] for t in support],active_tooth_refs=[tooth_refs[t] for t in active],assumption='STATIONARY_IN_FICTIONAL_SCENARIO') for p,support,active in [('P1',['16','36'],['11','21','31']),('P2',['26'],['11','21','31']),('P3',['46'],['11','41'])]]
    return dict(label={'macro':'Fictional distribution modification','micro':'Fictional attachment catalog','nano':'Fictional phases and support groups'}[module],module=module,raw_text=raw,planning_context=FunctionalContext(**context).model_dump(mode='json'),review_details=details.model_dump(mode='json'))
