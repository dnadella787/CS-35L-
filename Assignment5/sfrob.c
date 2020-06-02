#include <stdio.h>
#include <stdlib.h>


int decrypt(const char a){
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

void inputCheck(){
    if (ferror(stdin)){
        fprintf(stderr, "Error reading stdin\n");
        exit(1);
    }
}

void outputCheck(){
    if (ferror(stdout)){
        fprintf(stderr, "Error writing to stdout\n");
        exit(1);
    }
}

void allocCheck(const void *a){
    if (a == NULL){
        fprintf(stderr, "Memory alloc error\n");
        exit(1);
    }
}

int main(){
    char *word = NULL;
    char **allWords = NULL;

    int wordLength = 0;
    int numWords = 0;

    int currChar;
    while(!feof(stdin)){
        currChar = getchar();
        inputCheck();

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
        }
    }

    qsort(allWords, numWords, sizeof(char *), compare);

    for (int i = 0; i < numWords; i++){
        for (int j = 0; allWords[i][j] != ' '; j++){
            putchar(allWords[i][j]);
            outputCheck();
        }
        putchar(' ');
        outputCheck();
        free(allWords[i]);
    }
    free(allWords);
    free(word);
}
