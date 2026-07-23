# -*- coding: utf-8 -*-
import json
p=r'c:\Users\szy\Desktop\xinji\8005多仓位AGV\rcs\riot-behavior-lab\evidence\rounds\2026-07-20-round-16\runs\S1-dense-samples.json'
a=json.load(open(p,encoding='utf-8'))
exec=[x for x in a if x.get('orderState')==3]
rems=[]; 
for x in exec:
    r=x.get('remainCost')
    if r not in rems: rems.append(r)
print('execSamples', len(exec))
print('uniqueRemains', rems)
print('last', a[-1].get('orderState'), a[-1].get('station'), a[-1].get('remainCost'), a[-1].get('procState'))
w=json.load(open(r'c:\Users\szy\Desktop\xinji\8005多仓位AGV\rcs\riot-behavior-lab\evidence\rounds\2026-07-20-round-16\runs\S2-watch-after-cancelA.json',encoding='utf-8'))
for row in w:
    print('A=%s B=%s C=%s Cexec=%s' % (row['A']['orderState'], row['B']['orderState'], row['C']['orderState'], row['C'].get('executeVehicleKey')))
