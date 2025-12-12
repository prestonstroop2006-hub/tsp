import itertools
import time

# Attracties data
attracties = {
    'A0': {'wacht': 0, 'behoefte': 0, 'indoor': 1, 'kinderen': 0},
    'A1': {'wacht': 60, 'behoefte': 20, 'indoor': 0, 'kinderen': 1},
    'A2': {'wacht': 10, 'behoefte': 3, 'indoor': 1, 'kinderen': 9},
    'A3': {'wacht': 45, 'behoefte': 15, 'indoor': 0, 'kinderen': 2},
    'A4': {'wacht': 5, 'behoefte': 18, 'indoor': 0, 'kinderen': 10},
    'A5': {'wacht': 25, 'behoefte': 4, 'indoor': 1, 'kinderen': 7},
    'A6': {'wacht': 12, 'behoefte': 10, 'indoor': 0, 'kinderen': 0},
    'A7': {'wacht': 30, 'behoefte': 8, 'indoor': 1, 'kinderen': 5},
    'A8': {'wacht': 8, 'behoefte': 1, 'indoor': 0, 'kinderen': 3},
    'A9': {'wacht': 55, 'behoefte': 12, 'indoor': 0, 'kinderen': 1},
    'A10': {'wacht': 3, 'behoefte': 6, 'indoor': 0, 'kinderen': 8}
}

# Reistijden 
reistijden = {
    ('A0','A1'): (7,1.10), ('A0','A2'): (11,1.25), ('A0','A3'): (9,0.95),
    ('A0','A4'): (6,1.05), ('A0','A5'): (14,1.30), ('A0','A6'): (8,1.15),
    ('A0','A7'): (12,1.00), ('A0','A8'): (5,1.20), ('A0','A9'): (10,0.90),
    ('A0','A10'): (13,1.35),
    
    # Terug naar A0
    ('A1','A0'): (6,1.15), ('A2','A0'): (10,1.05), ('A3','A0'): (8,0.85),
    ('A4','A0'): (7,1.20), ('A5','A0'): (15,1.30), ('A6','A0'): (9,1.25),
    ('A7','A0'): (11,1.00), ('A8','A0'): (5,1.25), ('A9','A0'): (12,0.95),
    ('A10','A0'): (14,1.10),
    
    # Voor Sample A routes
    ('A2','A3'): (5,1.25), ('A3','A4'): (9,1.05), ('A4','A7'): (9,1.25),
    ('A7','A10'): (8,1.00), ('A10','A2'): (12,1.25), ('A3','A2'): (4,1.10),
    ('A4','A3'): (6,1.30), ('A7','A4'): (9,1.15), ('A10','A7'): (10,1.00),
}

# Gewichten
school = {'cong': 1.0, 'wacht': 0.5, 'behoefte': 1.5, 'indoor': 1.0, 'kinderen': 2.0}
ochtend = {'cong': 1.2, 'wacht': 1.5, 'behoefte': 0.2, 'indoor': 0.1, 'kinderen': 0.0}

# Kosten functie
def bereken_kosten(route, scenario):
    if scenario == 'school':
        g = school
    else:
        g = ochtend
    
    totaal = 0
    for i in range(len(route) - 1):
        van = route[i]
        naar = route[i + 1]
        
        if (van, naar) in reistijden:
            tijd, cong = reistijden[(van, naar)]
        else:
            tijd, cong = 10, 1.0
        
        totaal += tijd * cong * g['cong']
        
        if naar != 'A0':
            attr = attracties[naar]
            totaal += attr['wacht'] * g['wacht']
            totaal -= attr['behoefte'] * g['behoefte']
            totaal -= attr['indoor'] * g['indoor']
            totaal -= attr['kinderen'] * g['kinderen']
    
    return round(totaal, 2)

# Brute Force
def brute_force(attracties_lijst, scenario):
    andere = [a for a in attracties_lijst if a != 'A0']
    beste_route = None
    beste_kosten = 999999
    
    start = time.time()
    
    for perm in itertools.permutations(andere):
        route = ['A0'] + list(perm) + ['A0']
        k = bereken_kosten(route, scenario)
        if k < beste_kosten:
            beste_kosten = k
            beste_route = route
    
    tijd = (time.time() - start) * 1000
    return beste_route, beste_kosten, int(tijd)

# Nearest Neighbour
def nearest_neighbour(attracties_lijst, scenario):
    onbezocht = [a for a in attracties_lijst if a != 'A0']
    route = ['A0']
    huidig = 'A0'
    
    start = time.time()
    
    while onbezocht:
        volgende = None
        min_tijd = 9999
        
        for a in onbezocht:
            if (huidig, a) in reistijden:
                tijd, _ = reistijden[(huidig, a)]
                if tijd < min_tijd:
                    min_tijd = tijd
                    volgende = a
        
        if volgende is None:
            volgende = onbezocht[0]
        
        route.append(volgende)
        onbezocht.remove(volgende)
        huidig = volgende
    
    route.append('A0')
    k = bereken_kosten(route, scenario)
    
    tijd = (time.time() - start) * 1000
    return route, k, int(tijd)

# 2 Opt
def twee_opt(route, scenario):
    beste_route = route[:]
    beste_kosten = bereken_kosten(route, scenario)
    
    start = time.time()
    
    verbetering = True
    while verbetering:
        verbetering = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route) - 1):
                nieuwe = route[:]
                nieuwe[i:j+1] = reversed(nieuwe[i:j+1])
                nieuwe_kosten = bereken_kosten(nieuwe, scenario)
                if nieuwe_kosten < beste_kosten:
                    beste_route = nieuwe
                    beste_kosten = nieuwe_kosten
                    verbetering = True
    
    tijd = (time.time() - start) * 1000
    return beste_route, beste_kosten, int(tijd)

# Sample A
print("SAMPLE A (5 attracties):")

print("1. SCHOOLREISJE:")
bf1_route, bf1_kosten, bf1_tijd = brute_force(['A0', 'A2', 'A3', 'A4', 'A7', 'A10'], 'school')
nn1_route, nn1_kosten, nn1_tijd = nearest_neighbour(['A0', 'A2', 'A3', 'A4', 'A7', 'A10'], 'school')
opt1_route, opt1_kosten, opt1_tijd = twee_opt(nn1_route, 'school')

print(f"Brute Force: {bf1_kosten} ({bf1_tijd}ms)")
print(f"Nearest Neighbour: {nn1_kosten} ({nn1_tijd}ms)")
print(f"2-opt: {opt1_kosten} ({opt1_tijd}ms)")

print("2. OCHTENDRUSH:")
bf2_route, bf2_kosten, bf2_tijd = brute_force(['A0', 'A2', 'A3', 'A4', 'A7', 'A10'], 'ochtend')
nn2_route, nn2_kosten, nn2_tijd = nearest_neighbour(['A0', 'A2', 'A3', 'A4', 'A7', 'A10'], 'ochtend')
opt2_route, opt2_kosten, opt2_tijd = twee_opt(nn2_route, 'ochtend')

print(f"Brute Force: {bf2_kosten} ({bf2_tijd}ms)")
print(f"Nearest Neighbour: {nn2_kosten} ({nn2_tijd}ms)")
print(f"2-opt: {opt2_kosten} ({opt2_tijd}ms)")

# Sample B
print("SAMPLE B (10 attracties):")

print("1. SCHOOLREISJE:")
nnb1_route, nnb1_kosten, nnb1_tijd = nearest_neighbour(['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10'], 'school')
optb1_route, optb1_kosten, optb1_tijd = twee_opt(nnb1_route, 'school')

print(f"Nearest Neighbour: {nnb1_kosten} ({nnb1_tijd}ms)")
print(f"2-opt: {optb1_kosten} ({optb1_tijd}ms)")

print("2. OCHTENDRUSH:")
nnb2_route, nnb2_kosten, nnb2_tijd = nearest_neighbour(['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10'], 'ochtend')
optb2_route, optb2_kosten, optb2_tijd = twee_opt(nnb2_route, 'ochtend')

print(f"Nearest Neighbour: {nnb2_kosten} ({nnb2_tijd}ms)")
print(f"2-opt: {optb2_kosten} ({optb2_tijd}ms)")