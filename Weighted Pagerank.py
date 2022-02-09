from math import log

def main():
    f = open('pr_input.txt','r')
    occur = []
    rel = []
    Nr = 0
    N = 0
    terms = 0
    query = [int(i) for i in f.readline().strip().split()]

    for line in f.readlines():
        line = line.strip()
        li =  [int(i) for i in line.split()]
        occur.append(li[:-1])
        rel.append(li[-1])
        if li[-1]==1:
            Nr += 1
        N += 1
        terms = len(li)-1
        
    f.close()

    Nt = [0]*terms
    Ntr = [0]*terms

    for i in range(terms):
        for j in range(N):
            if occur[j][i]==1:
                Nt[i] += 1
                if rel[j]==1:
                    Ntr[i] += 1

    print('N =',N)
    print('Nr = ',Nr)
    print('Nt = ',Nt)
    print('Ntr = ',Ntr)
    print('Query = ',query)
    Pt = [0]*terms
    Ptbar = [0]*terms
    for i in range(terms):
        Pt[i] = Ntr[i]/Nr
        Ptbar[i] = (Nt[i] - Ntr[i])/(N - Nr)

    print('Pt = ',Pt)
    print('Ptbar = ',Ptbar)
    print()
    wts = [0]*terms
    for pos,i in enumerate(query):
        if i==1:
            w = log( (Ntr[pos] + 0.5)*(N - Nt[pos] - Nr + Ntr[pos] + 0.5) / ((Nr - Ntr[pos] + 0.5) * (Nt[pos] - Ntr[pos] + 0.5)), 10)
            print('weight',pos+1,w)
            wts[pos] = w
    
    print()
    scores = [0]*N
    for i in range(N):
        for j in range(len(query)):
            if query[j]==1:
                scores[i] += occur[i][j]*wts[j]
    
    print('scores = ',scores)
    
    ranks = []
    for i in range(len(scores)):
      ranks.append([scores[i],i])
    ranks.sort(reverse=True)
    sort_index = []
    
    for x in ranks:
        sort_index.append(x[1]+1)
    
    print(sort_index)

    # rounds = 5
    # for _ in range(rounds):
    #     d1 = input("Vector: ")
    #     d = [int(i) for i in d1.strip().split()]
    #     print(d)
    #     score = 0
    #     for j in range(len(query)):
    #         if query[j]==1:
    #             print(d[j], wts[j])
    #             scores += (d[j]*wts[j])
    #     print("Score for :", d1, score)

main()