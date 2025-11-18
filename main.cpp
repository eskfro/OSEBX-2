#include <iostream>
#include <cstdlib>

#define PYTHON_INTERPRETER "C:\\Users\\eskfr\\anaconda3\\envs\\apienv\\python.exe"
#define PYTHON_SCRIPT "main.py"

int main() {
    
    std::string command = std::string(PYTHON_INTERPRETER) + " " + PYTHON_SCRIPT;
    int result = std::system(command.c_str());

    if(result == 0) {
        std::cout << "Python script executed successfully." << std::endl;
    } else {
        std::cerr << "Error: Python script execution failed with code " << result << std::endl;
    }

    return result;
}
