#include<map>
#include<vector>
#include<string>
#include<fstream>
#include<sstream>
#include<iostream>
#include<climits>
#include <chrono>

using namespace std;
using namespace std::chrono;

class InvertedIndex {
public:
    explicit InvertedIndex(const string &fileName);

    map<string, vector<long > > index;

    void print();
};

InvertedIndex :: InvertedIndex(const string &fileName) {
    cout << "Creating Inverted Index from " << fileName << "..." << endl;
    ifstream inFile;
    inFile.open(fileName);
    string word;
    long i = 0;
    while (inFile >> word) {
        if (this->index.find(word) == this->index.end()) {
            this->index[word] = vector<long>();
        }
        this->index[word].push_back(i);
        i++;
    }
}

void InvertedIndex::print() {
    for (const auto &entry : this->index ) {
        cout << entry.first << ": ";
        for (const auto &i: entry.second ) {
            cout << i << " ";
        }
        cout << endl;
    }
}

long binaryNext(map<string, vector<long> > &index, const string &word, long i) {
    auto ls = index[word];
    if (ls.empty() || ls[ls.size() - 1] <= i) {
        return LONG_MAX;
    }
    if (ls[0] > i) {
        return ls[0];
    }
    long low = 0;
    long high = ls.size() - 1;
    long mid;
    while (high - low > 1) {
        mid = (low + high) / 2;
        if (ls[mid] <= i) {
            low = mid;
        } else {
            high = mid;
        }
    }
    return ls[high];
}

long gallopingBinary(map<string, vector<long> > &index, const string &word, long i, long low, long high) {
    auto ls = index[word];
    long mid;
    while (high - low > 1) {
        mid = (low + high) / 2;
        if (ls[mid] <= i) {
            low = mid;
        } else {
            high = mid;
        }
    }
    return high;
}

long gallopingNext(map<string, vector<long> > &index, const string &word, long i, long *gallopingCache) {
    auto ls = index[word];
    if (ls.empty() || ls[ls.size() - 1] <= i) {
        return LONG_MAX;
    }
    if (ls[0] > i) {
        *gallopingCache = 0;
        return ls[*gallopingCache];
    }
    long low = 0;
    if(*gallopingCache >= ls.size()){
        *gallopingCache = 0;
    }
    if (*gallopingCache > 0 && ls[*gallopingCache - 1] <= i) {
        low = *gallopingCache - 1;
    }
    long jump = 1;
    long high = low + jump;
    while (high < ls.size() && ls[high] <= i) {
        jump *= 2;
        low = high;
        high += jump;
    }
    if (high > ls.size()) {
        high = ls.size()-1;
    }
    *gallopingCache = gallopingBinary(index, word, i, low, high);
    return ls[*gallopingCache];
}

long linearNext(map<string, vector<long> > &index, const string &word, long i, long *linearCache) {
    auto ls = index[word];
    if (ls.empty() || ls[ls.size() - 1] <= i) {
        return LONG_MAX;
    }
    if (ls[0] > i) {
        *linearCache = 0;
        return ls[*linearCache];
    }
    if(*linearCache >= ls.size()){
        *linearCache = 0;
    }
    
    if (*linearCache > 0 && ls[*linearCache - 1] >= i) {
        *linearCache = 0;
    }
    while (*linearCache < ls.size() && ls[*linearCache] <= i) {
        *linearCache += 1;
    }
    return ls[*linearCache];
}

pair<long, long> nextPhraseBinarySearch(map<string, vector<long> > &index, const vector<string> &phrase, long position) {
    long u = binaryNext(index, phrase[0], position);
    long v = u;
    long n = phrase.size();
    for (int i = 1; i < phrase.size(); i++) {
        v = binaryNext(index, phrase[i], v);
    }
    if (v == LONG_MAX) {
        return make_pair(LONG_MAX, LONG_MAX);
    }
    if (v - u == phrase.size() - 1) {
        return make_pair (u, v);
    } else {
        return nextPhraseBinarySearch(index, phrase, v - n);
    }
}

pair<long, long> nextPhraseGallopingSearch(map<string, vector<long> > &index, const vector<string> &phrase, long position, long *gallopingCache) {
    long u = gallopingNext(index, phrase[0], position, gallopingCache);
    long v = u;
    long n = phrase.size();
    for (int i = 1; i < phrase.size(); i++) {
        v = gallopingNext(index, phrase[i], v, gallopingCache);
    }
    if (v == LONG_MAX) {
        return make_pair(LONG_MAX, LONG_MAX);
    }
    if (v - u == phrase.size() - 1) {
        return make_pair(u, v);
    } 
    else {
        return nextPhraseGallopingSearch(index, phrase, v - n, gallopingCache);
    }
}

pair<long, long> nextPhraseLinearSearch(map<string, vector<long> > &index,const vector<string> &phrase, long position, long *linearCache) {
    long u = linearNext(index, phrase[0], position, linearCache);
    long v = u;
    long n = phrase.size();
    for (int i = 1; i < phrase.size(); i++) {
        v = linearNext(index, phrase[i], v, linearCache);
    }
    if (v == LONG_MAX) {
        return make_pair(LONG_MAX, LONG_MAX);
    }
    if (v - u == phrase.size() - 1) {
        return make_pair(u, v);
    } 
    else {
        return nextPhraseLinearSearch(index, phrase, v - n, linearCache);
    }
}


int main(int argc, char **argv) {
    
    ifstream inFile;
    inFile.open("Corpus/file.txt");
    string word;
    vector< InvertedIndex> InvertedIndexes;
    int j = 0;
    while (inFile >> word){
        string p = "Corpus/PreppedDocs/" + word;
        InvertedIndex index(p);
        InvertedIndexes.push_back(index);
    }
    inFile.close();

    map<int, vector<string> > query;
    ifstream MyReadFile("Corpus/inp.txt");
    string myText;
    j = 0;
    while (getline (MyReadFile, myText)) {
        stringstream ss(myText);
        string word;
        while(ss >> word ){
            query[j].push_back(word);
        }
        j++;
    }
    MyReadFile.close();

    ofstream outFile("time.txt");

    cout<<"\n------- USING BINARY SEARCH -------\n";
    for (int j = 0; j<query.size(); j++){
        for (auto k : query[j]){
            cout<<k<<" "<<flush;
        }
        auto start = high_resolution_clock::now();
        long count;
        for (int i = 0; i<InvertedIndexes.size(); i++ ){
            long start = -1;
            count = 0;
            while(start != LONG_MAX){
                pair<long, long> binary_bounds = nextPhraseBinarySearch(InvertedIndexes[i].index, query[j], start);
                if (binary_bounds.first != LONG_MAX)
                    // cout << "DOC"<<i+1<<" "<<binary_bounds.first << " " << binary_bounds.second << endl;
                    count++;
                start = binary_bounds.second;
            }
            cout<<count<<endl;
        }
        auto stop = high_resolution_clock::now();

        auto duration = duration_cast<microseconds>(stop-start);
        outFile << "binary" << "," << query[j].size() << "," << count << ","
                << duration.count() << endl;
    }

    cout<<"\n------- USING GALLOPING SEARCH -------\n";

    for (int j = 0; j<query.size(); j++){
        for (auto k : query[j]){
            cout<<k<<" "<<flush;
        }
        auto start = high_resolution_clock::now();
        long count;
        for (int i = 0; i<InvertedIndexes.size(); i++ ){
            long start = -1;
            long gallopingCache = 0;
            count = 0;
            while(start != LONG_MAX){
                pair<long, long> galloping_bounds = nextPhraseGallopingSearch(InvertedIndexes[i].index, query[j], start, &gallopingCache);
                if (galloping_bounds.first != LONG_MAX)
                    // cout << "DOC"<<i+1<<" "<<galloping_bounds.first << " " << galloping_bounds.second << endl;
                    count++;
                start = galloping_bounds.second;
            }
            cout<<count<<endl;
        }
        auto stop = high_resolution_clock::now();
        auto duration = duration_cast<microseconds>(stop-start);
        outFile << "galloping" << "," << query[j].size() << "," << count << ","
                << duration.count() << endl;
    }

    cout<<"\n------- USING LINEAR SEARCH -------\n";

    for (int j = 0; j<query.size(); j++){

        for (auto k : query[j]){
            cout<<k<<" "<<flush;
        }
        // cout<<endl;
        auto start = high_resolution_clock::now();
        long count;
        for (int i = 0; i<InvertedIndexes.size(); i++ ){
            long start = -1;
            long linearCache = 0;
            count = 0;
            while(start != LONG_MAX){
                pair<long, long> linear_bounds = nextPhraseLinearSearch(InvertedIndexes[i].index, query[j], start, &linearCache);
                    // pair<long, long> binary_bounds = nextPhraseBinarySearch(InvertedIndexes[i].index, query[j], start);
                if (linear_bounds.first != LONG_MAX)
                    // cout << "DOC"<<i+1<<" "<<linear_bounds.first << " " << linear_bounds.second << endl;
                    count++;
                start = linear_bounds.second;
            }
            cout<<count<<endl;
        }
        auto stop = high_resolution_clock::now();
        auto duration = duration_cast<microseconds>(stop-start);
        outFile << "linear" << "," << query[j].size() << "," << count << ","
                << duration.count() << endl;
    }
    outFile.close();   
}
