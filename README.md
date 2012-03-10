Joos Compiler
-------------

A compiler for Joos, a subset of Java (using the JLS 2nd Edition).  The
features of Joos can be found here: http://www.student.cs.uwaterloo.ca/~cs444/joos.html

Usage
-----

To compile a Joos file, the Joos compiler can be invoked by the following command:
`./joosc file_1.java file_2.java`

For debug output, include the `--verbose` flag.

`./joosc --verbose file_1.java file_2.java`

To include the standard library, use the `--stdlib` flag.

`./joosc --stdlib file_1.java file_2.java`
