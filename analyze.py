import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

from model import Rule, World
import data
import process

matplotlib.rcParams['figure.dpi'] = 200

def defection_areachart(worlds):
    defection = process.defection_metric()
    all_defection = [];
   
    endRound = 12
    for world in worlds:
        all_defection.append(defection(world)[0:endRound])

    rounds = range(1,endRound+1)
     
    # Basic stacked area chart.
    plt.stackplot(rounds, all_defection)
    #plt.legend(loc = 'upper left')
    
    plt.xlabel('Rounds')
    plt.ylabel('Defection')
    plt.show()
#defection_areachart(data.worlds)

def defection_histogram(worlds):
    defection = map(process.cum_defection_metric(), data.worlds)

    N_points = 100000
    n_bins = 20

    plt.hist(defection, bins=20)
    plt.show()

def communication_barchart(worlds):
    metric = process.communication_metric(ignore_last=True)
    bars1 = [metric(world)["c2c_def"] for world in worlds]
    bars2 = [metric(world)["n2n_def"] for world in worlds]
    bars3 = [metric(world)["n2c_def"] for world in worlds]
    bars4 = [metric(world)["c2n_def"] for world in worlds]
    # set width of bar
    barWidth = 0.25
     
    # Set position of bar on X axis
    r1 = np.arange(len(bars1))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    r4 = [x + barWidth for x in r3]
     
    # Make the plot
    plt.bar(r1, bars1, color='#7f6d5f', width=barWidth, edgecolor='white', label='c2c_def')
    plt.bar(r2, bars2, color='#557f2d', width=barWidth, edgecolor='white', label='n2n_def')
    plt.bar(r3, bars3, color='#2d7f5e', width=barWidth, edgecolor='white', label='n2c_def')
    plt.bar(r4, bars4, color='#444444', width=barWidth, edgecolor='white', label='c2n_def')
     
    # Add xticks on the middle of the group bars
    plt.xlabel('group', fontweight='bold')
    #plt.xticks([r + barWidth for r in range(len(bars1))], ['A', 'B', 'C', 'D', 'E'])
     
    # Create legend & Show graphic
    plt.legend()
    plt.show()

def plot_barchart(bar_heights, bar_labels, group_labels=None):
    # set width of bar
    bar_width = 0.23
     
    # Set position of bar on X axis
    bar_xs = [np.arange(len(bar_heights[0]))]
    for i in range(len(bar_heights) - 1):
        bar_xs.append([x + bar_width for x in bar_xs[-1]])

    colors = ['#bdd7e7','#6baed6','#3182bd','#08519c'] 
    for xs,heights,label,color in zip(bar_xs, bar_heights, bar_labels, colors):
        plt.bar(xs, heights, color=color, width=bar_width, edgecolor="white", label=label)
    
    # Add xticks on the middle of the group bars
    plt.xlabel('group', fontweight='bold')
    if group_labels != None:
        plt.xticks([r + bar_width for r in range(len(bar_heights[0]))], group_labels)
     
    # Create legend & Show graphic
    plt.legend()
    plt.show()
    
student_groups = ["schaumberg-2018", "yip-2017",
                  "yip-2015", "schweitzer-2016",
                  "schweitzer-2017", "schweitzer-2015",
                  "massey-2016", "massey-2017",
                  "azevedo-2017"]

def grouped_communication_barchart(worlds):
    bars = [[],[],[],[]]
    for student_group in student_groups:
        selector = process.student_group_selector(student_group)
        group_worlds = process.apply_selectors(worlds, [selector])
        
        metric = process.communication_metric(ignore_last=True)
        comms = process.apply_metric(group_worlds, metric, include_world=False)
        comm_avg = process.average_metric(comms)
        bars[0].append(comm_avg["c2c_def"])
        bars[1].append(comm_avg["c2n_def"])
        bars[2].append(comm_avg["n2c_def"])
        bars[3].append(comm_avg["n2n_def"])
    
    plot_barchart(bars, ["c2c_def", "c2n_def", "n2c_def", "n2n_def"], student_groups)

def lin_fit(xs, ys):
    xs = np.asarray(xs)
    xs = xs.reshape(-1, 1)
    regr = linear_model.LinearRegression()
    regr.fit(xs, ys)
    y_pred = regr.predict(xs)
    print regr.score(xs, ys)

    return y_pred

def communication_scatterplot(worlds):
    f = plt.figure()
    #f.gca().set_xticks(np.arange(-20, 70, 10))
    #f.gca().set_yticks(np.arange(-70, 60, 10))
    f.gca().set_axisbelow(True)
    f.gca().axis("equal")
    plt.grid()

    metric = process.communication_metric(ignore_first=False, ignore_last=True)
    #colors = ['#543005','#8c510a','#bf812d','#dfc27d','#f6e8c3',
              #'#c7eae5','#80cdc1','#35978f','#01665e','#003c30']
    colors = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00',
              '#ffff33','#a65628','#f781bf','#999999'] 

    all_c2ns = []
    all_n2cs = []

    for i, student_group in enumerate(student_groups):
        selector = process.student_group_selector(student_group)
        group_worlds = process.apply_selectors(worlds, [selector])

        comms = process.apply_metric(group_worlds, metric, include_world=False)
        c2ns = map(lambda c: c["c2n_def"], comms)
        n2cs = map(lambda c: c["n2c_def"], comms)

        all_c2ns = all_c2ns + c2ns
        all_n2cs = all_n2cs + n2cs

        plt.scatter(c2ns, n2cs, s=100, c=colors[i], label=student_group)

    plt.plot(all_c2ns, lin_fit(all_c2ns, all_n2cs),
             color='blue', linewidth=3)
            
    plt.xlabel('c2n')
    plt.ylabel('n2c')
    plt.legend()
    f.show()


#selectors = [process.round_rule_selector("comm", [2]),
#             process.round_rule_selector("comm", [1], include=False)]
selectors = [process.round_rule_selector("comm", [1,2]),
             process.round_rule_selector("comm", [3], include=False),
             process.sec_id_selector("Schaumberg-2018a_oidd291", include=False)]

#selectors = [process.sec_id_selector("Azevedo-2017a_bepp250002_nocomm")]
#selectors = [process.sec_id_selector("Schaumberg-2018a_oidd291"),
             #process.world_id_selector(8)]
selectors = [process.sec_id_selector("Schaumberg-2018a_oidd291", include=False)]

metric = process.communication_metric(ignore_last=True)

filt = process.apply_selectors(data.worlds, selectors)
print(len(data.worlds))
print(len(filt))

#grouped_communication_barchart(data.worlds)
communication_scatterplot(data.worlds)
#defection_areachart(process.apply_selectors(data.worlds, selectors))
#defection_histogram(data.worlds)
raw_input()
