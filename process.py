from model import Rule, World
import math
import data

def defection_metric():
    def metric(world):
        optimal = 38.9
        alba_def = [max(prod - optimal, 0) for prod in world.alba]
        batia_def = [max(prod - optimal, 0) for prod in world.batia]
        capita_def = [max(prod - optimal, 0) for prod in world.capita]

        tot_def = [(a+b+c)/3 for a,b,c in zip(alba_def, batia_def, capita_def)]
        return { "def": tot_def }
    return metric

def disc_defection_metric():
    def metric(world):
        optimal = 38.9
        alba_def = [max(prod - optimal, 0) for prod in world.alba]
        batia_def = [max(prod - optimal, 0) for prod in world.batia]
        capita_def = [max(prod - optimal, 0) for prod in world.capita]
        
        def_cnt = [(a>8) + (b>8) + (c>8) for a,b,c in zip(alba_def, batia_def, capita_def)]
        return { "def": def_cnt }
    return metric

def communication_metric(def_metric, ignore_first=False, ignore_last=False):
    def metric(world):
        defection = (def_metric)(world)["def"]
        rule = data.get_rule(world)

        c2c_sum = 0
        c2c_cnt = 0
        c2n_sum = 0
        c2n_cnt = 0
        n2c_sum = 0
        n2c_cnt = 0
        n2n_sum = 0
        n2n_cnt = 0

        for i in range(1 + int(ignore_first),
                       world.year_cnt() - int(ignore_last)):
            def_delta = defection[i] - defection[i-1]
            comm_before = rule.comm[i-1] or rule.f2f[i-1]
            comm_after = rule.comm[i] or rule.f2f[i]
            if comm_before and comm_after:
                c2c_sum += def_delta
                c2c_cnt += 1
            if comm_before and (not comm_after):
                c2n_sum += def_delta
                c2n_cnt += 1
            if (not comm_before) and comm_after:
                n2c_sum += def_delta
                n2c_cnt += 1
            if (not comm_before) and (not comm_after):
                n2n_sum += def_delta
                n2n_cnt += 1

        def smart_div(num, den):
            if num == 0: return 0
            return num / den
        
        return { "c2c_def": smart_div(c2c_sum, c2c_cnt),
                 "c2n_def": smart_div(c2n_sum, c2n_cnt), 
                 "n2c_def": smart_div(n2c_sum, n2c_cnt), 
                 "n2n_def": smart_div(n2n_sum, n2n_cnt) }
    return metric

def nphat_metric(ignore_first=False, ignore_last=False):
    def metric(world):
        defection = (defection_metric())(world)["def"]
        rule = data.get_rule(world)

        c2n_sum = 0
        c2n_cnt = 0
        n2c_sum = 0
        n2c_cnt = 0

        def smart_div(num, den):
            if num == 0: return 0
            return num / den

        for i in range(1 + int(ignore_first),
                       world.year_cnt() - int(ignore_last)):
            def_delta = defection[i] - defection[i-1]

            comm_before = rule.comm[i-1] or rule.f2f[i-1]
            comm_after = rule.comm[i] or rule.f2f[i]
            if comm_before and (not comm_after) and def_delta > 0:
                c2n_sum += smart_div(def_delta, (75-38.9) - defection[i-1])
                c2n_cnt += 1
            if (not comm_before) and comm_after and def_delta < 0:
                n2c_sum += smart_div(-def_delta, defection[i-1])
                n2c_cnt += 1

        return { "nhat": smart_div(c2n_sum, c2n_cnt),
                 "phat": smart_div(n2c_sum, n2c_cnt) }
    return metric

def cum_defection_metric():
    def metric(world):
        return sum((defection_metric())(world)["def"])
    return metric

def apply_metric(worlds, metric, include_world=True):
    results = []
    for world in worlds:
        if include_world:
            results.append((world, metric(world)))
        else:
            results.append(metric(world))
    return results

def average_metric(metrics):
    N = float(len(metrics)) 
    return { k : sum(m[k] for m in metrics)/N for k in metrics[0] } 

# Selectors
# Returns worlds that are overall collaborative
def collaborative_selector():
    def selector(world):
        return sum(defection(world)) <= 80

    return selector

# Selects a world if it has a certain rule in the given rounds
def round_rule_selector(rule, rounds, include=True):
    def selector(world):
        rule_vec = getattr(data.get_rule(world), rule)
        for r in rounds:
            if include and not rule_vec[r]:
                return False
            if not include and rule_vec[r]:
                return False
        return True

    return selector

def student_group_selector(student_group, include=True):
    def selector(world):
        if include:
            return world.student_group == student_group 
        else:
            return world.student_group != student_group 

    return selector

def sec_id_selector(sec_id, include=True):
    def selector(world):
        if include:
            return world.sec_id == sec_id
        else:
            return world.sec_id != sec_id
    return selector

def world_id_selector(world_id, include=True):
    def selector(world):
        if include:
            return world.world_id == world_id
        else:
            return world.world_id != world_id
    return selector

def apply_selectors(worlds, selectors):
    worlds = list(worlds)
    for selector in selectors:
        worlds = filter(selector, worlds)
    return worlds
