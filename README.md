# ECLAT Algorithm Implementation (Mining technique)

This repository contains a Python implementation of the **ECLAT (Equivalence Class Transformation)** algorithm. Unlike Apriori, ECLAT uses a **vertical data format** (Item-Transaction ID sets) to find frequent itemsets and generate association rules efficiently.

## 🚀 Features
* **Vertical Data Conversion:** Automatically converts horizontal datasets (TID: Items) into vertical format (Item: TIDs).
* **Frequent Itemset Generation:** Uses a recursive depth-first search approach to find all itemsets meeting the `min_support`.
* **Association Rules:** Generates all possible rules from frequent itemsets.
* **Strong Rules Filtering:** Filters rules based on a user-defined `min_confidence`.
* **Lift Metric:** Calculates the **Lift** for each itemset to measure the importance of the rule.

## 🛠️ Requirements
* Python 3.x
* Pandas (`pip install pandas`)
* Openpyxl (to read Excel files: `pip install openpyxl`)

## 📂 Project Structure
* `ECLAT_algorithm.py`: The main source code.
* `Horizontal_DataSet.xlsx`: Sample dataset (Make sure your Excel has columns `TiD` and `items`).

## 📖 How it Works
1. **Vertical Format:** The algorithm maps each item to a set of Transaction IDs where it appears.
2. **Intersection:** To find the support of `{A, B}`, it simply calculates the intersection of the TID sets of `A` and `B`.
3. **Recursive Search:** It builds a prefix tree to explore larger itemsets.

## 📤 Output Sample
![ECLAT Output](https://github.com/user-attachments/assets/b3259060-59c8-483c-aab6-0007651f17df)
