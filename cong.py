
#danhsach = [1, 2,3,4,5,6,7,8,9,10, ...., 10000000]
#tong = 0
#for i=1 => 1000000
# i =1 tong = tong +i= 1
# i =2 tong = tong +i=1+2 =3
# i =3 tong = tong +i = 3+3=6
# i =4 ...
# ......
# ... tong = tong +i= x + 10000000
#tong = 0
#tong = tong + i
#
#
#tong
#syntax 
#        for( int i=1;i<10000;i++) {
#            tong = tong + i
#        } # C/C++
#
#        for i in range(1,1000000,1):
#            tong = tong + i #python
#
#
#        for ( var i=1; i<1000; i++) #javascript
#        for (Int i=1; ... ) #Java
      
tong =0
for i in range(1,1000000,1):
    print(i)
    tong = tong +i

print (tong)
