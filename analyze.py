import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

from model import Rule, World
import data
import process
import theory

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
        
        metric = process.communication_metric(process.defection_metric(),
                                              ignore_last=True)
        comms = process.apply_metric(group_worlds, metric, include_world=False)
        comm_avg = process.average_metric(comms)
        bars[0].append(comm_avg["c2c_def"])
        bars[1].append(comm_avg["c2n_def"])
        bars[2].append(comm_avg["n2c_def"])
        bars[3].append(comm_avg["n2n_def"])
    
    plot_barchart(bars, ["c2c_def", "c2n_def", "n2c_def", "n2n_def"], student_groups)

def communication_scatterplot(worlds):
    f = plt.figure(figsize=(9, 12))
    ax = f.gca()
    ax.set_axisbelow(True)
    ax.axis("equal")
    ax.spines["top"].set_visible(False)    
    ax.spines["bottom"].set_visible(False)    
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(False)   
    ax.get_xaxis().tick_bottom()    
    ax.get_yaxis().tick_left()
    plt.grid()
    f.patch.set_facecolor('white')

    metric = process.communication_metric(process.defection_metric(),
                                ignore_first=False, ignore_last=True)
    colors = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00',
              '#ffff33','#a65628','#f781bf','#999999'] 

    for i, student_group in enumerate(student_groups):
        selector = process.student_group_selector(student_group)
        group_worlds = process.apply_selectors(worlds, [selector])

        comms = process.apply_metric(group_worlds, metric, include_world=False)
        xs = map(lambda c: c["c2n_def"], comms)
        ys = map(lambda c: c["n2c_def"], comms)

        plt.scatter(xs, ys, s=100, c=colors[i], label=student_group)
    
    #plt.xlabel("Defection Change when Maintaining Communication (Avg. Barrels of Oil)")
    #plt.ylabel("Defection Change on Multi-Round No Communication (Avg. Barrels of Oil)")
    plt.xlabel("Defection Change when Losing Communication (Avg. Barrels of Oil)")
    plt.ylabel("Defection Change when Gaining Communication (Avg. Barrels of Oil)")
    plt.legend()
    f.show()

def nphat_heatmap(worlds):
    f = plt.figure(figsize=(9, 9))
    ax = f.gca()
    ax.set_axisbelow(True)
    ax.axis("equal")
    ax.spines["top"].set_visible(False)    
    ax.spines["bottom"].set_visible(False)    
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(False)   
    ax.get_xaxis().tick_bottom()    
    ax.get_yaxis().tick_left()
    plt.grid()
    f.patch.set_facecolor('white')

    colors = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00',
              '#ffff33','#a65628','#f781bf','#999999'] 
    strats = [theory.trigger_payoff, theory.sneaky_payoff,
              theory.defect_payoff]
    
    min_payoff = 1000000
    max_payoff = 0
    res = 0.05
    size = 1.0

    for phat in np.nditer(np.arange(0.0, size, res)):
        for nhat in np.nditer(np.arange(0.0, size, res)):
            payoffs = [strat(phat, nhat) for strat in strats]
            payoff = max(payoffs)
            if payoff < min_payoff:
                min_payoff = payoff
            if payoff > max_payoff:
                max_payoff = payoff
    min_payoff -= 300

    for phat in np.nditer(np.arange(0.0, size, res)):
        for nhat in np.nditer(np.arange(0.0, size, res)):
            payoffs = [strat(phat, nhat) for strat in strats]
            payoff = max(payoffs)
            index = payoffs.index(payoff)
            
            rect = patches.Rectangle((phat,nhat), res, res,
                                      alpha=(payoff - min_payoff)/(max_payoff - min_payoff),
                                      facecolor=colors[index], zorder=1)
            ax.add_patch(rect)

    metric = process.nphat_metric(ignore_first=False, ignore_last=True)
    for i, student_group in enumerate(student_groups):
        selector = process.student_group_selector(student_group)
        group_worlds = process.apply_selectors(worlds, [selector])

        comms = process.apply_metric(group_worlds, metric, include_world=False)
        xs = map(lambda c: c["phat"], comms)
        ys = map(lambda c: c["nhat"], comms)
    
        plt.scatter(np.mean(xs), np.mean(ys), s=50, c='black', label=student_group, zorder=10)
        plt.text(np.mean(xs), np.mean(ys)+0.02, student_group, horizontalalignment='center', weight='bold')
        #ax.annotate(student_group, xy=(np.mean(xs), np.mean(ys)), xytext=(np.mean(xs), np.mean(ys)+0.01))
    
    plt.xlabel("phat")
    plt.ylabel("nhat")

    rects = [patches.Rectangle((0, 0), res, res, 1, facecolor=colors[0], zorder=0),
             patches.Rectangle((0, 0), res, res, 1, facecolor=colors[1], zorder=0), 
             patches.Rectangle((0, 0), res, res, 1, facecolor=colors[2], zorder=0)]
    plt.legend(rects, ["Trigger", "Sneaky", "Defect"])
    ax.set_xlim(xmin=0, xmax=size)
    ax.set_ylim(ymin=0, ymax=size)
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

filt = process.apply_selectors(data.worlds, selectors)
print(len(data.worlds))
print(len(filt))

#grouped_communication_barchart(data.worlds)
communication_scatterplot(data.worlds)
#nphat_heatmap(data.worlds)
#defection_areachart(process.apply_selectors(data.worlds, selectors))
#defection_histogram(data.worlds)
raw_input()
