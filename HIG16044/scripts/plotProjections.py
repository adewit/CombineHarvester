import CombineHarvester.CombineTools.plotting as plot
import ROOT
import numpy as np


plot.ModTDRStyle()
ROOT.gStyle.SetGridColor(17)

def createAxisHists(n,src,xmin=0,xmax=499):
  result = []
  for i in range(0,n):
    res = src.GetHistogram().Clone("tmp")
    res.Reset()
    res.SetTitle("")
    res.SetName("axis%(i)d"%vars())
    res.SetAxisRange(xmin,xmax)
    res.SetStats(0)
    result.append(res)
  return result


lumis = [35.9*1.0,35.9*2.0,35.9*4.0,35.9*6.0,35.9*8.0,35.9*10.0,35.9*14.0,35.9*18.0,35.9*25.0,35.9*30.0,35.9*35.0,35.9*40.0,35.9*45.0,35.9*50.0,35.9*55.0,35.9*60.0,35.9*65.0,35.9*70.0,35.9*75.0,35.9*80.0,35.9*83.5]

uncerts_nosyst=[0.29,0.205,0.144,0.118,0.102,0.091,0.077,0.068,0.058,0.053,0.049,0.046,0.043,0.041,0.039,0.037,0.036,0.034,0.033,0.032,0.0318]
uncerts_s1=[0.327,0.245279,0.186762,0.1604,0.1448,0.1338,0.11965,0.11045,0.1,0.097,0.093,0.089,0.087,0.084,0.082,0.080,0.079,0.078,0.076,0.074,0.074]
uncerts_s2=[0.32,0.23,0.17,0.14,0.13,0.116,0.10,0.09,0.08,0.0745,0.0706,0.067,0.064,0.061,0.0597,0.0578,0.056,0.055,0.053,0.052,0.0516]

lumis_slimmed = [35.9,100,300,1000,3000];
uncerts_s1_slimmed = [0.327,0.222296,0.142838997214,0.098286908078,0.074]
uncerts_s2_slimmed = [0.32,0.20643454039,0.127504178263,0.07685933,0.0515925189017]
uncerts_nosyst_slimmed = [0.29,0.18104178273,0.100038997214,0.0551448467967,0.0317962594509]

lumi_curve = ROOT.TF1("lumi_curve","0.29/TMath::Sqrt(x/35.9)",0.,3000.)
#lumi_curve_syst = ROOT.TF1("lumi_curve_syst","0.33/TMath::Sqrt(x/35.9)",0.,3000.)
lumi_curve.SetLineColor(ROOT.kBlack)
#lumi_curve_syst.SetLineColor(ROOT.kMagenta+3)

graph_s1 = ROOT.TGraph(len(lumis),np.array(lumis),np.array(uncerts_s1))
graph_s1_slimmed = ROOT.TGraph(len(lumis_slimmed),np.array(lumis_slimmed),np.array(uncerts_s1_slimmed))
graph_s2 = ROOT.TGraph(len(lumis),np.array(lumis),np.array(uncerts_s2))
graph_s2_slimmed = ROOT.TGraph(len(lumis_slimmed),np.array(lumis_slimmed),np.array(uncerts_s2_slimmed))
graph_s2_slimmed = ROOT.TGraph(len(lumis_slimmed),np.array(lumis_slimmed),np.array(uncerts_s2_slimmed))
graph_nosyst = ROOT.TGraph(len(lumis),np.array(lumis),np.array(uncerts_nosyst))
graph_nosyst_slimmed = ROOT.TGraph(len(lumis_slimmed),np.array(lumis_slimmed),np.array(uncerts_nosyst_slimmed))


graph_s1.SetMarkerStyle(20)
graph_s1.SetMarkerColor(ROOT.kGreen+3)
graph_s1.SetLineColor(ROOT.kGreen+3)
graph_s1.SetLineWidth(2)
graph_s1_slimmed.SetMarkerStyle(20)
graph_s1_slimmed.SetMarkerColor(ROOT.kGreen+3)
graph_s1_slimmed.SetLineColor(ROOT.kGreen+3)
graph_s1_slimmed.SetLineWidth(2)
graph_s2.SetMarkerStyle(21)
graph_s2.SetMarkerColor(ROOT.kRed)
graph_s2.SetLineColor(ROOT.kRed)
graph_s2.SetLineWidth(2)
graph_s2_slimmed.SetMarkerStyle(21)
graph_s2_slimmed.SetMarkerColor(ROOT.kRed)
graph_s2_slimmed.SetLineColor(ROOT.kRed)
graph_s2_slimmed.SetLineWidth(2)
graph_nosyst.SetLineWidth(2)
graph_nosyst.SetMarkerStyle(22)
graph_nosyst.SetMarkerColor(ROOT.kBlue)
graph_nosyst.SetLineColor(ROOT.kBlue)
graph_nosyst_slimmed.SetLineWidth(2)
graph_nosyst_slimmed.SetMarkerStyle(22)
graph_nosyst_slimmed.SetMarkerColor(ROOT.kBlue)
graph_nosyst_slimmed.SetLineColor(ROOT.kBlue)

c1 = ROOT.TCanvas()
pads=plot.OnePad()
pads[0].cd()
pads[0].SetLogx(True)
pads[0].SetGrid(3,1)
#axish = createAxisHists(1,graph_s1,0,3000)
graph_s1_slimmed.GetYaxis().SetTitle("Expected uncertainty on #mu_{VHbb}")
graph_s1_slimmed.GetXaxis().SetTitle("Integrated luminosity (fb^{-1})")
graph_s1_slimmed.GetYaxis().SetRangeUser(0,0.5)
graph_s1_slimmed.SetTitle("")
#axish[0].GetYaxis().SetRangeUser(0,0.4)
#axish[0].Draw()
#graph_s1.Draw("AL")
graph_s1_slimmed.Draw("APL")
#graph_s2.Draw("LSAME")
graph_s2_slimmed.Draw("PLSAME")
#graph_nosyst.Draw("LSAME")
graph_nosyst_slimmed.Draw("PLSAME")
#lumi_curve.Draw("LSAME")
#lumi_curve_syst.Draw("LSAME")
legend = plot.PositionedLegend(0.45,0.20,3,0.01)
legend.SetTextFont(42)
legend.SetTextSize(0.030)
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.AddEntry(graph_s1,"w/ Run 2 syst. uncert. (S1)","PL")
legend.AddEntry(graph_s2,"w/ YR18 syst. uncert. (S2)","PL")
legend.AddEntry(graph_nosyst,"w/ Stat. uncert. only","PL")
#legend.AddEntry(lumi_curve_syst,"0.33/sqrt(Lumi scale)","L")
#legend.AddEntry(lumi_curve,"0.29/sqrt(L scaling)","L")
legend.Draw("SAME")
pads[0].cd()
pads[0].GetFrame().Draw()
pads[0].RedrawAxis()

plot.DrawCMSLogo(pads[0], 'CMS', 'Projection', 11, 0.045, 0.03, 1.0, '', 1.0)
plot.DrawTitle(pads[0], "13 TeV", 3)

print "s1:"
print "35.9: ",graph_s1.Eval(35.9)
print "100: ",graph_s1.Eval(100)
print "300: ",graph_s1.Eval(300)
print "1000: ",graph_s1.Eval(1000)
print "3000: ",graph_s1.Eval(3000)

print "s2:"
print "35.9: ",graph_s2.Eval(35.9)
print "100: ",graph_s2.Eval(100)
print "300: ",graph_s2.Eval(300)
print "1000: ",graph_s2.Eval(1000)
print "3000: ",graph_s2.Eval(3000)

print "nosyst:"
print "35.9: ",graph_nosyst.Eval(35.9)
print "100: ",graph_nosyst.Eval(100)
print "300: ",graph_nosyst.Eval(300)
print "1000: ",graph_nosyst.Eval(1000)
print "3000: ",graph_nosyst.Eval(3000)



c1.SaveAs("Projection.pdf")
c1.SaveAs("Projection.png")


