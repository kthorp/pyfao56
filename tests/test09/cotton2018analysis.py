import pandas as pd
import numpy as np
#from scipy import stats
import sys

plots = ['p01-1','p01-2','p01-3','p01-4',
         'p02-1','p02-2','p02-3','p02-4',
         'p03-1','p03-2','p03-3','p03-4',
         'p04-1','p04-2','p04-3','p04-4',
         'p05-1','p05-2','p05-3','p05-4',
         'p06-1','p06-2','p06-3','p06-4',
         'p07-1','p07-2','p07-3','p07-4',
         'p08-1','p08-2','p08-3','p08-4',
         'p09-1','p09-2','p09-3','p09-4',
         'p10-1','p10-2','p10-3','p10-4',
         'p11-1','p11-2','p11-3','p11-4',
         'p12-1','p12-2','p12-3','p12-4',
         'p13-1','p13-2','p13-3','p13-4',
         'p14-1','p14-2','p14-3','p14-4',
         'p15-1','p15-2','p15-3','p15-4',
         'p16-1','p16-2','p16-3','p16-4']

colnames=['Plot','Case','IrrNum','IrrSum','IrrMax','ETaSum','ETaRMSD',
          'TrnSum','TrnRMSD','DrAvg','DrMin','DrMax','DrRMSD','KsAvg',
          'KsMin','KsMax','KsRMSD','DPSum','SCYld']
data = pd.DataFrame(columns=colnames)
for plot in ['p06-1']:#plots:
    outfile0 = 'cotton2018'+plot+'case00.out'
    outdata0 = pd.read_csv(outfile0,skiprows=10,sep='\s+')
    for case in list(range(42)):
        outfile = 'cotton2018'+plot+'case'+'{:02d}'.format(case)+'.out'
        outdata = pd.read_csv(outfile,skiprows=10,sep='\s+')
        mydict = dict()
        mydict.update({'Plot':plot})
        mydict.update({'Case':case})
        #Number of irrigations
        mydict.update({'IrrNum':float((outdata['Irrig']>0).sum())})
        #Seasonal irrigation depth
        mydict.update({'IrrSum':(outdata['Irrig']).sum()})
        #Maximum daily irrigation
        mydict.update({'IrrMax':(outdata['Irrig']).max()})
        #Seasonal ETa
        mydict.update({'ETaSum':(outdata['ETa']).sum()})
        #RMSD between ETa from Case X and Case 0.
        caseX = np.array(outdata['ETa'].tolist())
        case0 = np.array(outdata0['ETa'].tolist())
        rmsd = np.sqrt(np.mean((caseX-case0)**2))
        mydict.update({'ETaRMSD':rmsd})
        #Seasonal transpiration
        mydict.update({'TrnSum':(outdata['T']).sum()})
        #RMSD between T from Case X and Case 0.
        caseX = np.array(outdata['T'].tolist())
        case0 = np.array(outdata0['T'].tolist())
        rmsd = np.sqrt(np.mean((caseX-case0)**2))
        mydict.update({'TrnRMSD':rmsd})
        #Mean daily Dr
        mydict.update({'DrAvg' :(outdata['Dr'].head(143)).mean()})
        #Minimum daily Dr
        mydict.update({'DrMin' :(outdata['Dr'].head(143)).min()})
        #Maximum daily Dr
        mydict.update({'DrMax' :(outdata['Dr'].head(143)).max()})
        #RMSD between Dr from Case X and Case 0.
        caseX = np.array(outdata['Dr'].head(143).tolist())
        case0 = np.array(outdata0['Dr'].head(143).tolist())
        rmsd = np.sqrt(np.mean((caseX-case0)**2))
        mydict.update({'DrRMSD':rmsd})
        #Mean daily Ksend
        mydict.update({'KsAvg' :(outdata['Ksend'].head(143)).mean()})
        #Minimum daily Ksend
        mydict.update({'KsMin' :(outdata['Ksend'].head(143)).min()})
        #Maximum daily Ksend
        mydict.update({'KsMax' :(outdata['Ksend'].head(143)).max()})
        #RMSD between Ks from Case X and Case 0.
        caseX = np.array(outdata['Ksend'].head(143).tolist())
        case0 = np.array(outdata0['Ksend'].head(143).tolist())
        rmsd = np.sqrt(np.mean((caseX-case0)**2))
        mydict.update({'KsRMSD':rmsd})
        #Seasonal deep percolation
        mydict.update({'DPSum' :(outdata['DP']).sum()})
        #Estimated seed cotton yield
        Tsum = (outdata['T']).sum()/1000.
        mydict.update({'SCYld':(Tsum-0.3292)/0.1262})
        data.loc[len(data)] = mydict
data.to_csv('cotton2018analysis.csv',index=False)

#datamean = data.groupby('Case').mean()
#datamean.to_csv('cotton2018analysismean.csv',index=False)
#datastd = data.groupby('Case').std()
#datastd.to_csv('cotton2018analysisstd.csv',index=False)

#data100 = data[data['Plot'].isin(['p01-2','p06-1','p09-2','p15-4'])]
#data100case0 = data100[data100['Case']==0]
#print(data100case0)

#f=open('cotton2018analysisstats.csv','w')
#for case in list(range(1,39)):
#    for colname in colnames[2:]:
#        field = np.array(data100case0[colname].tolist())
#        model = np.array(data[data['Case']==case][colname].tolist())
#        tval, pval = stats.ttest_ind(field,model)
#        string = str(case) + ','
#        string += colname + ','
#        string += str(tval) + ','
#        string += str(pval) + '\n'
#        f.write(string)
#f.close()

#datap061 = data[data['Plot']=='p06-1']
#datap061.to_csv('cotton2018analysisp06-1.csv',index=False)
