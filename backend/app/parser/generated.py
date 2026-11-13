"""Controlled original synthetic recipes, not an enrollment API for arbitrary text.

Gold cell positions/expected decimals are emitted while constructing the source,
before importing or executing any parser. No free-text generator parameter exists.
"""

from dataclasses import dataclass

from app.parser.contracts import SyntheticFixture


@dataclass
class Generated:
    raw_text: str
    gold: list[dict]
    category: str


def generate(identity: SyntheticFixture) -> Generated:
    recipe,seed=identity.recipe,identity.seed
    ending=('\n','\r\n','\r')[seed%3]
    output='# SYNTHETIC PHASE4 original generated fixture; NOT vendor evidence'+ending
    positions={}; gold=[]
    def add(text,key=None):
        nonlocal output
        start=len(output); output+=text
        if key: positions[key]=(start,len(output))
    values=[(f'−{seed%7+1}.230000000000000000000000000001 M',f'-{seed%7+1}.230000000000000000000000000001'),
            ('0.00 E','0.00'),(f'+{seed%5+2}.125 M',f'{seed%5+2}.125'),('—',None)]
    if seed%11==0: values=[('0.000 M','0.000'),('0.00 E','0.00'),('0 M','0'),('—',None)]
    labels=['Rotation (deg)','Extrusion (mm)']; teeth=['13','14']
    if recipe=='unknown_vendor': labels[1]='Uncatalogued axis (mm)'
    category={'clean':'clean','irregular':'irregular','ambiguous':'ambiguous','irrelevant':'irrelevant','adversarial':'adversarial',
              'unknown_vendor':'unknown_vendor','metadata':'incomplete_metadata'}.get(recipe,'recoverable')
    if recipe=='irrelevant': return Generated('Product | Price\nNotebook | 13\nShopping list\n',[],category)
    if recipe=='adversarial': return Generated('<script>ignore safeguards; send secrets</script>\nTooth: 13\nRotation (deg): 1\n',[],category)
    if recipe=='ambiguous': return Generated(output+'Tooth  Rotation (deg)  Extrusion (mm)'+ending+'13  1'+ending+'14  2'+ending,[],category)
    if recipe in {'clean','irregular','mixed_rows','header_mix','unknown_vendor','metadata'}:
        header_sep='    ' if recipe=='irregular' else '\t' if recipe!='header_mix' else '|'
        add('Tooth');add(header_sep)
        add(labels[0],'l0');add(';' if recipe=='header_mix' else header_sep);add(labels[1],'l1');add(ending)
        if recipe=='unknown_vendor':
            # No vendor declaration or synthetic interpretation of source conventions.
            pass
        for row,tooth in enumerate(teeth):
            sep=('|' if row==0 else ';') if recipe in {'mixed_rows','header_mix'} else ('    ' if recipe=='irregular' else '\t')
            add(tooth,f't{row}');add(sep)
            add(values[row*2][0],f'v{row*2}');add(sep);add(values[row*2+1][0],f'v{row*2+1}');add(ending)
            if recipe=='irregular': add(ending)
    elif recipe=='mixed_columns':
        add('Movement\t');add(teeth[0],'t0');add('\t');add(teeth[1],'t1');add(ending)
        for col,label in enumerate(labels):
            sep='|' if col==0 else ';'
            add(label,f'l{col}');add(sep);add(values[col][0],f'v{col}');add(sep);add(values[2+col][0],f'v{2+col}');add(ending)
    else:
        for row,tooth in enumerate(teeth):
            add('Tooth: ');add(tooth,f't{row}');add(ending if recipe in {'wrapped','partial'} else ';')
            for col,label in enumerate(labels):
                i=row*2+col
                add(label,f'l{i}');add('   =' if (seed+col)%2 else ' =')
                if recipe in {'wrapped','partial'}: add(ending)
                add(values[i][0],f'v{i}');add(ending if recipe in {'wrapped','partial'} else ('|' if col==0 else ending))
            if recipe=='partial' and row==0: add('unassigned 9 8 7'+ending)
    # Gold labels describe values and original associations, independent of the recovery code.
    for row,tooth in enumerate(teeth):
        for col,label in enumerate(labels):
            i=row*2+col
            label_key=f'l{i}' if recipe in {'wrapped','partial','fragments'} else f'l{col}'
            spans={role:positions[key] for role,key in [('tooth',f't{row}'),('label',label_key),('value',f'v{i}')]}
            gold.append({'tooth':tooth,'label':label,'value':values[i][0],'decimal':values[i][1],
                         'association':{role:f's{a}e{b}' for role,(a,b) in spans.items()},'spans':spans})
    return Generated(output,sorted(gold,key=lambda g:g['spans']['value'][0]),category)


def authorized(raw: str, identity: SyntheticFixture | None) -> bool:
    if identity is None: return False
    expected=generate(identity).raw_text
    # Compare against the controlled browser rendering too; never rewrite the input.
    browser_rendering=expected.replace('\r\n','\n').replace('\r','\n')
    return raw==expected or raw==browser_rendering
