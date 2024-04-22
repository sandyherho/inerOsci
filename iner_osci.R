################################################
# iner_osci.R				                   #
#					                           #
# 2D Idealized Inertial Oscillation Solver     #
#					                           #
# Sandy Herho <sandy.herho@email.ucr.edu>      #
#                                              #
# 04/21/2024				                   #
################################################

# Constants
pi <- pi
freq <- -2 * pi / (24 * 3600)
f <- 2 * freq
dt <- 6 * 24 * 3600 / 120
alpha <- f * dt
beta <- 0.25 * alpha^2
ntot <- 120
uzero <- 0.05
vzero <- 0.05
initial_conditions <- c(0.1, 0.0, 0.0, 0.0)  # u, v, x, y

update_positions_and_velocities <- function(u, v, du, dv) {
  ustar <- u + du
  vstar <- v + dv
  un <- (ustar * (1 - beta) + alpha * vstar) / (1 + beta)
  vn <- (vstar * (1 - beta) - alpha * ustar) / (1 + beta)
  return(c(un, vn))
}

write_outputs <- function(file, x, y, time) {
  write(sprintf('%.6f %.6f %.2f', x, y, time), file=file, append=TRUE)
}

simulate <- function(mode) {
  conditions <- initial_conditions
  filename <- sprintf('output_R_%d.txt', mode)
  file <- file(filename, "w")
  write(sprintf('%f %f %d', freq, dt, ntot), file=file)
  
  for (n in 1:ntot) {
    time <- n * dt
    if (n == 40) {
      du <- 0.0
      dv <- -0.3
    } else if (n == 80) {
      du <- 0.0
      dv <- 0.1
    } else {
      du <- 0.0
      dv <- 0.0
    }
    
    if (mode == 1) {
      velocities <- update_positions_and_velocities(conditions[1], conditions[2], du, dv)
      u <- velocities[1]
      v <- velocities[2]
    } else {
      u <- cos(alpha) * conditions[1] + sin(alpha) * conditions[2] + du
      v <- cos(alpha) * conditions[2] - sin(alpha) * conditions[1] + dv
    }
    
    x <- conditions[3] + dt * (u + uzero) / 1000
    y <- conditions[4] + dt * (v + vzero) / 1000
    conditions <- c(u, v, x, y)
    
    write_outputs(filename, x, y, time)
  }
  
  close(file)
}

# Run simulations
simulate(1)
simulate(2)
