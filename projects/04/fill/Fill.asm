// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

    @i          // i: screen offset
    M=0

(LOOP)
    @KBD
    D=M
    @color
    M=-1
    @PAINT
    D;JNE       // if read something, jump to PAINT
    @color
    M=0
    @PAINT
    0;JMP       // otherwise, jump to CLEAR
    @LOOP
    0;JMP       // loops

(PAINT)
    @i          // if offset >= 8192, skip PAINT (whole screen is already painted)
    D=M
    @8192
    D=D-A
    @LOOP
    D;JGE

    @i          // SCREEN[i] = -1
    D=M
    @SCREEN
    A=D+A
    @color
    D=M
    @SCREEN
    M=D
    @i          // i++
    M=M+1

    @LOOP       // return
    0;JMP
