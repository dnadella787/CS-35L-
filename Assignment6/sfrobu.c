#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <ctype.h>
#include <string.h>
#include <sys/stat.h>

//global var to see if -f flag or not
int flag = 0;

//decrypts character according to flag
int decrypt(const char a){
    if (flag)
        return (toupper((unsigned char)(a ^ 42)));
    return (a ^ 42);   
}


int frobcmp(const char *a, const char *b){
    while(1)
    {
        while (*a == '\0'){
            a++;
        }
        while (*b == '\0'){
            b++;
        }
        if (*a == ' ' && *b == ' ')
            return 0;
        if (*a == ' ' && *b != ' ')
            return -1;
        if(*a != ' ' && *b == ' ')
            return 1;
        if(decrypt(*a) == decrypt(*b)){
            a++;b++;
            continue;
        }
        if(decrypt(*a) > decrypt(*b))
            return 1;
        if(decrypt(*a) < decrypt(*b))
            return -1;
    }
}

int compare(const void *a, const void *b){
    return frobcmp(*(char**) a, *(char**) b);
}

//error checking funtions:
void inputCheck(int val){
    if (val < 0){
        write(STDERR_FILENO, "Error reading stdin\n", 21);
        exit(1);
    }
}

void outputCheck(int val){
    if (val < 0){
        write(STDERR_FILENO, "Error writing to stdout\n", 25);
        exit(1);
    }
}

void allocCheck(const void *a){
    if (a == NULL){
        write(STDERR_FILENO, "Memory alloc error\n", 20);
        exit(1);
    }
}

int main(int argc, char** argv){
    if (argc > 2){
        write(STDERR_FILENO, "too many args\n", 15);
        exit(1);
    }
    
    if (argc == 2){
        if (!(strcmp(argv[1], "-f")))
            flag = 1;
        else{
            write(STDERR_FILENO, "only -f flag allowed\n", 22);
            exit(1);
        }
    } 

    struct stat fileData;
    if (fstat(STDIN_FILENO, &fileData) < 0){
        write(STDERR_FILENO, "fstat error\n", 13);
        exit(1);
    }

    int bufferLength = 0;
    char *buffer = NULL;
    int charLength = 0;
    //if regular file read whole file.
    if (S_ISREG(fileData.st_mode))
    {
        bufferLength = fileData.st_size;
        if (bufferLength != 0){
            buffer = realloc(buffer, sizeof(char) * (bufferLength));
            allocCheck(buffer);
            int returnVal = read(STDIN_FILENO, buffer, bufferLength);
            inputCheck(returnVal);
            charLength = bufferLength;
        }
    }
    else{
        bufferLength = 8;
        buffer = realloc(buffer, sizeof(char) * (bufferLength));
        allocCheck(buffer);
    }

    //read contents and append 
    while (1){
        if (bufferLength == 0)
            break;
        if ((bufferLength / 2) <= charLength)
        {
            bufferLength *= 2;
            buffer = realloc(buffer, sizeof(char) * bufferLength);
            allocCheck(buffer);
        }
        int returnVal = read(STDIN_FILENO, buffer+charLength, 1);
        charLength++;
        if (returnVal == 0){
            buffer[charLength-1] = EOF;
            break;
        }
        inputCheck(returnVal);
    }




    char *word = NULL;
    char **allWords = NULL;

    int wordLength = 0;
    int numWords = 0;

    int currChar;
    //parse buffer into 2D array
    for (int i = 0; i < charLength; i++)
    {
        currChar = buffer[i];

        if (currChar != ' ' && currChar != EOF){
            word = realloc(word, sizeof(char) * (wordLength+1));
            allocCheck(word);
            word[wordLength] = currChar;
            wordLength++;
        }
        else{
            word = realloc(word, sizeof(char) * (wordLength + 1));
            allocCheck(word);
            word[wordLength] = ' ';
            wordLength = 0;

            allWords = realloc(allWords, sizeof(char *) * (numWords + 1));
            allocCheck(allWords);
            allWords[numWords] = word;
            word = NULL;
            numWords++;
            if ((charLength == 1) && (buffer[0] == EOF)){
                numWords--;
            }
        }
    }


    qsort(allWords, numWords, sizeof(char *), compare);

    for (int i = 0; i < numWords; i++)
    {
        for (int j = 0; allWords[i][j] != ' '; j++)
        {
            int returnVal = write(STDOUT_FILENO, &allWords[i][j], 1);
            outputCheck(returnVal);
        }
        char space = ' ';
        int returnVal = write(STDOUT_FILENO, &space, 1);
        outputCheck(returnVal);
        free(allWords[i]);
    }
    free(allWords);
    free(word);
    free(buffer);
}
