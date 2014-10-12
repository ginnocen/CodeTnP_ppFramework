rm an.log
rm Results/foutputTrigger.root
rm Plots/canvasTrg.pdf

time root -b > an.log 2>&1 <<EOI
.x ConvertIntoRootFiles.C("Trg")
.q
EOI

time root -b > an.log 2>&1 <<EOI
.x CompareMCData.C("Trg")
.q
EOI
