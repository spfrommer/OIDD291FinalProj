from model import Rule, World

def read_csv(file):
    with open(file) as f:
        csv = f.read()
        data = []
        for line in csv.splitlines():
            data.append(line.split(","))
        # Remove header line
        data.pop(0)
        return data

def read_rules(file):
    SEC_COL = 0
    YEAR_COL = 1
    COMM_COL = 2
    TOT_COL = 3
    F2F_COL = 4
    YR_CNT_COL = 5

    csv = read_csv(file)
    rules = []

    cur_rule = Rule(csv[0][SEC_COL])
    
    for row in csv:
        sec_id = row[SEC_COL]
        if not (sec_id == cur_rule.sec_id):
            rules.append(cur_rule)
            cur_rule = Rule(sec_id)
        
        cur_rule.append_year(bool(row[COMM_COL]),
                             bool(row[F2F_COL]),
                             bool(row[TOT_COL]))
    
    rules.append(cur_rule)
    return rules

def read_worlds(file):
    GRP_COL = 0
    SEC_COL = 1
    WORLD_COL = 2
    YEAR_COL = 3
    ALBA_COL = 4
    BATIA_COL = 5
    CAPITA_COL = 6
    DELTA_COL = 7
    TOTAL_COL = 8
    PRICE_COL = 9
    PROFIT_COL = 10

    csv = read_csv(file)
    worlds = []

    cur_world = World(csv[0][GRP_COL], csv[0][SEC_COL], int(csv[0][WORLD_COL]))

    for row in csv:
        sec_id = row[SEC_COL]
        world_id = int(row[WORLD_COL])
        if not (sec_id == cur_world.sec_id and
                world_id == cur_world.world_id):
            worlds.append(cur_world)
            cur_world = World(row[GRP_COL], sec_id, world_id)

        cur_world.append_year(float(row[ALBA_COL]),
                              float(row[BATIA_COL]),
                              float(row[CAPITA_COL]))
    
    worlds.append(cur_world)
    return worlds


rules = read_rules("data/opeq_params.csv")
worlds = read_worlds("data/opeq.csv")

def get_rule(world):
    for rule in rules:
        if rule.sec_id == world.sec_id:
            return rule
    return None
