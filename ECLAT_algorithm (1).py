import pandas as pd
import itertools

file_path = 'Horizontal_DataSet.xlsx'  # Dataset path in the same project file directory
df = pd.read_excel(file_path)


# ----------- Convert data to vertical format ----------- #
virtical_data = {}
for index, row in df.iterrows():
    tid = f"T{row['TiD']}"    # Unique Transaction ID by prepending "T" before transaction name
    items_string = row['items']
    items_list = items_string.split(',')

    for item in items_list:
      if item not in virtical_data:
        virtical_data[item] = {tid}   # Add a new item with its first occurence in a transaction
      else:
        virtical_data[item].add(tid)  # Add a transaction to the existing item


# ----------- GENERATING ALL FREQUENT ITEMSETS ----------- #
def my_eclat(data_vert, min_sup):
    freqItemsList = []
    def scan(current_set, candidates):
        for i, (item, tids) in enumerate(candidates):
            new_set = current_set | {item}
            sup_count = len(tids)

            if sup_count >= min_sup:
                freqItemsList.append((frozenset(new_set), sup_count))

                new_cands = []
                for j in range(i + 1, len(candidates)):
                    other_item, other_tids = candidates[j]
                    intersected_tids = tids & other_tids
                    if len(intersected_tids) >= min_sup:
                       new_cands.append((other_item, intersected_tids))

                if new_cands:
                    scan(new_set,new_cands)

    sorted_candidates = sorted(data_vert.items(), key=lambda x: len(x[1]), reverse=True)
    scan(set(), sorted_candidates)
    # Print all freqent itemsets with their support
    for itemset, support in freqItemsList:
        print(f"Items: {set(itemset)}, Support: {support}")

    return freqItemsList


# ----------- Generate Association Rules ----------- #
def genFreqItemSets(frequentItemsList):
    for freqentItemset, support in frequentItemsList:
        if len(freqentItemset) < 2:
            continue
        genAssocRules(list(freqentItemset))
    

def genAssocRules(frequentItemset):
    all_antecedents = []

    def genAntecedents(index, current_antecedent):
        # Base case: if we've considered all items
        if index == len(frequentItemset):
            # Only add non-empty antecedents, and ensure it's not the full itemset
            if current_antecedent and len(current_antecedent) < len(frequentItemset):
                all_antecedents.append(frozenset(current_antecedent))
            return

        # Exclude the current item
        genAntecedents(index + 1, current_antecedent)
        # Include the current item
        genAntecedents(index + 1, current_antecedent + [frequentItemset[index]])

    genAntecedents(0, [])

    # For each generated antecedent, determine the corresponding consequent and print the rule
    for ant in all_antecedents:
        cons = frozenset(frequentItemset) - ant
        print(f"{set(ant)} -> {set(cons)}")

# ----------- Items Lift ----------- #
def itemsLift(freqsets):
    num_transactions = len(df)
    support_dict = {frozenset(itemset): support for itemset, support in freqsets}

    for i, (itemset, support) in enumerate(freqsets):
        if len(itemset) < 2:
            lift = None
        else:
            prod_support = 1
            for elem in itemset:
                elem_support = support_dict[frozenset([elem])] / num_transactions
                prod_support *= elem_support

            support_itemset = support_dict[frozenset(itemset)] / num_transactions
            lift = support_itemset / prod_support

        freqsets[i] = (itemset, support, lift)

    for itemset, support, lift in freqsets:
        print(f"Items: {set(itemset)}, Support: {support}, Lift: {lift}")


# ----------- Generate Strong Rules ----------- #
def get_rules(frequent_sets, vertical_db, min_confidence):
    strong_rules = []

    for itemset, support_together in frequent_sets:
        if len(itemset) < 2:
            continue

        for size in range(1, len(itemset)):
            for combo in itertools.combinations(itemset, size):
                before = frozenset(combo)
                after = itemset - before

                support_before = len(set.intersection(*(vertical_db[item] for item in before)))

                if support_before == 0:
                    continue

                confidence = support_together / support_before

                if confidence >= min_confidence:
                    strong_rules.append((before, after, confidence))

    return strong_rules


# ----------- Run using diff. support and conf. values ----------- #
minSupport = int(input("\n  Enter min. support: "))
minConfidence = float(input("  Enter min. confidence: "))

print("\n\n=========== All Frequent Itemsets & their Support ===========")
frequnt_items_list = my_eclat(virtical_data, minSupport)


print("\n\n=========== Association Rules ===========")
genFreqItemSets(frequnt_items_list)

print("\n\n=========== Strong Rules ===========")
strongRules = get_rules(frequnt_items_list, virtical_data, minConfidence)
for before, after, conf in strongRules:
    print(f"{set(before)} -> {set(after)} , cofidence = {conf}")

print("\n\n=========== Items Lift ===========")
itemsLift(frequnt_items_list)