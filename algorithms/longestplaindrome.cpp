#include<iostream>
using namespace std;
#include<string.h>

int plandrome(string a){
    int s = a.size();
    if(s ==1)return 1;
    if (s==2) a.substr(0,1) == a.substr(1,1) ? 2 : -1;
    for(int i=0; i<s/2 ;i++){
        if( a.substr(i,1) != a.substr(s -(i+1),1)) return -1;
    }
    return s;
}

//Brute Force:: complexity is O(N^3)
int largest_plandrome_bf(string a){
    int max_counter = -1;
    int s = a.size();
    for (int i=0; i< s; i++){
        for(int j=0; j< s; j++){
             max_counter = max(plandrome(a.substr(i,j)),max_counter);
        }
    }
    return max_counter;
}


//dynamic Programming:: Complexity is O(N^2)
//Memoization:: O(N^2) for space complexity
int largest_plandrome_df(string a,char *MEM[]){
    // substrucuture by length
    for(int i=0;i<a.size();i++){
        MEM[i][i] = 1;
    }
    int j;
    //substructure by length
    for(int sslen=2; sslen<= a.size(); sslen++){
        for(int i=0; i< a.size() - sslen+ 1; i++){
            j =  i + sslen -1;
            if (a.substr(i,1) == a.substr(j,1) && sslen == 2)
               MEM[i][j] = 2;
            else if (a.substr(i,1) == a.substr(j,1))
               MEM[i][j] = MEM[i+1][j-1] + 2;
            else
                 MEM[i][j] = max(MEM[i][j-1], MEM[i+1][j]);
         }
     }
    return MEM[0][a.size()-1];
 }



 main(){
     string a = "xxxmadamyyy";
     cout<<"Brute force largest plandrome ="<<largest_plandrome_bf(a)<<endl;
     // MEMORIZATION INITILIZATION HERE
     char **MEM;
     MEM  = new char*[a.size()];
     for(int i=0;i<a.size();i++)
         MEM[i] = new char[a.size()];
     //SENDING MEM TO MAINTAIN THE STATE INITIAL ACTION or SUBSTRUTURES
     cout<<"Dynamic Programming largest plandrome ="<<largest_plandrome_df(a,MEM)<<endl;
 }

