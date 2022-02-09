"""
    Name: Vanshika Jain
    Roll No.: BT18CSE107
"""

import sys
def edit_dist_fun(str1, str2, m, n, sub_mat):

    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]
    sub = [[0 for x in range(n + 1)] for x in range(m + 1)]
    delm = [[0 for x in range(n + 1)] for x in range(m + 1)]
    ins = [[0 for x in range(n + 1)] for x in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):

            if i == 0:
                dp[i][j] = j  # Min. operations = j
                sub[i][j] = j
                delm[i][j] = j
                ins[i][j] = j

            elif j == 0:
                dp[i][j] = i  # Min. operations = i
                sub[i][j] = i
                delm[i][j] = i
                ins[i][j] = i
            else:
                c1 = ord(str1[i - 1]) - ord("A")
                c2 = ord(str2[j - 1]) - ord("A")
                sub[i][j] = dp[i - 1][j - 1] + int(sub_mat[c1][c2])
                delm[i][j] = dp[i - 1][j] + 1
                ins[i][j] = dp[i][j - 1] + 1

                dp[i][j] = min(
                    ins[i][j], delm[i][j], sub[i][j]  # Insert  # Remove
                )  # Replace

    return dp[m][n], dp, sub, delm, ins

def possiblePaths(cost, subm, delm, insm, m, n, paths, str1, str2):
    if m == 0 and n == 0:
        print("Possible paths: ", paths)
        return
    # Insertion
    elif m == 0:
        paths.append(('Insert to ' + str2, str2[n - 1]))
        possiblePaths(cost, subm, delm, insm, m, n - 1, paths, str1, str2)
        paths.pop()
        return
    # Deletion
    elif n == 0:
        paths.append((str1[m - 1], 'Delete from ' + str1))
        possiblePaths(cost, subm, delm, insm, m - 1, n, paths, str1, str2)
        paths.pop()
        return
    else:
        # Sustitution
        if cost[m][n] == subm[m][n]:
            paths.append(('Substitute: ', str1[m - 1], str2[n - 1]))
            possiblePaths(cost, subm, delm, insm, m - 1, n - 1, paths, str1, str2)
            paths.pop()
        # Deletion
        if cost[m][n] == delm[m][n]:
            paths.append((str1[m - 1], 'Delete from ' + str1))
            possiblePaths(cost, subm, delm, insm, m - 1, n, paths, str1, str2)
            paths.pop()
        # Insertion
        if cost[m][n] == insm[m][n]:
            paths.append(('Insert to ' +str2, str2[n - 1]))
            possiblePaths(cost, subm, delm, insm, m, n - 1, paths, str1, str2)
            paths.pop()
        return


if __name__ == "__main__":
    print("\nReading from subMatrix.txt")
    with open("subMarix.txt", "r") as f:
        lines = f.readlines()
    adj = []
    for i in range(len(lines)):
        line = lines[i]
        val = line.split()
        adj.append(val)

    print(len(adj), len(adj[0]))

    print("Enter String 1")
    str1 = input()
    
    print("Enter String 2")
    str2 = input()
    
    cost, cost_mat, subs_mat, del_mat, ins_mat = edit_dist_fun(
        str1.upper(), str2.upper(), len(str1), len(str2), adj
    )
    print("\nCost of converting " ,str1, " to ", str2, " : ", cost)
    
    possiblePaths(
        cost_mat, subs_mat, del_mat, ins_mat, len(str1), len(str2), [], str1, str2
    )