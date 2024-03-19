# RHT_Project 
University Project for the course Radiative Heat Transfer

## Radiative Heat Transfer between two infinitely large parallel plates
 - Given a base case, the task was to create 80 simulations given the all combinations of the following parameters
   - spherical coordinate angels (theta and phi)
   - optical thickness (tau)
   - grid resolution (refinement)
- The solver used is fireRAD_MaCFP derived from OpemFOAM's firefoam
- The method used is fvDOM (Discrete Ordinate Method) aka FAM (Finite Angle Method)

### The automation is made with Python which does the following:
- Preprocessing (main_pre.py)
   - creates the necessary directories for each case and copies the base case into them
   - modifies the files within each case coresponding to its parameters
   - run the all the cases
- Posprocessing (main_post.py)
   - creates a separate directory (DATA/) and subdirectories to gather the results.
   - copies the relevant files and directories from the results (i.e. 08_log.rad, postProcessing/) from each case to data.
   - generates plots (I) and (G) from the gathered results.

   

