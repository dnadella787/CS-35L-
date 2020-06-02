#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

//check if any error in stdin
void inputCheck(int val){
    if (val < 0){
        write(STDERR_FILENO, "Error reading stdin\n", 21);
        exit(1);
    }
}
//check if an error in stdout
void outputCheck(int val){
    if(val < 0){
        write(STDERR_FILENO, "Error writing to stdout\n", 25);
        exit(1);
    }
}

int main(int argc, char** argv){
    //only two args allowed
    if(argc != 3){
        write(STDERR_FILENO, "trb only takes 2 inputs\n", 25);
        exit(1);
    }

    //both args must be same length
    int fromLength = strlen(argv[1]);
    int toLength = strlen(argv[2]);
    if(fromLength != toLength){
        write(STDERR_FILENO, "inputs of differing lengths\n", 29);
        exit(1);
    }

    //no repeats allowed in FROM arg
    for(int i = 0; i < fromLength; i++){
        for(int j = i + 1; j < fromLength; j++){
            if (argv[1][i] == argv[1][j]){
                write(STDERR_FILENO, "repeat chars in first set\n", 27);
                exit(1);
            }
        }
    }

    //translate characters
    while(1){
        char curr[1];
        int returnVal = read(STDIN_FILENO, curr, 1);
        //EOF reached, read returns 0 for EOF
        if (returnVal == 0)
            break;
        inputCheck(returnVal);

        for (int i = 0; i < fromLength; i++){
            if (curr[0] == argv[1][i]){
                curr[0] = argv[2][i];
                break;
            }
        }
        returnVal = write(STDOUT_FILENO, curr, 1);
        outputCheck(returnVal);
    }
}