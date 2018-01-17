import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys
import math
import os
from argparse import ArgumentParser


parser = ArgumentParser(description='Create volcano plot from spreadsheet of \
                        p-values and fold changes')
parser.add_argument('-i', '--input', dest='input_file', required=True,
                    help='input spreadsheet file (.csv, .xls, .xlsx)',
                    metavar='FILE')
parser.add_argument('-o', '--ouput', dest='output_file',
                    help='output file (.png, .pdf)', metavar='FILE')
parser.add_argument('-p', '--pvalue', dest='pvalue',
                    help='p-value threshold for genes of interest',
                    metavar='PVALUE', nargs='?', const=0.05, type=float,
                    default=0.05)
parser.add_argument('-f', '--foldchange', dest='foldchange',
                    help='fold change threshold for genes of interest',
                    metavar='FOLDCHANGE', nargs='?', const=2, type=float,
                    default=2)

args = parser.parse_args()

INPUT_FILENAME, INPUT_EXTENSION = os.path.splitext(args.input_file)
_, OUTPUT_EXTENSION = os.path.splitext(args.output_file)
P_VAL_THRESH = args.pvalue
FC_THRESH = args.foldchange

if INPUT_EXTENSION == '.csv':
    df = pd.read_csv(args.input_file)
elif INPUT_EXTENSION in ['.xls', '.xlsx']:
    df = pd.read_excel(io=args.input_file)
else:
    sys.exit('ERROR: {} is not .csv, .xls, \
            or .xlsx file'.format(args.input_file))

df['neglog_p_value'] = np.negative(np.log10(df['p_value']))
df['log2_fc'] = np.log2(df['fold_change'])

df['goi'] = np.where((df['p_value'] < args.pvalue) &
            (np.absolute(df['log2_fc']) >= math.log(args.foldchange,2)),
            np.where(df['log2_fc'] > 0, '#2c7bb6','#d7191c'), 'black')

X_MAX = round(max(abs(df['log2_fc'].min()), abs(df['log2_fc'].max()))*1.1,1)
X_MIN = -X_MAX
Y_MIN = 0
Y_MAX = df['neglog_p_value'].max()
NEG_LOG_P_THRESH = -math.log(args.pvalue,10)
LOG_FC_THRESH_POS = math.log(args.foldchange,2)
LOG_FC_THRESH_NEG = -LOG_FC_THRESH_POS

plt.rcParams.update({'mathtext.default': 'regular'})
plt.rcParams.update({'figure.figsize': [12.0, 8.0]})

plt.scatter(df['log2_fc'], df['neglog_p_value'], c=df['goi'])
plt.xlabel('$log_2(Fold\ change)$', fontsize=20)
plt.ylabel('$-log_{10}(\mathit{p}-value)$', fontsize=20)
plt.axis([X_MIN,X_MAX,Y_MIN,Y_MAX])
#plt.xticks(np.arange(X_MIN, X_MAX, 1.0))
plt.plot([X_MIN,LOG_FC_THRESH_NEG],[NEG_LOG_P_THRESH,NEG_LOG_P_THRESH], color='grey', linestyle='--')
plt.plot([LOG_FC_THRESH_POS,X_MAX],[NEG_LOG_P_THRESH,NEG_LOG_P_THRESH],color='grey', linestyle='--')
plt.plot([LOG_FC_THRESH_NEG,LOG_FC_THRESH_NEG],[NEG_LOG_P_THRESH,Y_MAX], color='grey', linestyle='--')
plt.plot([LOG_FC_THRESH_POS,LOG_FC_THRESH_POS],[NEG_LOG_P_THRESH,Y_MAX], color='grey', linestyle='--')
print(plt.xlim())
plt.savefig(args.output_file, dpi=600)
