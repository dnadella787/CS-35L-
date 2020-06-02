#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//check if any error in stdin
void inputCheck(){
    if (ferror(stdin)){
        fprintf(stderr, "Error reading stdin\n");
        exit(1);
    }
}
//check if an error in stdout
void outputCheck(){
    if(ferror(stdout)){
        fprintf(stderr, "Error writing to stdout\n");
        exit(1);
    }
}

int main(int argc, char** argv){
    //only two args allowed
    if(argc != 3){
        fprintf(stderr, "trb only takes 2 inputs\n");
        exit(1);
    }

    //both args must be same length
    int fromLength = strlen(argv[1]);
    int toLength = strlen(argv[2]);
    if(fromLength != toLength){
        fprintf(stderr, "inputs of differing lengths\n");
        exit(1);
    }

    //no repeats allowed in FROM arg
    for(int i = 0; i < fromLength; i++){
        for(int j = i + 1; j < fromLength; j++){
            if (argv[1][i] == argv[1][j]){
                fprintf(stderr, "repeat chars in first set\n");
                exit(1);
            }
        }
    }

    //translate characters
    while(1){
        int curr = getchar();
        inputCheck();
        if (curr == EOF)
            break;

        for (int i = 0; i < fromLength; i++){
            if (curr == argv[1][i]){
                curr = argv[2][i];
                break;
            }
        }
        putchar(curr);
        outputCheck();
    }
}