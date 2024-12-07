# Quine-McCluskey Code
# Rabe, Gary Clyde T., Ugates, John Rhey T.
# BSECE-3D

def decimal_to_binary(decimal_num, num_bits):
    # Convert decimal number to binary representation
    binary = bin(decimal_num)[2:].zfill(num_bits)
    return binary

def count_ones(binary_num):
    # Count the number of ones in a binary number
    return binary_num.count('1')

def mul(x, y):
    res = []
    for i in x:
        if i + "'" in y or (len(i) == 2 and i[0] in y):
            return []
        else:
            res.append(i)
    for i in y:
        if i not in res:
            res.append(i)
    return res

def multiply(x, y):
    res = []
    for i in x:
        for j in y:
            tmp = mul(i, j)
            res.append(tmp) if len(tmp) != 0 else None
    return res

def refine(my_list, dc_list):
    res = []
    for i in my_list:
        if int(i) not in dc_list:
            res.append(i)
    return res

def findEPI(x):
    res = []
    for i in x:
        if len(x[i]) == 1:
            res.append(x[i][0]) if x[i][0] not in res else None
    return res

def findVariables(x, variable_letters):
    var_list = []
    for i in range(len(x)):
        if x[i] == '0':
            var_list.append(variable_letters[i] + "'")
        elif x[i] == '1':
            var_list.append(variable_letters[i])
    return var_list

def flatten(x):
    flattened_items = []
    for i in x:
        flattened_items.extend(x[i])
    return flattened_items

def findminterms(a):
    gaps = a.count('-')
    if gaps == 0:
        return [str(int(a, 2))]
    x = [bin(i)[2:].zfill(gaps) for i in range(pow(2, gaps))]
    temp = []
    for i in range(pow(2, gaps)):
        temp2, ind = a[:], -1
        for j in x[0]:
            if ind != -1:
                ind = ind + temp2[ind + 1:].find('-') + 1
            else:
                ind = temp2[ind + 1:].find('-')
            temp2 = temp2[:ind] + j + temp2[ind + 1:]
        temp.append(str(int(temp2, 2)))
        x.pop(0)
    return temp

def compare(a, b):
    c = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            mismatch_index = i
            c += 1
            if c > 1:
                return (False, None)
    return (True, mismatch_index)

def removeTerms(_chart, terms):
    for i in terms:
        for j in findminterms(i):
            try:
                del _chart[j]
            except KeyError:
                pass

def generate_logic_function():
    min_variables = 1
    max_variables = 26

    num_variables = input(f"Enter the number of variables ({min_variables}-{max_variables}): ")

    if not num_variables.isdigit() or not min_variables <= int(num_variables) <= max_variables:
        print(f"Error: Number of variables should be a numerical value between {min_variables} and {max_variables}.")
        return

    num_variables = int(num_variables)
    variable_letters = input(f"Enter {num_variables} variable letters separated by space: ").split()

    if len(variable_letters) != num_variables or any(not letter.isalpha() or len(letter) != 1 for letter in variable_letters):
        print("Error: Invalid input for variable letters.")
        return

    print("\nUser inputs:")
    print("Variables:", variable_letters)

    # User input for minterms
    print(f"Enter minterms (in decimal form, limited to {2 ** num_variables - 1}):")
    minterms_input = input("Enter minterms separated by space: ")
    minterms = []
    for minterm_str in minterms_input.split():
        try:
            minterm = int(minterm_str)
            if 0 <= minterm < 2 ** num_variables:
                minterms.append(minterm)
            else:
                print(f"Error: Minterms should be between 0 and {2 ** num_variables - 1}")
                return
        except ValueError:
            print("Error: Invalid input. Please enter integers only.")
            return

    print("Minterms:", minterms)

    dont_care_input = input("Enter don't care terms separated by space (press Enter if none): ")
    if dont_care_input.strip():
        try:
            dont_care = list(map(int, dont_care_input.split()))
            for term in dont_care:
                if term < 0 or term >= 2 ** num_variables:
                    print(f"Error: Don't care terms should be between 0 and {2 ** num_variables - 1}")
                    return
        except ValueError:
            print("Error: Invalid input for don't care terms. Please enter integers only.")
            return
    else:
        dont_care = []

    print("Don't Cares:", dont_care)

    # Convert minterms to binary representation
    binary_table = []
    for minterm in minterms + dont_care:
        binary = decimal_to_binary(minterm, num_variables)
        binary_table.append([minterm, binary])

    # Displaying the minterms in ascending order
    print("\nMinterms in Ascending Order:")
    header = ["Minterm"] + variable_letters
    print("\t".join(header))
    print("-" * (8 * num_variables + 5))
    binary_table.sort(key=lambda x: x[0])
    for row in binary_table:
        print("\t".join([str(row[0])] + [bit for bit in row[1]]))

    # Rearrange minterms based on the number of ones in their binary representation
    binary_table.sort(key=lambda x: (count_ones(x[1]), x[0]))

    # Displaying the minterms rearranged by the number of ones in binary representation
    print("\nMinterms Rearranged by Number of Ones in Binary Representation:")
    print("\t".join(header))
    print("-" * (8 * num_variables + 5))

    prev_ones = None
    for row in binary_table:
        ones = count_ones(row[1])
        if ones != prev_ones:
            if prev_ones is not None:
                print("-" * (8 * num_variables + 5))
            prev_ones = ones
        print("\t".join([str(row[0])] + [bit for bit in row[1]]))

    # Quine McCluskey Algorithm
    dc = dont_care
    minterms.sort()
    size = len(bin(minterms[-1])) - 2
    groups, all_pi = {}, set()

    # Primary grouping starts
    for term in minterms + dont_care:  # Include don't-care terms as well
        try:
            groups[bin(term).count('1')].append(bin(term)[2:].zfill(size))
        except KeyError:
            groups[bin(term).count('1')] = [bin(term)[2:].zfill(size)]
    # Primary grouping ends

    # Primary group printing starts
    print("\n\n\n\nGroup No.\tMinterms\tBinary of Minterms\n%s" % ('=' * 50))
    for i in sorted(groups.keys()):
        print("%5d:" % i)  # Prints group number
        for j in groups[i]:
            print("\t\t    %-20d%s" % (int(j, 2), j))  # Prints minterm and its binary representation
        print('-' * 50)
    # Primary group printing ends

    # Process for creating tables and finding prime implicants starts
    while True:
        tmp = groups.copy()
        groups, m, marked, should_stop = {}, 0, set(), True
        l = sorted(tmp.keys()) if tmp else []
        for i in range(len(l) - 1):
            for j in tmp[l[i]]:  # Loop which iterates through current group elements
                for k in tmp[l[i + 1]]:  # Loop which iterates through next group elements
                    res = compare(j, k)  # Compare the minterms
                    if res[0]:  # If the minterms differ by 1 bit only
                        try:
                            groups[m].append(
                                j[:res[1]] + '-' + j[res[1] + 1:]) if j[:res[1]] + '-' + j[res[1] + 1:] not in groups[
                                m] else None  # Put a '-' in the changing bit and add it to corresponding group
                        except KeyError:
                            groups[m] = [
                                j[:res[1]] + '-' + j[res[1] + 1:]]  # If the group doesn't exist, create the group at first and then put a '-' in the changing bit and add it to the newly created group
                        should_stop = False
                        marked.add(j)  # Mark element j
                        marked.add(k)  # Mark element k
            m += 1
        local_unmarked = set(flatten(tmp)).difference(marked)  # Unmarked elements of each table
        all_pi = all_pi.union(local_unmarked)  # Adding Prime Implicants to the global list
        print("Unmarked elements(Prime Implicants) of this table:",
              None if len(local_unmarked) == 0 else ', '.join(local_unmarked))  # Printing Prime Implicants of the current table
        if should_stop:  # If the minterms cannot be combined further
            print("\n\nAll Prime Implicants: ", None if len(all_pi) == 0 else ', '.join(all_pi))  # Print all prime implicants
            break
        # Printing of all the next groups starts
        print("\n\n\n\nGroup No.\tMinterms\tBinary of Minterms\n%s" % ('=' * 50))
        for i in sorted(groups.keys()):
            print("%5d:" % i)  # Prints group number
            for j in groups[i]:
                print("\t\t%-24s%s" % (','.join(findminterms(j)), j))  # Prints minterms and its binary representation
            print('-' * 50)
        # Printing of all the next groups ends
    # Process for creating tables and finding prime implicants ends

    # Printing and processing of Prime Implicant chart starts
    sz = len(str(minterms[-1]))  # The number of digits of the largest minterm
    chart = {}
    print(f'\n\n\nPrime Implicants chart:\n\n    Minterms    |{" ".join((str(i).rjust(sz) for i in minterms))}'
      f'\n{"=" * (len(minterms) * (sz + 1) + 16)}')

    for i in all_pi:
        merged_minterms, y = findminterms(i), 0
        print("%-16s|" % ','.join(merged_minterms), end='')
        for j in refine(merged_minterms, dc):
            x = minterms.index(int(j)) * (sz + 1)  # The position where we should put 'X'
            print(' ' * abs(x - y) + ' ' * (sz - 1) + 'X', end='')
            y = x + sz
            try:
                chart[j].append(
                    i) if i not in chart[j] else None  # Add minterm in the chart
            except KeyError:
                chart[j] = [i]
        print('\n' + '-' * (len(minterms) * (sz + 1) + 16))
    # Printing and processing of Prime Implicant chart ends

    EPI = findEPI(chart)  # Finding essential prime implicants
    print("\nEssential Prime Implicants: " + ', '.join(str(i) for i in EPI))
    removeTerms(chart, EPI)  # Remove EPI related columns from the chart

    if len(chart) == 0:  # If no minterms remain after removing EPI related columns
        final_result = [findVariables(i, variable_letters) for i in EPI] # Final result with only EPIs
    else:  # Else follow Petrick's method for further simplification
        P = [[findVariables(j) for j in chart[i]] for i in chart]
        while len(P) > 1:  # Keep multiplying until we get the SOP form of P
            P[1] = multiply(P[0], P[1])
            P.pop(0)
        final_result = [min(P[0], key=len)]  # Choosing the term with minimum variables from P
        final_result.extend(findVariables(i, variable_letters) for i in EPI)  # Adding the EPIs to the final solution
    print('\n\nMinimal Quine-McCluskey Expression: F = ' + ' + '.join(''.join(i) for i in final_result))

if __name__ == "__main__":
    generate_logic_function()