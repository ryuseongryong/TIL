- https://aaronbloomfield.github.io/pdr/docs/gdb_vs_lldb.html
- https://lldb.llvm.org/use/map.html

- GDB는 GNU 프레임워크의 일부로, GNU C++ 컴파일러인 g++와 함께 작동하도록 만들어졌다. LLDB는 LLVM 프레임워크의 일부로, LLVM C++ 컴파일러인 clang++와 작동하도록 만들어졌다.
- 이상적으로는 컴파일러와 동일한 프레임워크의 디버거를 사용하는 것이 좋다. 그러나 LLVM의 버그로 인해 Ubuntu Virtual Box image내에서 작동하지 않는다. 따라서 clang++ 컴파일러를 계속 사용하되 lldb 대신 gdb를 사용하기도 한다.
- 두 디버거 모두 어느 컴파일러로 컴파일된 코드를 디버깅할 수 있다. 이 클래스에 관한 유일한 실제 차이점은 일부 명령어에 대해서 있다. 디버거 간에는 다른 차이점이 있지만 이러한 차이점은 GDB, LLDB 명령어 요약 페이지에서 볼 수 있다.

```
Assembly-specific commands

displaying the values in the registers: info registers for gdb, registers read for lldb
set the assembly output format to what we are used to in class (and what we are programming in): set disassembly-flavor intel for gdb, settings set target.x86-disassembly-flavor intel for lldb
prints the assembly code for the supplied function (up until the next label): disassemble (function) for gdb, disassemble --name (function) for lldb
Program execution

starts a program execution, and breaks when it enters the main() function: start in gdb; there is no direct equivalent in lldb (but you can do it via two commands: b main and run)
shows the lines of source code before and after the point at which the program paused: list in gdb, f in lldb
Breakpoints

show breakpoints: info break in gdb, breakpoint
list in lldb
delete all breakpoints: delete (or just d) in gdb, breakpoint delete in lldb
delete the breakpoint indicated by (num): delete (num) in gdb, breakpoint delete (num) in lldb
Examining data

display all the local variables and their values: info
locals in gdb, frame variable in lldb
set the variable (var) to the value (value): set variable
(var) = (value) in gdb, expr (var) = (value) in lldb
```