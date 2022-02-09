"""
    Name: Vanshika Jain
    Roll No.: BT18CSE107
"""

class KMP:
    def __init__(self, pat, txt):
        self.pat = pat
        self.txt = txt
        self.computeLPSArray()
        
    def computeLPSArray(self):
        leng = 0 # length of the previous longest prefix suffix
        self.lps = [0]
        i = 1
        while i < len(self.pat):
            if self.pat[i]== self.pat[leng]:
                leng += 1
                self.lps.append(leng)
                i += 1
            else:
                if leng != 0:
                    leng = self.lps[leng-1]

                # Also, note that we do not increment i here
                else:
                    self.lps.append(0)
                    i += 1
                
    def KMPSearch(self):
        M = len(self.pat)
        N = len(self.txt)

        j = 0 # index for pat[]

        print("\nLPS Array formed: " ,self.lps)
        i = 0 # index for txt[]
        while i < N:
            if self.pat[j] == self.txt[i]:
                i += 1
                j += 1

            if j == M:
                print ("\nFound pattern at index " + str(i-j))
                j = self.lps[j-1]

            elif i < N and self.pat[j] != self.txt[i]:
                if j != 0:
                    j = self.lps[j-1]
                    print("NOT FOUND! Jump back to", j)
                else:
                    i += 1

if __name__ == '__main__':

    txt = input("Enter text: ")
    pat = input("Enter pattern: ")
    k = KMP (pat.lower(), txt.lower())
    k.KMPSearch()