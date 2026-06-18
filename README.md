# Hydrazine-Renderer
A very-not-real-time Ray Tracer written in Python

## Ray-Sphere Intersection Math

We have a Sphere centered at $(C_x, C_y, C_z)$ with radius $R$

The sphere in question is defined by the equation:

$R^2 = (x-C_x)^2 + (y-C_y)^2 + (z-C_z)^2$

We also have a ray folowing these parametric equations:

$x(t) = d_x \cdot t + x_0$  
$y(t) = d_y \cdot t + y_0$  
$z(t) = d_z \cdot t + z_0$

So what we want are all points such that they're part of the ray AND the sphere  
So below we plug in the parametric pieces of the ray in the sphere equation:

$R^2 = (d_x \cdot t + (x_0 - C_x))^2$  
$\:\:\:\:\:\:\:\: + (d_y \cdot t + (y_0 - C_y))^2$  
$\:\:\:\:\:\:\:\: + (d_z \cdot t + (z_0 - C_z))^2$

$R^2 = (d_x \cdot t + (x_0 - C_x))^2$  
$\:\:\:\:\:\:\:\: + (d_y \cdot t + (y_0 - C_y))^2$  
$\:\:\:\:\:\:\:\: + (d_z \cdot t + (z_0 - C_z))^2$

$R^2 = d_x^2 \cdot t^2 + 2t \cdot d_x \cdot (x_0 - C_x) + (x_0 - C_x)^2$  
$\:\:\:\:\:\:\:\: + d_y^2 \cdot t^2 + 2t \cdot d_y \cdot (y_0 - C_y) + (y_0 - C_y)^2$  
$\:\:\:\:\:\:\:\: + d_z^2 \cdot t^2 + 2t \cdot d_z \cdot (z_0 - C_z) + (z_0 - C_z)^2$

Since $t$ is now expressed like a quadratic, we can extract the coefficients and solve it that way:

$A = d_x^2 + d_y^2 + d_z^2$

$B = 2 \cdot (d_x \cdot (x_0 - C_x) + d_y \cdot (y_0 - C_y) + d_z \cdot (z_0 - C_z))$

$C = (x_0 - C_x)^2 + (y_0 - C_y)^2 + (z_0 - C_z)^2 - R^2$

where

$At^2 + Bt + C = 0$

## Ray-Plane Intersection Math

