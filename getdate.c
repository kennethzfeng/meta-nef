#include <stdio.h>

int s2n(char* slice) {
    /* slice is 4bytes */
    int res = 0;
    char c;
    int i;

    for(i = 0; i < 4; ++i) {
        c = *(slice+i);
        res = (res << 8) | c;
    return res;
    }
}
    
int main() {
    int i;
    char filename[80];
    char slice[4];
    FILE* fp;
    for(i = 0; i < 4; ++i) {
        sprintf(filename, "%d.nef", i+1);
        fp = (filename, "r");
        fseek(fp, 234, SEEK_SET);
        fread(slice, 4, sizeof(char), fp);
        printf("%d\n", s2n(slice));
    }

    return 0;
}
