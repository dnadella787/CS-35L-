
randmain: randmain.c randcpuid.c 
	$(CC) $(CFLAGS) -c randmain.c -o randmain.o
	$(CC) $(CFLAGS) -c randcpuid.c -o randcpuid.o
	$(CC) $(CFLAGS) -ldl -Wl,-rpath=$(PWD) randmain.o randcpuid.o -o randmain  

randlibhw.so: randlibhw.o
	$(CC) $(CFLAGS) -shared randlibhw.o -o randlibhw.so

randlibhw.o: randlibhw.c
	$(CC) $(CFLAGS) -c -fPIC randlibhw.c -o randlibhw.o 

randlibsw.so: randlibsw.o
	$(CC) $(CFLAGS) -shared randlibsw.o -o randlibsw.so

randlibsw.o: randlibsw.c
	$(CC) $(CFLAGS) -c -fPIC randlibsw.c -o randlibsw.o 