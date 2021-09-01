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

(LOOP)
    // addr = @SCREEN
    @SCREEN
    D=A
    @addr
    M=D

    // get KBD value
    @KBD
    D=M

    // set color to black
    @color
    M=-1

    // if a key is pressed, paint
    @PAINT
    D;JGT

    // set color to white
    @color
    M=0

(PAINT)
    // get color
    @color
    D=M

    // select addr pointer
    @addr
    A=M

    // paint
    M=D

    // increase addr pointer
    @addr
    M=M+1
    D=M

    // check if paint is done
    // the next address after @SCREEN is @KBD
    @KBD
    D=D-A

    // paint if is not done
    @PAINT
    D;JLT

    // return to loop
    @LOOP
    0;JMP
