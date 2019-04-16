# ----------- Data Visualisation ----------- #
# Written by Benjamin J. Griffiths
# Created on Friday 26th October, 2018
# ------------------------------------------ #

# %% -- import modules ------------------------------------------------------ #
import matplotlib as mpl
import numpy as np
import pandas
import ptitprince as pt
import seaborn as sns
from matplotlib import pyplot
from matplotlib import transforms

# %% -- define functions ---------------------------------------------------- #
# plot raincloud
def custom_rainplot(data,colour,axes,fontname,labels,ylim,offset,pvalue):
    
    # get transform data
    trans   = axes.transData
    offset  = transforms.ScaledTranslation(offset,0,f.dpi_scale_trans)
    
    # plot violin
    axes=pt.half_violinplot(data = data,bw = "scott",inner = None, scale = "count",
                          width = 0.5, linewidth = 1, cut = 1, palette = colour,
                          ax = axes, edgecolor = [0,0,0])
    
    # plot single points
    axes=sns.swarmplot(data = data, edgecolor =[0,0,0], size = 1.5, 
                       transform = trans + offset, palette = colour,
                       ax = axes)
    
    # plot mean and confidence intervals
    axes=sns.boxplot(data = data, palette = colour, width = 0.1, ax = axes, linewidth = 1, fliersize = 1, whis = 5)
    
    # plot significance
    sig_offset = ylim[1]-(ylim[1]*0.05)
    for i in np.arange(0,np.size(pvalue)):
        if pvalue[i] < 0.001:
            pyplot.scatter(np.array([-0.05,0,0.05])+i,[sig_offset,sig_offset,sig_offset],s=3,c='black',marker='*',edgecolors=None)
        elif pvalue[i] < 0.01:
            pyplot.scatter(np.array([-0.025,0.025])+i,[sig_offset,sig_offset],s=3,c='black',marker='*',edgecolors=None)
        elif pvalue[i] < 0.05:
            pyplot.scatter(np.array([0])+i,[sig_offset],s=3,c='black',marker='*',edgecolors=None)
    
    # add horizontal line
    axes.axhline(y=0, xmin=-1, xmax=3, color=[0,0,0], linewidth = 1)
    
    # aesthetics
    axes.set_ylabel(labels['ylabel'],fontname=fontname,fontsize=7,labelpad=5,fontweight='light')   # add Y axis label
    axes.set_ylim(ylim)                  # set Y axis range to 0 -> 1
    axes.set_xlim(-0.65,-0.5+len(data.columns))                  # set Y axis range to 0 -> 1
    axes.tick_params(axis='x',          # change X tick parameters
                   which='both',          # affect both major and minor ticks
                   bottom=False,          # turn off bottom ticks
                   labelbottom=True,  # keep bottom labels
                   pad=2.5,
                   width=1)   
    axes.tick_params(axis='y',          # change X tick parameters
                       pad=3,
                       width=1,
                       length=2.5)
    axes.set_yticks(labels['yticks'])
    axes.set_xticklabels(labels['xticklabel'],fontname=fontname,fontweight='light',fontsize=6)
    axes.set_yticklabels(labels['yticklabel'],fontname=fontname,fontweight='light',fontsize=6)

    # change axes
    axes.spines['top'].set_visible(False)
    axes.spines['right'].set_visible(False)
    axes.spines['bottom'].set_visible(False)
    axes.spines['left'].set_linewidth(1)
       
def custom_timeseriesplot(data,variables,axes,colour,labels,xlim,ylim,xtick,vertical,horizontal):
    
    sns.lineplot(x=variables['x'],
             y=variables['y'],
             data=data,
             ci='sem',
             hue=variables['condition'],
             palette=colour,
             ax = axes,
             linewidth=1)
        
    # add horizontal line
    if vertical:
        ax.axvline(x=0, linewidth = 1, color = [0,0,0], linestyle='--')
    if horizontal:
        ax.axhline(y=0, linewidth = 1, color = [0,0,0], linestyle='-')
    
    # aesthetics
    ax.set_ylabel(labels['ylabel'],fontname='Calibri',fontsize=6,labelpad=0,fontweight='light')   # add Y axis label
    ax.set_xlabel(labels['xlabel'],fontname='Calibri',fontsize=6,labelpad=3,fontweight='light')   # add Y axis label
    ax.set_ylim(ylim)                  # set Y axis range to 0 -> 1
    ax.set_xlim(xlim)                  # set Y axis range to 0 -> 1  
    ax.set_yticks([ylim[0],0,ylim[1]])
    ax.set_xticks(xtick)
    ax.set_yticklabels([ylim[0],0,ylim[1]],fontname='Calibri',fontweight='light',fontsize=5)
    ax.set_xticklabels(xtick,fontname='Calibri',fontweight='light',fontsize=5)
    ax.tick_params(axis='both',          # change X tick parameters
                       pad=3,
                       length=2.5)
    # change axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # remove legend
    ax.get_legend().remove()
    
# %% -- define key parameters ----------------------------------------------- #
# get current directory
wdir = 'E:/bjg335/projects/reinstatement_fidelity/'

# set context
sns.set_context("paper")

# set plot defaults
mpl.rcParams['xtick.major.width'] = 1
mpl.rcParams['ytick.major.width'] = 1
mpl.rcParams['xtick.color'] = [0,0,0]
mpl.rcParams['ytick.color'] = [0,0,0]
mpl.rcParams['lines.linewidth'] = 1
mpl.rcParams['axes.linewidth'] = 1

# %% ----- RSA Plot ----- # 
# define raincloud data filename
data_fname = wdir + "data/fig1_data/percept_betas.csv"

# load raincloud data
data_raincloud = pandas.read_csv(data_fname,
                       delimiter=",")

# restrict to retrieval data
#data_raincloud = data_raincloud.drop(labels = ['FrontCent','LeftTemp'], axis = 1)
data_raincloud['LeftTemp'][9] = 0

# create figure
f,ax = pyplot.subplots(1,1)
f.set_figheight(5/2.54) # 4inches 
f.set_figwidth(4.8/2.54) # 12inches
f.set_dpi(1000)

# define colour scheme
colour = sns.color_palette("Reds",n_colors=7)
colour = [colour[2],colour[3]]

# define labels
labels = {'title':'',
          'ylabel':'Similarity Index (z)',
          'xticklabel':['Occipital','Frontal','Temporal'],
          'yticks':[-0.05,0,0.05,0.1,0.15],
          'yticklabel':['-0.05','0','0.05','0.1','0.15']}

# plot raincloud
custom_rainplot(data_raincloud,colour,ax,'calibri',labels,[-0.05,0.15],0.125,[1,1,1])
   
# save image
pyplot.savefig(wdir + "/figures/fig4a.tif",bbox_inches='tight',transparent=True,dpi='figure')

# %% ----- Power Plot ----- # 
# define raincloud data filename
data_fname = wdir + "data/fig2_data/group_task-rf_eeg-cluster.csv"

# load raincloud data
data_raincloud = pandas.read_csv(data_fname,
                       delimiter=",")

# restrict to retrieval data
data_raincloud = data_raincloud.drop(labels = ['retrieval','rse'], axis = 1)

# create figure
f,ax = pyplot.subplots(1,1)
f.set_figheight(6/2.54) # 4inches 
f.set_figwidth(3/2.54) # 12inches
f.set_dpi(1000)

# define colour scheme
colour = sns.color_palette("Blues",n_colors=7)
colour = [colour[3]]

# define labels
labels = {'title':'',
          'ylabel':'Alpha/Beta Power (Post-Stim. > Pre-Stim.; z)',
          'xticklabel':[''],
          'yticks':[-0.5,-0.25,0,0.25],
          'yticklabel':['-0.5','-0.25','0','0.25']}

# plot raincloud
custom_rainplot(data_raincloud,colour,ax,'calibri',labels,[-0.5,0.25],0.125,[1])
   
# save image
pyplot.savefig(wdir + "/figures/fig4b.tif",bbox_inches='tight',transparent=True,dpi='figure')


# -- prep frequency
# load frequency data
datatmp = pandas.read_csv(wdir + "data/fig2_data/group_task-percept_eeg-freqseries.csv",
                                 delimiter=',',
                                 header=None)

# create new structure for frequency data
data_frequency = pandas.DataFrame(data=np.reshape(datatmp.values,[datatmp.size]),columns=['signal'])

# create subject number array
data_frequency = data_frequency.assign(subj=pandas.Series(np.repeat(np.arange(0,21),[150])).values)
    
# create condition array
data_frequency = data_frequency.assign(condition=pandas.Series(np.tile(np.append(np.ones(75),np.zeros(75)),[21])).values)

# create frequency array
data_frequency = data_frequency.assign(frequency=pandas.Series(np.tile(np.linspace(3,40,75),[42])).values)

# get freq diff
data_freqA = data_frequency[data_frequency['condition']==1];
data_freqB = data_frequency[data_frequency['condition']==0];
data_freqA = data_freqA.reset_index()
data_freqB = data_freqB.reset_index()

# create new frame
data_freqdiff = data_freqA
data_freqdiff['signal'] = data_freqA['signal']-data_freqB['signal']

# create figure
f,ax = pyplot.subplots(1,1)
f.set_figheight(2.5/2.54) # 4inches 
f.set_figwidth(3.8/2.54) # 12inches
f.set_dpi(1000)

# define colour scheme
colour = sns.color_palette("Blues",n_colors=7)
colour = [colour[5]]

# define labels and variables
labels = {'legend':[''],
          'ylabel':'Power\n(Post > Pre; z)',
          'xlabel':'Frequency (Hz.)'}

variables = {'x':'frequency',
             'y':'signal',
             'condition':'condition'}

# plot frequency series
custom_timeseriesplot(data_freqdiff,variables,ax,colour,labels,[3,40],[-0.5,0.1],[5,10,15,20,25,30,35,40],True,True)

# save image
pyplot.savefig(wdir + "/figures/fig4c.tif",bbox_inches='tight',transparent=True,dpi='figure')


# -- prep time
# load frequency data
datatmp = pandas.read_csv(wdir + "data/fig2_data/group_task-percept_eeg-timeseries.csv",
                                 delimiter=',',
                                 header=None)

# create new structure for frequency data
data_time = pandas.DataFrame(data=np.reshape(datatmp.values,[datatmp.size]),columns=['signal'])

# create subject number array
data_time = data_time.assign(subj=pandas.Series(np.repeat(np.arange(0,21),[61])).values)
    
# create condition array
data_time = data_time.assign(condition=pandas.Series(np.tile(np.zeros(61),[21])).values)

# create frequency array
data_time = data_time.assign(frequency=pandas.Series(np.tile(np.linspace(-1,2,61),[21])).values)

# create figure
f,ax = pyplot.subplots(1,1)
f.set_figheight(2.5/2.54) # 4inches 
f.set_figwidth(3.8/2.54) # 12inches
f.set_dpi(1000)

# define colour scheme
colour = sns.color_palette("Blues",n_colors=7)
colour = [colour[5]]

# define labels and variables
labels = {'legend':[''],
          'ylabel':'Power(z)',
          'xlabel':'Time (s)'}

variables = {'x':'frequency',
             'y':'signal',
             'condition':'condition'}

# plot frequency series
custom_timeseriesplot(data_time,variables,ax,colour,labels,[-0.5,2],[-0.25,0.25],[-0.5,0,0.5,1,1.5,2],True,True)

# save image
pyplot.savefig(wdir + "/figures/fig4d.tif",bbox_inches='tight',transparent=True,dpi='figure')

# %% ----- Correlation Plot ----- # 
# define raincloud data filename
data_fname = wdir + "data/fig3_data/group_task-all_eeg-cluster.csv"

# load raincloud data
data_raincloud = pandas.read_csv(data_fname,
                       delimiter=",")

# restrict to retrieval data
data_raincloud = data_raincloud.drop(labels = ['retrieval','forgotten','per_noBold','ret_noBold','ret_noConf'], axis = 1)

# create figure
f,ax = pyplot.subplots(1,1)
f.set_figheight(6/2.54) # 4inches 
f.set_figwidth(3/2.54) # 12inches
f.set_dpi(1000)

# define colour scheme
colour = sns.color_palette("Greens",n_colors=7)
colour = [colour[2],(0.7,0.7,0.7)]

# define labels
labels = {'title':'',
          'ylabel':'Power-Similarity Correlation (z)',
          'xticklabel':[''],
          'yticks':[-0.4,-0.2,0,0.2,0.4],
          'yticklabel':['-0.4','-0.2','0','0.2','0.4']}

# plot raincloud
custom_rainplot(data_raincloud,colour,ax,'calibri',labels,[-0.4,0.4],0.125,[0.033])
   
# save image
pyplot.savefig(wdir + "/figures/fig4e.tif",bbox_inches='tight',transparent=True,dpi='figure')
