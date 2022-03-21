'''
Auxiliary functions for WAKIS results plotting:
- Longitudinal wake potential
- Longitudinal Impedance 
- Transverse wake potential
- Transverse Impedance
'''

import numpy as np
import os 
import matplotlib.pyplot as plt
import scipy.constants as spc  
import pickle as pk
import h5py as h5py

UNIT = 1e-3 #conversion to m
CST_PATH = '/mnt/c/Users/elefu/Documents/CERN/WAKIS/Scripts/CST/' 
OUT_PATH = CST_PATH #os.getcwd() + '/'

def read_WarpX_out(out_path=OUT_PATH):
    #--- read the dictionary
    with open(out_path+'input_data.txt', 'rb') as handle:
        input_data = pk.loads(handle.read())
    return input_data

def read_CST_out(cst_out_path=CST_PATH):
    with open(cst_out_path+'cst_out.txt', 'rb') as handle:
        cst_data = pk.loads(handle.read())
    return cst_data

def read_WAKIS_out(out_path=OUT_PATH):
    if os.path.exists(out_path+'wake_solver.txt'):
        with open(out_path+'wake_solver.txt', 'rb') as handle:
            wakis_data = pk.loads(handle.read())
    else: wakis_data=None 

    return wakis_data 

def plot_long_WP(data=read_WAKIS_out(out_path=OUT_PATH), cst_data=read_CST_out(CST_PATH), flag_compare_cst=True):
    # Obtain WAKIS variables
    WP=data.get('WP')
    s=data.get('s')

    # Obtain CST variables
    WP_cst=cst_data.get('WP_cst')
    s_cst=cst_data.get('s_cst')

    #Plot longitudinal wake potential W||(s) & comparison with CST 
    fig = plt.figure(1, figsize=(6,4), dpi=200, tight_layout=True)
    ax=fig.gca()
    ax.plot(s*1.0e3, WP, lw=1.2, color='orange', label='$W_{||}$(0,0)(s)')
    if flag_compare_cst:
        ax.plot(s_cst*1e3, WP_cst, lw=1.3, color='black', ls='--', label='$W_{//}$(s) CST')
    ax.set(title='Longitudinal Wake potential $W_{||}$(s)',
            xlabel='s [mm]',
            ylabel='$W_{||}$(s) [V/pC]',
            xlim=(min(s*1.0e3), np.amin((np.max(s*1.0e3), np.max(s_cst*1.0e3))))
            )
    ax.legend(loc='best')
    ax.grid(True, color='gray', linewidth=0.2)
    plt.show()

def plot_long_Z(data=read_WAKIS_out(out_path=OUT_PATH), cst_data=read_CST_out(CST_PATH), flag_compare_cst=False, flag_normalize=True):
    # Obtain wakis variables
    Z=data.get('Z')
    freq=data.get('f')

    # Obtain CST variables
    Z_cst=cst_data.get('Z_cst')
    freq_cst=cst_data.get('freq_cst')

    # Plot longitudinal impedance Z||(w) comparison with CST [normalized]
    #---normalizing factor between CST and in numpy.fft
    if flag_normalize:
        norm=max(Z_cst)/max(Z) 
        title='Longitudinal impedance Z||(w) \n [normalized by '+str(round(norm,3))+']'
    else:
        norm=1.0
        title='Longitudinal impedance Z||(w)'

    #--- obtain the maximum frequency for WarpX and plot
    ifmax=np.argmax(Z)
    fig = plt.figure(2, figsize=(6,4), dpi=200, tight_layout=True)
    ax=fig.gca()
    ax.plot(freq[ifmax]*1e-9, Z[ifmax]*norm, marker='o', markersize=4.0, color='blue')
    ax.annotate(str(round(freq[ifmax]*1e-9,2))+ ' GHz', xy=(freq[ifmax]*1e-9,Z[ifmax]*norm), xytext=(-20,5), textcoords='offset points', color='blue') 
    ax.plot(freq*1e-9, Z*norm, lw=1, color='b', marker='s', markersize=2., label='Z||(w)')
    #--- obtain the maximum frequency for CST and plot
    if flag_compare_cst:
        ifmax=np.argmax(Z_cst)
        ax.plot(freq_cst[ifmax]*1e-9, Z_cst[ifmax], marker='o', markersize=5.0, color='red')
        ax.annotate(str(round(freq_cst[ifmax]*1e-9,2))+ ' GHz', xy=(freq_cst[ifmax]*1e-9,Z_cst[ifmax]), xytext=(+20,5), textcoords='offset points', color='red') 
        ax.plot(freq_cst*1.0e-9, Z_cst, lw=1.2, color='red', marker='s', markersize=2., label='Z||(w) from CST')
    #--- plot Z||(s)
    ax.set(title=title,
            xlabel='f [GHz]',
            ylabel='Z||(w) [$\Omega$]',   
            ylim=(0.,np.max(Z_cst)*1.2),
            xlim=(0.,np.max(freq_cst)*1e-9)      
            )
    ax.legend(loc='best')
    ax.grid(True, color='gray', linewidth=0.2)
    plt.show()

def plot_trans_WP(data=read_WAKIS_out(out_path=OUT_PATH), cst_data=read_CST_out(CST_PATH), flag_compare_cst=True):
    # Obtain wakis variables
    WPx=data.get('WPx')
    WPy=data.get('WPy')
    s=data.get('s')
    # Obtain the offset of the source beam and test beam
    xsource=data.get('xsource')
    ysource=data.get('ysource')
    xtest=data.get('xtest')
    ytest=data.get('ytest') 

    # Obtain CST variables
    WPx_cst=cst_data.get('WPx_cst')
    WPy_cst=cst_data.get('WPy_cst')
    s_cst=cst_data.get('s_cst')

    #-- Quadrupolar cases
    if xtest != 0.0 and ytest == 0.0:
        WPx_cst=cst_data.get('WPx_quadrupolarX_cst')
        WPy_cst=cst_data.get('WPy_quadrupolarX_cst')
        s_cst=cst_data.get('s_cst_quadrupolar')
    if xtest == 0.0 and ytest != 0.0:
        WPx_cst=cst_data.get('WPx_quadrupolarY_cst')
        WPy_cst=cst_data.get('WPy_quadrupolarY_cst')
        s_cst=cst_data.get('s_cst_quadrupolar')
    if xtest != 0.0 and ytest != 0.0:
        WPx_cst=cst_data.get('WPx_quadrupolar_cst')
        WPy_cst=cst_data.get('WPy_quadrupolar_cst')
        s_cst=cst_data.get('s_cst_quadrupolar')

    #-- Dipolar cases
    if xsource != 0.0 and ysource == 0.0:
        WPx_cst=cst_data.get('WPx_dipolarX_cst')
        WPy_cst=cst_data.get('WPy_dipolarX_cst')
        s_cst=cst_data.get('s_cst_dipolar')
    if xsource == 0.0 and ysource != 0.0:
        WPx_cst=cst_data.get('WPx_dipolarY_cst')
        WPy_cst=cst_data.get('WPy_dipolarY_cst')
        s_cst=cst_data.get('s_cst_dipolar')
    if xsource != 0.0 and ysource != 0.0:
        WPx_cst=cst_data.get('WPx_dipolar_cst')
        WPy_cst=cst_data.get('WPy_dipolar_cst')
        s_cst=cst_data.get('s_cst_dipolar')

    # Plot transverse wake potential Wx⊥(s), Wy⊥(s) & comparison with CST
    fig = plt.figure(3, figsize=(6,4), dpi=200, tight_layout=True)
    ax=fig.gca()
    ax.plot(s*1.0e3, WPx, lw=1.2, color='g', label='Wx⊥(s)')
    ax.plot(s_cst*1.0e3, WPx_cst, lw=1.2, color='g', ls='--', label='Wx⊥(s) from CST')
    ax.plot(s*1.0e3, WPy, lw=1.2, color='magenta', label='Wy⊥(s)')
    ax.plot(s_cst*1.0e3, WPy_cst, lw=1.2, color='magenta', ls='--', label='Wy⊥(s) from CST')
    ax.set(title='Transverse Wake potential W⊥(s) \n xsource, ysource = '+str(xsource*1e3)+' mm | xtest, ytest = '+str(xtest*1e3)+' mm',
            xlabel='s [mm]',
            ylabel='$W_{⊥}$ [V/pC]',
            xlim=(min(s*1.0e3), np.amin((np.max(s*1.0e3), np.max(s_cst*1.0e3)))),
            )
    ax.legend(loc='best')
    ax.grid(True, color='gray', linewidth=0.2)
    plt.show()

def plot_trans_Z(data=read_WAKIS_out(out_path=OUT_PATH), cst_data=read_CST_out(CST_PATH), flag_compare_cst=True, flag_normalize=True):
    # Obtain wakis variables
    Zx=data.get('Zx')
    Zy=data.get('Zy')
    freqx=data.get('f')
    freqy=data.get('f')

    # Obtain the offset of the source beam and test beam
    xsource=data.get('xsource')
    ysource=data.get('ysource')
    xtest=data.get('xtest')
    ytest=data.get('ytest') 

    # Obtain CST variables
    Zx_cst=cst_data.get('Zx_cst')
    Zy_cst=cst_data.get('Zy_cst')
    freq_cst=cst_data.get('freq_cst')

    #-- Quadrupolar cases
    if xtest != 0.0 and ytest == 0.0:
        Zx_cst=cst_data.get('Zx_quadrupolarX_cst')
        Zy_cst=cst_data.get('Zy_quadrupolarX_cst')
        freq_cst=cst_data.get('freq_cst_quadrupolar')
    if xtest == 0.0 and ytest != 0.0:
        Zx_cst=cst_data.get('Zx_quadrupolarY_cst')
        Zy_cst=cst_data.get('Zy_quadrupolarY_cst')
        freq_cst=cst_data.get('freq_cst_quadrupolar')
    if xtest != 0.0 and ytest != 0.0:
        Zx_cst=cst_data.get('Zx_quadrupolar_cst')
        Zy_cst=cst_data.get('Zy_quadrupolar_cst')
        freq_cst=cst_data.get('freq_cst_quadrupolar')

    #-- Dipolar cases
    if xsource != 0.0 and ysource == 0.0:
        Zx_cst=cst_data.get('Zx_dipolarX_cst')
        Zy_cst=cst_data.get('Zy_dipolarX_cst')
        freq_cst=cst_data.get('freq_cst_dipolar')
    if xsource == 0.0 and ysource != 0.0:
        Zx_cst=cst_data.get('Zx_dipolarY_cst')
        Zy_cst=cst_data.get('Zy_dipolarY_cst')
        freq_cst=cst_data.get('freq_cst_dipolar')
    if xsource != 0.0 and ysource != 0.0:
        Zx_cst=cst_data.get('Zx_dipolar_cst')
        Zy_cst=cst_data.get('Zy_dipolar_cst')
        freq_cst=cst_data.get('freq_cst_dipolar')

    #---normalizing factor between CST and in wakis results
    if flag_normalize:
        norm_x=max(Zx_cst)/max(Zx) 
        norm_y=max(Zy_cst)/max(Zy) 
        title='Transverse impedance Z⊥(w) [normalized by '+str(round(norm_x,3))+']'
    else:
        norm_x=1.0
        norm_y=1.0
        title='Transverse impedance Z⊥(w)'

    #--- obtain the maximum frequency
    ifxmax=np.argmax(Zx)
    ifymax=np.argmax(Zy)
    #--- plot Zx⊥(w)
    fig = plt.figure(4, figsize=(6,4), dpi=200, tight_layout=True)
    ax=fig.gca()
    ax.plot(freqx[ifxmax]*1e-9, Zx[ifxmax]*norm_x, marker='o', markersize=4.0, color='green')
    ax.annotate(str(round(freqx[ifxmax]*1e-9,2))+ ' GHz', xy=(freqx[ifxmax]*1e-9,Zx[ifxmax]), xytext=(-10,5), textcoords='offset points', color='grey') 
    ax.plot(freqx*1e-9, Zx*norm_x, lw=1, color='g', marker='s', markersize=2., label='Zx⊥(w)')
    #--- obtain the maximum frequency for CST Zx⊥(w) and plot
    if flag_compare_cst:
        ifmax=np.argmax(Zx_cst)
        ax.plot(freq_cst[ifmax]*1e-9, Zx_cst[ifmax], marker='o', markersize=5.0, color='black')
        ax.annotate(str(round(freq_cst[ifmax]*1e-9,2))+ ' GHz', xy=(freq_cst[ifmax]*1e-9,Zx_cst[ifmax]), xytext=(+20,5), textcoords='offset points', color='black') 
        ax.plot(freq_cst*1.0e-9, Zx_cst, lw=1.2, ls='--', color='black', marker='s', markersize=2., label='Zx⊥(w) from CST')
    #--- plot Zy⊥(w)
    ax.plot(freqy[ifymax]*1e-9, Zy[ifymax]*norm_y, marker='o', markersize=4.0, color='magenta')
    ax.annotate(str(round(freqy[ifymax]*1e-9,2))+ ' GHz', xy=(freqy[ifymax]*1e-9,Zy[ifymax]), xytext=(-10,5), textcoords='offset points', color='grey') 
    ax.plot(freqy*1e-9, Zy*norm_y, lw=1, color='magenta', marker='s', markersize=2., label='Zy⊥(w)')
    #--- obtain the maximum frequency for CST Zy⊥(w) and plot
    if flag_compare_cst:
        ifmax=np.argmax(Zy_cst)
        ax.plot(freq_cst[ifmax]*1e-9, Zy_cst[ifmax], marker='o', markersize=5.0, color='black')
        ax.annotate(str(round(freq_cst[ifmax]*1e-9,2))+ ' GHz', xy=(freq_cst[ifmax]*1e-9,Zy_cst[ifmax]), xytext=(+20,5), textcoords='offset points', color='black') 
        ax.plot(freq_cst*1.0e-9, Zy_cst, lw=1.2, ls='--', color='black', marker='s', markersize=2., label='Zy⊥(w) from CST')

    ax.set(title=title,
            xlabel='f [GHz]',
            ylabel='Z⊥(w) [$\Omega$]',   
            #ylim=(0.,np.max(Zx_cst)*1.2),
            xlim=(0.,np.max(freq_cst))      
            )
    ax.legend(loc='best')
    ax.grid(True, color='gray', linewidth=0.2)
    plt.show()

def plot_WAKIS(data=read_WAKIS_out(OUT_PATH), cst_data=read_CST_out(CST_PATH), flag_compare_cst=True, flag_normalize=True):
    # Plot results
    plot_long_WP(data=data, cst_data=cst_data, flag_compare_cst=flag_compare_cst)
    plot_long_Z(data=data, cst_data=cst_data, flag_compare_cst=flag_compare_cst, flag_normalize=flag_normalize)
    plot_trans_WP(data=data, cst_data=cst_data, flag_compare_cst=flag_compare_cst)
    plot_trans_Z(data=data, cst_data=cst_data, flag_compare_cst=flag_compare_cst, flag_normalize=flag_normalize)

def subplot_WAKIS(data=read_WAKIS_out(OUT_PATH)):
    #fig = plt.figure(100, figsize=(6,4), dpi=200, tight_layout=True)
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig.suptitle('WAKIS wake solver result')

    # Longitudinal WP
    WP=data.get('WP')
    s=data.get('s')

    ax1.plot(s*1.0e3, WP, lw=1.2, color='orange', label='$W_{||}$(0,0)(s)')
    ax1.set(title='Longitudinal Wake potential $W_{||}$(s)',
            xlabel='s [mm]',
            ylabel='$W_{||}$(s) [V/pC]',
            )
    ax1.legend(loc='best')
    ax1.grid(True, color='gray', linewidth=0.2)

    # Longitudinal Z
    Z=data.get('Z')
    freq=data.get('f')
    ifmax=np.argmax(Z)

    ax2.plot(freq[ifmax]*1e-9, Z[ifmax], marker='o', markersize=4.0, color='blue')
    ax2.annotate(str(round(freq[ifmax]*1e-9,2))+ ' GHz', xy=(freq[ifmax]*1e-9,Z[ifmax]), xytext=(-20,5), textcoords='offset points', color='blue') 
    ax2.plot(freq*1e-9, Z, lw=1, color='b', marker='s', markersize=2., label='Z||(w)')
    ax2.set(title='Longitudinal impedance Z||(w)',
            xlabel='f [GHz]',
            ylabel='Z||(w) [$\Omega$]',   
            ylim=(0.,np.max(Z)*1.2),
            xlim=(0.,np.max(f)*1e-9)      
            )
    ax2.legend(loc='best')
    ax2.grid(True, color='gray', linewidth=0.2)

    # Transverse WP    
    WPx=data.get('WPx')
    WPy=data.get('WPy')
    xsource=data.get('xsource')
    ysource=data.get('ysource')
    xtest=data.get('xtest')
    ytest=data.get('ytest') 

    ax3.plot(s*1.0e3, WPx, lw=1.2, color='g', label='Wx⊥(s)')
    ax3.plot(s*1.0e3, WPy, lw=1.2, color='magenta', label='Wy⊥(s)')
    ax3.set(title='Transverse Wake potential W⊥(s) \n xsource, ysource = '+str(xsource*1e3)+' mm | xtest, ytest = '+str(xtest*1e3)+' mm',
            xlabel='s [mm]',
            ylabel='$W_{⊥}$ [V/pC]',
            )
    ax3.legend(loc='best')
    ax3.grid(True, color='gray', linewidth=0.2)

    # Transverse Z
    Zx=data.get('Zx')
    Zy=data.get('Zy')
    ifxmax=np.argmax(Zx)
    ifymax=np.argmax(Zy)

    #--- plot Zx⊥(w)
    ax4=fig.gca()
    ax4.plot(f[ifxmax]*1e-9, Zx[ifxmax] , marker='o', markersize=4.0, color='green')
    ax4.annotate(str(round(f[ifxmax]*1e-9,2))+ ' GHz', xy=(f[ifxmax]*1e-9,Zx[ifxmax]), xytext=(-10,5), textcoords='offset points', color='g') 
    ax4.plot(f*1e-9, Zx , lw=1, color='g', marker='s', markersize=2., label='Zx⊥(w)')
    #--- plot Zy⊥(w)
    ax4.plot(f[ifymax]*1e-9, Zy[ifymax] , marker='o', markersize=4.0, color='magenta')
    ax4.annotate(str(round(f[ifymax]*1e-9,2))+ ' GHz', xy=(f[ifymax]*1e-9,Zy[ifymax]), xytext=(-10,5), textcoords='offset points', color='m') 
    ax4.plot(f*1e-9, Zy , lw=1, color='magenta', marker='s', markersize=2., label='Zy⊥(w)')
    ax4.set(title='Transverse impedance Z⊥(w)',
            xlabel='f [GHz]',
            ylabel='Z⊥(w) [$\Omega$]',   
            ylim=(0.,np.maximum(max(Zx)*1.2, max(Zy)*1.2)),
            xlim=(0.,np.max(f)*1e-9)      
            )
    ax4.legend(loc='best')
    ax4.grid(True, color='gray', linewidth=0.2)

    plt.show()

if __name__ == "__main__":
    
    out_path=os.getcwd() + '/'+'runs/out'

    data=read_WAKIS_out(out_path)
    
    subplot_WAKIS(data=data)

    plot_WAKIS(data=data, 
                cst_data=read_CST_out(), 
                flag_compare_cst=True, 
                flag_normalize=False
                )