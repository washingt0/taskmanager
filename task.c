#include <stdio.h>
#include <stdlib.h>

void init(){
	system("rm -r /tmp/task/");
	system("mkdir /tmp/task");
	system("find /proc/* -maxdepth 0 -type d > /tmp/task/tasks.tsk");
}

int main(){
	init();
	return 0;
}