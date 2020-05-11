//OpenMP
//Collaborate with Xianglu

#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

int thread[4] = {0,0,0,0};


int get_pi(int num){
  int count;
  int local_hits = 0;
  int rdm = 3000000;
  double x_coord, y_coord;
  for (count = 0; count < rdm; count++){
    x_coord = (double)rand() / (RAND_MAX) - 0.5;
    y_coord = (double)rand() / (RAND_MAX) - 0.5;
    if ((x_coord * x_coord + y_coord * y_coord)<0.25){
      local_hits ++;
    }
  }
  thread[num] = rdm;
  return local_hits;
}



int main(){
  float pi;
  int total_hits = 0;
  int total = 0;
  #pragma omp parallel reduction(+: total_hits, total) num_threads(4)
  {
    #pragma omp sections
    {
      #pragma omp section
      {
        total_hits = get_pi(0);
        total = thread[0];
      }
      #pragma omp section
      {
        total_hits = get_pi(1);
        total = thread[1];
      }
      #pragma omp section
      {
        total_hits = get_pi(2);
        total = thread[2];
      }
      #pragma omp section
      {
        total_hits = get_pi(3);
        total= thread[3];
      }
    }
    #pragma omp barrier
  }

  pi = (float) total_hits/total *4;
  printf("pi is around %f\n", pi);
}





