PROGRAM iner_osci

!*******************************************
! Predictions of the path of a water
! parcel subject to inertial oscillations.
! 
! Sandy Herho <sh001@ucr.edu>
! 04/20/24
!*******************************************

REAL :: u,v,un,vn,x,y,xn,yn
REAL :: u2,v2,un2,vn2,x2,y2,xn2,yn2
REAL :: uzero, vzero, du, dv
REAL :: dt,freq,f,pi,alpha,beta
INTEGER :: n,ntot

! ambient flow
uzero = 0.05
vzero = 0.05

! initial relative speed and location
u = 0.1
v = 0.0
x = 0.
y = 0.

! Initialize mode 2 variables
u2 = u
v2 = v
x2 = x
y2 = y

pi = 4.*atan(1.)
freq = -2.*pi/(24.*3600.)
f = 2*freq
dt = 6.*24.*3600./120.
alpha = f*dt
beta = 0.25*alpha*alpha

ntot = 120;

! Open output files for both modes
OPEN(10,FILE='output1.txt',FORM='formatted')
OPEN(20,FILE='output2.txt',FORM='formatted')

WRITE(10,*) 'freq', 'dt', 'ntot'
WRITE(20,*) 'freq', 'dt', 'ntot'

!**** start of iteration loop ****
DO n = 1,ntot
!*********************************

time = REAL(n)*dt
du = 0.0
dv = 0.0

IF(n == 40) THEN
 du = 0.0
 dv = -0.3
END IF

IF(n == 80) THEN
 du = 0.0
 dv = 0.1
END IF

! Calculations for mode 1
ustar = u + du
vstar = v + dv

un = (ustar*(1-beta)+alpha*vstar)/(1+beta)
vn = (vstar*(1-beta)-alpha*ustar)/(1+beta)

xn = x + dt*(un+uzero)/1000.0
yn = y + dt*(vn+vzero)/1000.0

u = un
v = vn
x = xn
y = yn

WRITE(10,*) x, y, time

! Calculations for mode 2
ustar = u2 + du
vstar = v2 + dv

un2 = cos(alpha)*ustar+sin(alpha)*vstar
vn2 = cos(alpha)*vstar-sin(alpha)*ustar

xn2 = x2 + dt*(un2+uzero)/1000.0
yn2 = y2 + dt*(vn2+vzero)/1000.0

u2 = un2
v2 = vn2
x2 = xn2
y2 = yn2

WRITE(20,*) x2, y2, time

!**** end of iteration loop ****
END DO
!*******************************

END PROGRAM iner_osci
