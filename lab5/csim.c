#include"cachelab.h"
#include<unistd.h>
#include<stdio.h>
#include<stdlib.h>
#include<getopt.h>  
#define MAXSIZE 30
char input[MAXSIZE];
struct sCache {
  int vaild; 
  int tag;   
  int count; 
};
typedef struct sCache Cache;
int hit_count = 0, miss_count = 0, eviction_count = 0;
int hextodec(char c) {
  if (c >= '0' && c <= '9') {
    return c - '0';
  }
  if (c >= 'A' && c <= 'F') {
    return c - 'A' + 10;
  }
  if (c >= 'a' && c <= 'f') {
    return c - 'a' + 10;
  }
  return 0;
}
void one_Line(int count, unsigned int setindex,unsigned int tag, double S, unsigned int E, double B, Cache *cache) {

  for (int i = 0; i < E; i++) {
    unsigned int target = setindex*E+i;
    if (cache[target].vaild && tag == cache[target].tag) {
      cache[target].count = count;
      hit_count++;
      return;
    }
  }

  miss_count++;
  for (int i = 0; i < E; i++) {
    unsigned int target = setindex*E+i;
    if (!cache[target].vaild) {
      unsigned int target = setindex*E+i;
      cache[target].tag = tag;
      cache[target].count = count;
      cache[target].vaild = 1;
      return;
    }
  }

  // LRU
  int mix_index = 0;
  int mix_count = 100000;
  for (int i = 0; i < E; i++) {
    unsigned int target = setindex*E+i;
    if (cache[target].count < mix_count) {
      mix_count = cache[target].count;
      mix_index = i;
    }
  }
  eviction_count++;
  unsigned int target = setindex*E+mix_index;
  cache[target].tag = tag;
  cache[target].count = count;
  cache[target].vaild = 1;
  return;
}
int main(int argc, char *argv[])
{
	int count = 0;
	int opt = 0;                     
  	unsigned int s = 0, E = 0, b = 0; 
  	double S = 0, B = 0; 
  	char *t = "";              
	while ((opt = getopt(argc, argv, "s:E:-b:-t:")) != -1) {
    	switch (opt) {
		    case 's':
		      s = atoi(optarg);
		      S = 1 << s; 
		      break;
		    case 'E':
		      E = atoi(optarg); 
		      break;
		    case 'b':
		      b = atoi(optarg);
		      B = 1 << b; 
		      break;
		    case 't':
		      t = optarg; 
		      break;
	    }
   }
   Cache *cache = (Cache *)malloc(16 * S * E);
   for (int i = 0; i < S * E; i++) { 
    cache[i].vaild = 0;
    cache[i].tag = 0;
    cache[i].count = 0;
  }
    FILE *fp;
    fp = fopen(t,"r");
  while (fgets(input, MAXSIZE, fp)) {
    int op = 0; 
    unsigned int offset = 0, tag = 0,setindex = 0; 
    char c;
    int cflag = 0;                 
    unsigned int address = 0; 
    count++;                           

    for (int i = 0; (c = input[i]) && (c != '\n'); i++) {
      if (c == ' ') { 
        continue;
      } else if (c == 'I') {
        op = 0; 
      } else if (c == 'L') {
        op = 1; 
      } else if (c == 'S') {
        op = 1; 
      } else if (c == 'M') {
        op = 2; 
      } else if (c == ',') {
        cflag = 1; //�ж��� 
      } else {
        if (cflag) {          
          continue;
        } else {
          address = 16 * address + hextodec(c); 
        }
      }
    }

    for (int i = 0; i < b; i++) {
      offset = offset * 2 + address % 2;
      address >>= 1;
    }
    for (int i = 0; i < s; i++) {
      setindex = setindex * 2 + address % 2;
      address >>= 1;
    }
    tag = address;

    if (op == 1) {
      one_Line(count, setindex, tag, S, E, B, cache);
    }
   
    if (op == 2) {
      one_Line(count, setindex, tag, S, E, B, cache);
      hit_count++;
    }
  }
	free(cache);
	fclose(fp);
	printSummary(hit_count, miss_count, eviction_count);
	return 0;
}

