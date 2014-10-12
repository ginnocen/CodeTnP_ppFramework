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

rm an.log
rm Results/foutputTracking.root
rm Plots/canvasTrk.pdf

time root -b > an.log 2>&1 <<EOI
.x ConvertIntoRootFiles.C("Trk")
.q
EOI

time root -b > an.log 2>&1 <<EOI
.x CompareMCData.C("Trk")
.q
EOI


rm an.log
rm Results/foutputMuonID.root
rm Plots/canvasTrg.pdf

time root -b > an.log 2>&1 <<EOI
.x ConvertIntoRootFiles.C("MuonID")
.q
EOI

time root -b > an.log 2>&1 <<EOI
.x CompareMCData.C("MuonID")
.q
EOI
