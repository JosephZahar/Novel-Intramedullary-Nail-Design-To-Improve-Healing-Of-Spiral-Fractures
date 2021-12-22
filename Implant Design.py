import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import seaborn as sns

Implant_df = pd.read_excel(r'/Users/macbookpro/Desktop/Implant Design Lab results.xlsx')
Specimens = [' 1', ' 2', ' 3', ' 4', ' 5']
Specimens_name = ['7.5 pcf', '12.5 pcf', '12.5 pcf + 2 mm layer', '20 pcf + 3 mm layer', '20 pcf + 2 mm layer']
fonttype = {'fontname': 'Times New Roman'}
def cw1plots(data, x1, y1, Specimens, png):
    fig = plt.figure(figsize=([8, 5]))
    with plt.style.context('fast'):
        ax1 = plt.axes()
        [ax1.plot(data[x1 + Specimen] * 100, data[y1 + Specimen], marker='o', markersize=0.5, linestyle='None') for
         Specimen in Specimens]
        plt.rcParams['figure.dpi'] = 360
        ax1.set_ylabel(y1 + ' (MPa)', fontsize=13, **fonttype)
        ax1.set_xlabel(x1 + ' (%)', fontsize=13, **fonttype)
        ax1.legend(Specimens_name, prop={"size": 12,"family": 'Times New Roman'})
        for tick in ax1.get_xticklabels():
            tick.set_fontname("Times New Roman")
        for tick in ax1.get_yticklabels():
            tick.set_fontname("Times New Roman")
        plt.savefig(png + '.png', dpi=1000)


def Tangent_Modulus(data, Specimen):
    Tangent_modulus = (
            (data.loc[data['Tensile strain' + Specimen] >= 0.045].head(1)['Tensile stress' + Specimen].item() -
             data.loc[data['Tensile strain' + Specimen] >= 0.035].head(1)[
                 'Tensile stress' + Specimen].item()) / (0.045 - 0.035))
    return Tangent_modulus


def Peak_Stress(data, Specimen):
    Peak_stress = data['Tensile stress' + Specimen].max()
    return Peak_stress


def Peak_Strain(data, Specimen):
    Peak_strain = (data.loc[data['Tensile stress' + Specimen] == Peak_Stress(data, Specimen)].head(1)[
                       'Tensile strain' + Specimen].item())
    return Peak_strain

def Max_Time(data, Specimen):
    Max_time = data['Time' + Specimen].max()
    return Max_time

def Instantaneous_modulus(data, Specimen):
    Instantaneous_modulus = Peak_Stress(data,Specimen)/Peak_Strain(data,Specimen)
    return Instantaneous_modulus


def Relaxation_Modulus(data, Specimen):
    Relaxation_modulus = ((data.loc[data['Time' + Specimen] == Max_Time(data, Specimen)].head(1)[
                       'Tensile stress' + Specimen].item()) /
                              (data.loc[data['Time' + Specimen] == Max_Time(data, Specimen)].head(1)[
                                   'Tensile strain' + Specimen].item()))
    return Relaxation_modulus


def Time_Constant(data, Specimen):
    S1 = data.loc[data['Time' + Specimen] == Max_Time(data, Specimen)].head(1)[
                       'Tensile stress' + Specimen].item()
    S0 = data.loc[data['Time' + Specimen] == 0].head(1)['Tensile stress' + Specimen].item()
    Stress_tau = (S0 - S1) * math.exp(-1) + S1
    Time_constant = (data.loc[data['Tensile stress' + Specimen] <= Stress_tau].head(1)['Time' + Specimen].item())
    return Time_constant


def Percentage_Relaxation(data, Specimen):
    S1 = data.loc[data['Time' + Specimen] == Max_Time(data, Specimen)].head(1)[
                       'Tensile stress' + Specimen].item()
    S0 = data.loc[data['Time' + Specimen] == 0].head(1)['Tensile stress' + Specimen].item()
    Percentage_relaxation = ((S0 - S1) / S0) * 100
    return Percentage_relaxation


def cw1mean(data1, data2, y1, y2, Specimens1, Specimens2, png):
    with plt.style.context('seaborn-bright'):
        fig = plt.figure(figsize=([7, 4]))
        ax = fig.add_subplot(121)
        Incubated = [y1(data1, Specimen) for Specimen in Specimens1[0:3]]
        Fresh = [y1(data1, Specimen) for Specimen in Specimens1[3:6]]
        for i in range(3):
            ax.scatter(['Incubated Samples'], Incubated[i], color = 'grey')
        for x in range(3):
            ax.scatter(['Fresh Samples'], Fresh[x], color = 'grey')
        x = ['Incubated Samples', 'Fresh Samples']
        x_pos = [i for i, _ in enumerate(x)]
        patterns = ("",'/////')
        bars = ax.bar(x_pos, [np.mean(Incubated), np.mean(Fresh)], data=data1,
               yerr=[np.std(Incubated), np.std(Fresh)], color=["darkgrey",'w'], edgecolor='black', alpha = 0.5 ,  capsize=2, width=0.4)
        for i, x in zip(bars, patterns):
            i.set_hatch(x)
        ax.set_ylabel('Tangent Modulus (MPa)', fontsize=12, **fonttype)
        ax.set_xlabel('')
        for tick in ax.get_xticklabels():
            tick.set_fontname("Times New Roman")
        for tick in ax.get_yticklabels():
            tick.set_fontname("Times New Roman")
        sns.despine()
        plt.tight_layout(pad=3)

        ax = fig.add_subplot(122)
        Incubated = [y2(data2, Specimen) for Specimen in Specimens2[0:3]]
        Fresh = [y2(data2, Specimen) for Specimen in Specimens2[3:6]]
        x = ['Incubated Samples', 'Fresh Samples']
        x_pos = [i for i, _ in enumerate(x)]
        patterns = ("", '///// ')
        bars = ax.bar(x_pos, [np.mean(Incubated), np.mean(Fresh)], data=data1,
                      yerr=[np.std(Incubated), np.std(Fresh)], color=["darkgrey", 'w'], edgecolor='black', alpha=0.5,
                      capsize=2, width=0.4)
        for i, x in zip(bars, patterns):
            i.set_hatch(x)
        for i in range(3):
            ax.scatter(['Incubated Samples'], Incubated[i], color = 'grey')
        for x in range(3):
            ax.scatter(['Fresh Samples'], Fresh[x], color = 'grey')
        ax.set_ylabel('Ultimate Tensile Strength (MPa)', fontsize=12, **fonttype)
        ax.set_xlabel('')
        for tick in ax.get_xticklabels():
            tick.set_fontname("Times New Roman")
        for tick in ax.get_yticklabels():
            tick.set_fontname("Times New Roman")
        sns.despine()
        plt.tight_layout(pad=3)
        plt.savefig(png + '.png')

#cw1bargraphs(stress_relaxation, Relaxation_Modulus, Specimens2, 'Relaxation Modulus (MPa)')
cw1plots(Implant_df, 'Tensile strain (Extension)', 'Tensile stress', Specimens, 'Implant_df')
#cw1mean(test_to_failure, test_to_failure, Tangent_Modulus, Peak_Stress, Specimens , Specimens, 'Bargraph')