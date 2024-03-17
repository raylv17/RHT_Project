mkdir 0
cp -r 0_initial/fields/* 0/

blockMesh >& 01_log.mesh
setFields >& 02_log.setFields
fireRADFoam_MaCFP >& 08_log.rad
