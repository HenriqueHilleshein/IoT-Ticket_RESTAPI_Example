#include <iostream>
#include <fstream>
#include <string>
#include <sys/types.h>
#include <unistd.h>

// The dumb program used to use the processor
int main(){
    std::ofstream pidFile;
    pidFile.open("pidfile", std::ios::trunc);
    if(pidFile.is_open()){
        pidFile << getpid();
        pidFile.close();
    }
    while(true){
        std::cout << "Using processor :)" << std::endl;
    }
}
