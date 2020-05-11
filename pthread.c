//collaborate with xianglu

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
int total;
int task_slot[2] = {0, 0};
pthread_mutex_t task_lock;

void *producer(){
  while(total > 0){
    pthread_mutex_lock(&task_lock);
    if(task_slot[0] == 0 && task_slot[1] == 0){
      task_slot[0] = 1;
      total --;
      printf("Producer No.1 inserts 1 task\n");
    }
    else if(task_slot[0] == 1 && task_slot[1] == 0){
      task_slot[1]=1;
      total --;
      printf("Producer No.1 inserts 1 task\n");
    }
    pthread_mutex_unlock(&task_lock);
  }
  pthread_exit(0);
}



void *consumer(void *consumer_thread_data){
  int *consumer_num = (int*)consumer_thread_data;
  int t = 0;
  while(task_slot[0]==1 || total > 0){
    pthread_mutex_lock(&task_lock);
    if(task_slot[0] == 1 && task_slot[1] == 1){
      task_slot[0] = 1;
      task_slot[1] = 0;
      t ++;
      printf("Consumer %d extracts 1 task\n", *consumer_num);
    }
    else if (task_slot[0] == 1 && task_slot[1] == 0){
      task_slot[0] = 0;
      t ++;
      printf("Consumer %d extracts 1 task\n", *consumer_num);
    }
    pthread_mutex_unlock(&task_lock);
  }
  printf("In total, Consumer %d extracts %d tasks\n", *consumer_num, t);
  pthread_exit(0);
}



int main(int argc, char *argv[]){
  total = atoi(argv[1]);
  pthread_t p_thread[3];
  int consumer_num[2] = {1, 2};

  pthread_attr_t attr;
  pthread_attr_init(&attr);
  pthread_mutex_init(&task_lock, NULL);
 
  pthread_create(&p_thread[0], &attr, producer, NULL);
  pthread_create(&p_thread[1], &attr, consumer, (void*)&consumer_num[0]);
  pthread_create(&p_thread[2], &attr, consumer, (void*)&consumer_num[1]);
  pthread_join(p_thread[0], NULL);
  pthread_join(p_thread[1], NULL);
  pthread_join(p_thread[2], NULL);
  

return 0;
}
